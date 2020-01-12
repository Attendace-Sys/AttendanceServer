from import_export import resources, fields
from import_export.widgets import JSONWidget, ManyToManyWidget, ForeignKeyWidget
from django.contrib import admin
from django.db.models import Count
from student.models import Student, StudentImagesData
from django.utils import timezone
from course.models import Course
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from import_export.results import Error, Result, RowResult
from import_export.admin import ImportExportModelAdmin
import csv
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from datetime import datetime
from import_export.resources import Resource, DeclarativeMetaclass
from import_export.resources import Error, Result, RowResult
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin, messages
from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry
from django.contrib.auth import get_permission_codename
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST
from django.db import DEFAULT_DB_ALIAS, connections
from import_export.utils import atomic_if_using_transaction
from django.db.transaction import (
    TransactionManagementError,
    atomic,
    savepoint,
    savepoint_commit,
    savepoint_rollback
)
from django.core.exceptions import ImproperlyConfigured, ValidationError
import traceback
from copy import deepcopy
import tablib
from student.models import Student
from student.admin import StudentAdmin
import logging
from django.db import transaction

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CoursesResource(resources.ModelResource):
    # student = fields.Field(attribute='students', widget=ManyToManyWidget(model=Student, field='students'),
    #                       column_name='Student')
    students = fields.Field(
        attribute='students',
        widget=ManyToManyWidget(model=Student, separator=',', field='student_code'),
    )
    
    class Meta:
        model = Course
        fields = ('course_code', 'course_name', 'start_day', 'end_day', 'teacher', 'students', 'day_of_week',
                  'time_start_of_course', 'time_duration')
        export_order = fields
        import_id_fields = ('course_code',)
        skip_unchanged = True
        report_skipped = False

    def import_row(self, row, instance_loader, using_transactions=True, dry_run=False, **kwargs):
        try:
            row['student_code'] = str(row['student_code'])
        except:
            pass
        row_result = self.get_row_result_class()()
        try:
            self.before_import_row(row, **kwargs)
            instance, new = self.get_or_init_instance(instance_loader, row)
            self.after_import_instance(instance, new, **kwargs)
            if new:
                row_result.import_type = RowResult.IMPORT_TYPE_NEW
            else:
                row_result.import_type = RowResult.IMPORT_TYPE_UPDATE
            row_result.new_record = new
            original = deepcopy(instance)
            # print("Get instance ----------------------------------------")
            # print(row)
            print(dry_run)
            diff = self.get_diff_class()(self, original, new)
            if self.for_delete(row, instance):
                if new:
                    row_result.import_type = RowResult.IMPORT_TYPE_SKIP
                    diff.compare_with(self, None, dry_run)
                else:
                    row_result.import_type = RowResult.IMPORT_TYPE_DELETE
                    self.delete_instance(instance, using_transactions, dry_run)
                    diff.compare_with(self, None, dry_run)
            else:
                import_validation_errors = {}
                try:
                    self.import_obj(instance, row, dry_run)
                except ValidationError as e:
                    # Validation errors from import_obj() are passed on to
                    # validate_instance(), where they can be combined with model
                    # instance validation errors if necessary
                    import_validation_errors = e.update_error_dict(import_validation_errors)
                if self.skip_row(instance, original):
                    row_result.import_type = RowResult.IMPORT_TYPE_SKIP
                else:
                    self.validate_instance(instance, import_validation_errors)
                    self.save_instance(instance, using_transactions, dry_run)
                    self.save_m2m(instance, row, using_transactions, dry_run)
                    # Add object info to RowResult for LogEntry
                    row_result.object_id = instance.pk
                    row_result.object_repr = force_text(instance)
                diff.compare_with(self, instance, dry_run)

            row_result.diff = diff.as_html()
            self.after_import_row(row, row_result, **kwargs)

        except ValidationError as e:
            row_result.import_type = RowResult.IMPORT_TYPE_INVALID
            row_result.validation_error = e
        except Exception as e:
            row_result.import_type = RowResult.IMPORT_TYPE_ERROR
            if not isinstance(e, TransactionManagementError):
                logger.debug(e, exc_info=e)
            tb_info = traceback.format_exc()
            row_result.errors.append(self.get_error_result_class()(e, tb_info, row))
        return row_result

    def import_data(self, dataset, dry_run=False, raise_errors=False,
                    use_transactions=None, collect_failed_rows=False, **kwargs):
        """
        Imports data from ``tablib.Dataset``. Refer to :doc:`import_workflow`
        for a more complete description of the whole import process.

        :param dataset: A ``tablib.Dataset``

        :param raise_errors: Whether errors should be printed to the end user
            or raised regularly.

        :param use_transactions: If ``True`` the import process will be processed
            inside a transaction.

        :param collect_failed_rows: If ``True`` the import process will collect
            failed rows.

        :param dry_run: If ``dry_run`` is set, or an error occurs, if a transaction
            is being used, it will be rolled back.
        """

        if use_transactions is None:
            use_transactions = self.get_use_transactions()

        connection = connections[DEFAULT_DB_ALIAS]
        supports_transactions = getattr(connection.features, "supports_transactions", False)

        if use_transactions and not supports_transactions:
            raise ImproperlyConfigured

        using_transactions = (use_transactions or dry_run) and supports_transactions

        with atomic_if_using_transaction(using_transactions):
            return self.import_data_inner(dataset, dry_run, raise_errors, using_transactions, collect_failed_rows, **kwargs)

    def import_data_inner(self, dataset, dry_run, raise_errors, using_transactions, collect_failed_rows, **kwargs):
        result = self.get_result_class()()
        result.diff_headers = self.get_diff_headers()
        result.total_rows = len(dataset)

        if using_transactions:
            # when transactions are used we want to create/update/delete object
            # as transaction will be rolled back if dry_run is set
            sp1 = savepoint()

        try:
            with atomic_if_using_transaction(using_transactions):
                self.before_import(dataset, using_transactions, dry_run, **kwargs)
        except Exception as e:
            logger.debug(e, exc_info=e)
            tb_info = traceback.format_exc()
            result.append_base_error(self.get_error_result_class()(e, tb_info))
            if raise_errors:
                raise

        instance_loader = self._meta.instance_loader_class(self, dataset)

        # Update the total in case the dataset was altered by before_import()
        result.total_rows = len(dataset)

        if collect_failed_rows:
            result.add_dataset_headers(dataset.headers)

        for i, row in enumerate(dataset.dict, 1):
            with atomic_if_using_transaction(using_transactions):
                row_result = self.import_row(
                    row,
                    instance_loader,
                    using_transactions=using_transactions,
                    dry_run=dry_run,
                    **kwargs
                )
            result.increment_row_result_total(row_result)

            if row_result.errors:
                if collect_failed_rows:
                    result.append_failed_row(row, row_result.errors[0])
                if raise_errors:
                    raise row_result.errors[-1].error
            elif row_result.validation_error:
                result.append_invalid_row(i, row, row_result.validation_error)
                if collect_failed_rows:
                    result.append_failed_row(row, row_result.validation_error)
                if raise_errors:
                    raise row_result.validation_error
            if (row_result.import_type != RowResult.IMPORT_TYPE_SKIP or
                    self._meta.report_skipped):
                result.append_row_result(row_result)

        try:
            with atomic_if_using_transaction(using_transactions):
                self.after_import(dataset, result, using_transactions, dry_run, **kwargs)
        except Exception as e:
            logger.debug(e, exc_info=e)
            tb_info = traceback.format_exc()
            result.append_base_error(self.get_error_result_class()(e, tb_info))
            if raise_errors:
                raise

        if using_transactions:
            if dry_run or result.has_errors():
                savepoint_rollback(sp1)
            else:
                savepoint_commit(sp1)

        return result
