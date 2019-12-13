from django.contrib import admin
from django import forms
from django.contrib import admin
from .models import Teacher
from django.db.models import Count
from student.models import Student, StudentImagesData
from django.utils import timezone
from course.models import Course
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from course.resources import CoursesResource
import csv
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from datetime import datetime
from import_export.resources import Resource, DeclarativeMetaclass
import django
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
import functools
import logging
import tablib
import traceback
from collections import OrderedDict
from copy import deepcopy
from diff_match_patch import diff_match_patch
import django
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.core.management.color import no_style
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.models.fields.related import ForeignObjectRel
from django.db.models.query import QuerySet
from django.db.transaction import (
    TransactionManagementError,
    atomic,
    savepoint,
    savepoint_commit,
    savepoint_rollback
)
import openpyxl
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe



# Register your models here.
class TeacherChoiceField(forms.ModelChoiceField):
    @staticmethod
    def label_from_instance(obj):
        return "{0}: {1} {2}".format(obj.teacher_code, obj.first_name, obj.last_name)


class CourseAdmin(ImportExportModelAdmin):
    # class CourseAdmin(ImportExportModelAdmin):
    list_display = ('course_code', 'course_name', 'start_day', 'end_day', 'teacher', 'student_count', 'children_display'
                    , 'class_time', 'class_time_calendar', 'class_time_begin_time',)
    search_fields = ('course_code',)
    fieldsets = (
        (None, {
            'fields': ('course_code', 'course_name', 'start_day', 'end_day', 'teacher', 'class_time',
                       'class_time_calendar', 'class_time_begin_time',)
        }),
        ('Advance options', {
            'fields': ('students',),
            'description': 'option advance',
            'classes': ('collapse',),
        }),
    )
    filter_horizontal = ('students',)
    # filter_vertical = ('students',)
    list_filter = (
        ('teacher', RelatedDropdownFilter),
        ('start_day', DateRangeFilter), ('end_day', DateTimeRangeFilter),
    )

    list_per_page = 20
    date_hierarchy = 'start_day'
    raw_id_fields = ["teacher", ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'teacher':
            return TeacherChoiceField(queryset=Teacher.objects.all())
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def children_display(self, obj):
        return ", ".join([
            students.student_code for students in obj.students.all()
        ])

    children_display.short_description = "Students List"

    @staticmethod
    def children_display(obj):
        display_text = ", ".join([
            "<a href={}>{}</a>".format(
                reverse('admin:{}_{}_change'.format(obj._meta.app_label, obj._meta.model_name),
                        args=(students.pk,)),
                students.__str__)
            for students in obj.students.all()
        ])
        if display_text:
            return mark_safe(display_text)
        return "-"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            student_count=Count("students", distinct=True),
        )
        return queryset

    @staticmethod
    def student_count(obj):
        # return obj.students.count()
        return obj.student_count

    student_count.admin_order_field = 'student_count'

    actions = ["export_as_csv"]

    @staticmethod
    def set_csv_file_name():
        return 'Courses'

    def export_as_csv(self, request, queryset):
        # noinspection PyProtectedMember
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        name = self.set_csv_file_name()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={0}.csv'.format(name)
        writer = csv.writer(response)
        writer.writerow(['Ma mon hoc', 'Ten mon hoc', 'Ngay bat dau', 'Ngay ket thuc', 'Giao vien phu trach',
                         'Buoi hoc', 'Tiet bat dau', 'Duration'])
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"
    """
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    """


    def write_to_tmp_storage(self, import_file, input_format):
        tmp_storage = self.get_tmp_storage_class()()
        data = bytes()
        for chunk in import_file.chunks():
            data += chunk

        tmp_storage.save(data, input_format.get_read_mode())
        return tmp_storage

    def import_action(self, request, *args, **kwargs):
        if not self.has_import_permission(request):
            raise PermissionDenied

        context = self.get_import_context_data()
        print("show context")
        print(context)
        import_formats = self.get_import_formats()

        form_type = self.get_import_form()
        form_kwargs = self.get_form_kwargs(form_type, *args, **kwargs)
        form = form_type(import_formats,
                         request.POST or None,
                         request.FILES or None,
                         **form_kwargs)

        if request.POST and form.is_valid():
            input_format = import_formats[
                int(form.cleaned_data['input_format'])
            ]()
            import_file = form.cleaned_data['import_file']
            """
            code change data file excel here
            """
            wb = openpyxl.load_workbook(import_file)
            worksheet = wb.active
            worksheet.delete_rows(0, 9)
            worksheet.delete_cols(1, 1)
            worksheet.delete_cols(7, 6)
            # worksheet.append(["student_code", "first_name", "last_name", "email", "username", "password"])
            worksheet.insert_rows(1)
            wb.save(import_file)
            # check
            # first always write the uploaded file to disk as it may be a
            # memory file or else based on settings upload handlers
            tmp_storage = self.write_to_tmp_storage(import_file, input_format)

            # then read the file, using the proper format-specific mode
            # warning, big files may exceed memory
            try:
                data = tmp_storage.read(input_format.get_read_mode())
                if not input_format.is_binary() and self.from_encoding:
                    data = force_text(data, self.from_encoding)
                dataset = input_format.create_dataset(data)
                dataset.headers = ['student_code', 'first_name', 'email', 'username', 'password',
                                   'comment']
                print("show dataset")
                print(dataset)
            except UnicodeDecodeError as e:
                return HttpResponse(_(u"<h1>Imported file has a wrong encoding: %s</h1>" % e))
            except Exception as e:
                return HttpResponse(
                    _(u"<h1>%s encountered while trying to read file: %s</h1>" % (type(e).__name__, import_file.name)))

            # prepare kwargs for import data, if needed
            res_kwargs = self.get_import_resource_kwargs(request, form=form, *args, **kwargs)
            resource = self.get_import_resource_class()(**res_kwargs)

            # prepare additional kwargs for import_data, if needed
            imp_kwargs = self.get_import_data_kwargs(request, form=form, *args, **kwargs)

            result = resource.import_data(dataset, dry_run=True,
                                          raise_errors=False,
                                          file_name=import_file.name,
                                          user=request.user,
                                          **imp_kwargs)

            context['result'] = result

            if not result.has_errors() and not result.has_validation_errors():
                initial = {
                    'import_file_name': tmp_storage.name,
                    'original_file_name': import_file.name,
                    'input_format': form.cleaned_data['input_format'],
                }
                confirm_form = self.get_confirm_import_form()
                initial = self.get_form_kwargs(form=form, **initial)
                context['confirm_form'] = confirm_form(initial=initial)
        else:
            res_kwargs = self.get_import_resource_kwargs(request, form=form, *args, **kwargs)
            resource = self.get_import_resource_class()(**res_kwargs)

        context.update(self.admin_site.each_context(request))

        context['title'] = _("Import")
        context['form'] = form
        context['opts'] = self.model._meta
        # context['fields'] = [f.column_name for f in resource.get_user_visible_fields()]
        context['fields'] = ['student_code', 'first_name', 'email', 'username', 'password',
                             'comment']
        request.current_app = self.admin_site.name
        return TemplateResponse(request, [self.import_template_name],
                                context)


admin.site.register(Course, CourseAdmin)
