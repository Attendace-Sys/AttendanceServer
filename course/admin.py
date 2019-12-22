from django.contrib import admin
from django import forms
from django.contrib import admin
from .models import Teacher
from django.db.models import Count
from student.models import Student, StudentImagesData
from django.utils import timezone
from course.models import Course, Schedule, Attendance, ScheduleImagesData
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from import_export import resources
from import_export.admin import ImportExportModelAdmin
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
from course.resources import CoursesResource
from import_export.resources import ModelResource
from student.models import Student
from student.admin import StudentAdmin


# Register your models here.
class TeacherChoiceField(forms.ModelChoiceField):
    @staticmethod
    def label_from_instance(obj):
        return "{0}: {1} {2}".format(obj.teacher_code, obj.first_name, obj.last_name)


class CourseAdmin(ImportExportModelAdmin):
    list_display = (
        'course_code', 'course_name', 'children_display', 'start_day', 'end_day', 'teacher', 'student_count',
        'day_of_week', 'time_start_of_course', 'duaration',)
    search_fields = ('course_code',)
    fieldsets = (
        (None, {
            'fields': ('course_code', 'course_name', 'start_day', 'end_day', 'teacher', 'day_of_week',
                       'time_start_of_course', 'time_duration',)
        }),
        ('Advance options', {
            'fields': ('students',),
            'description': 'option advance',
            'classes': ('collapse',),
        }),
    )
    readonly_fields = []
    filter_horizontal = ('students',)
    list_filter = (
        ('teacher', RelatedDropdownFilter),
        ('start_day', DateRangeFilter), ('end_day', DateTimeRangeFilter),
    )
    resource_class = CoursesResource

    list_per_page = 20
    date_hierarchy = 'start_day'
    raw_id_fields = ["teacher", ]

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ['course_code', ]
        return self.readonly_fields

    @staticmethod
    def duaration(obj):
        # return obj.students.count()
        return " " + str(obj.time_duration) + " tiết "

    duaration.short_description = "Time duration"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'teacher':
            return TeacherChoiceField(queryset=Teacher.objects.all())
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def children_display(self, obj):
        return ", ".join([
            # students.student_code for students in obj.students.all()
            students.__str__() for students in obj.students.all()
        ])

    children_display.short_description = "Students List"

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

    def write_to_tmp_storage(self, import_file, input_format):
        tmp_storage = self.get_tmp_storage_class()()
        data = bytes()
        for chunk in import_file.chunks():
            data += chunk

        tmp_storage.save(data, input_format.get_read_mode())
        return tmp_storage
    """

    def export_action(self, request, *args, **kwargs):
        if not self.has_export_permission(request):
            raise PermissionDenied

        formats = self.get_export_formats()
        form = ExportForm(formats, request.POST or None)
        if form.is_valid():
            file_format = formats[
                int(form.cleaned_data['file_format'])
            ]()

            queryset = self.get_export_queryset(request)
            export_data = self.get_export_data(file_format, queryset, request=request)
            content_type = file_format.get_content_type()
            response = HttpResponse(export_data, content_type=content_type)
            response['Content-Disposition'] = 'attachment; filename="%s"' % (
                self.get_export_filename(request, queryset, file_format),
            )

            post_export.send(sender=None, model=self.model)
            return response

        context = self.get_export_context_data()

        context.update(self.admin_site.each_context(request))

        context['title'] = _("Export")
        context['form'] = form
        context['opts'] = self.model._meta
        request.current_app = self.admin_site.name
        return TemplateResponse(request, [self.export_template_name],
                                context)
    """
    def import_action(self, request, *args, **kwargs):
        if not self.has_import_permission(request):
            raise PermissionDenied

        context = self.get_import_context_data()

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
            # input_format = Excel
            import_file = form.cleaned_data['import_file']

            # first always write the uploaded file to disk as it may be a

            wb = openpyxl.load_workbook(import_file)
            worksheet = wb.active
            try:
                t_course_code = worksheet.cell(row=6, column=4).value
                t_course_code = t_course_code[5:]
                t_course_name = worksheet.cell(row=6, column=1).value
                t_course_name = t_course_name[8:]
                t_start_day = ''
                t_end_day = ''
                t_teacher = worksheet.cell(row=7, column=4).value
                t_teacher = t_teacher[15:]
                t_students = ""
                t_class_time = '2'
                t_class_time_calendar = '2'
                t_class_time_begin_time = '1'
            except Exception as e:
                return HttpResponse(
                    _(u"<h1>%s encountered while trying to read file: %s</h1>"
                      u"<h1> Make sure its a real import format</h1> " %
                      (type(e).__name__, import_file.name)))
            # create new wb for save data

            count_data_row = worksheet.max_row
            for x in range(10, 10 + count_data_row):
                if worksheet.cell(row=x, column=2).value:
                    t_students = t_students + "," + str(worksheet.cell(row=x, column=2).value)

            wb.create_sheet(title="Sheet1", index=0)
            us_ws = wb.active
            us_ws.append(["course_code", "course_name", "start_day", "end_day", "teacher", "students", "class_time",
                          "class_time_calendar", "class_time_begin_time"])
            # add row here
            us_ws.append([t_course_code, t_course_name, t_start_day, t_end_day, t_teacher, t_students, t_class_time,
                          t_class_time_calendar, t_class_time_begin_time])

            wb.save(import_file)
            # ===============================================================================================
            # memory file or else based on settings upload handlers
            tmp_storage = self.write_to_tmp_storage(import_file, input_format)

            # then read the file, using the proper format-specific mode
            # warning, big files may exceed memory
            try:
                data = tmp_storage.read(input_format.get_read_mode())
                if not input_format.is_binary() and self.from_encoding:
                    data = force_text(data, self.from_encoding)
                dataset = input_format.create_dataset(data)
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
        context['fields'] = [f.column_name for f in resource.get_user_visible_fields()]
        request.current_app = self.admin_site.name
        return TemplateResponse(request, [self.import_template_name],
                                context)


class CourseChoiceField(forms.ModelChoiceField):
    @staticmethod
    def label_from_instance(obj):
        return "{0}: {1} {2}".format(obj.course_code, obj.course_name, obj.teacher)


class ScheduleImagesDataInline(admin.TabularInline):
    model = ScheduleImagesData
    fields = ('schedule', 'image_data'),
    extra = 1
    # classes = 'collapse',


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('schedule_code', 'course', 'schedule_date', 'schedule_number_of_day')
    search_fields = ('schedule_code',)
    inlines = (ScheduleImagesDataInline,)
    fieldsets = (
        (None, {
            'fields': ('course',  'schedule_number_of_day')
        }),
    )
    readonly_fields = ['schedule_code', 'course', 'schedule_date', 'schedule_number_of_day']
    # filter_horizontal = ('students',)
    list_filter = (
        ('course', RelatedDropdownFilter),
        # ('start_day', DateRangeFilter), ('end_day', DateTimeRangeFilter),
    )

    list_per_page = 20
    raw_id_fields = ["course", ]

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ['schedule_code', 'course', 'schedule_date', 'schedule_number_of_day' ]
        return self.readonly_fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'course':
            return CourseChoiceField(queryset=Course.objects.all())
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ScheduleChoiceField(forms.ModelChoiceField):
    @staticmethod
    def label_from_instance(obj):
        return "{0}: {1} {2}".format(obj.course, obj.schedule_code, obj.schedule_number_of_day)


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('attendance_code', 'student', 'schedule_code', 'date', 'absent_status', 'image_data', 'checked_status')
    search_fields = ('attendance_code', 'checked_status',)

    fieldsets = (
        (None, {
            'fields': ('student', 'schedule_code', 'absent_status', 'image_data',)
        }),

    )
    # filter_horizontal = ('students',)
    list_filter = (
        ('student', RelatedDropdownFilter),
        ('schedule_code', RelatedDropdownFilter),
    )

    list_per_page = 20
    raw_id_fields = ["schedule_code", ]
    """
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'course':
            return CourseChoiceField(queryset=Course.objects.all())
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    """


admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Course, CourseAdmin)
