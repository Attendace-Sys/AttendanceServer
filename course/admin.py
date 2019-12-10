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
from student.resources import StudentsResource
import csv
from django.http import HttpResponse
from django.urls import path
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.safestring import mark_safe


# Register your models here.
class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


class ExportCsvMixin:

    def __init__(self):
        pass

    def export_as_csv(self, request, queryset):
        # noinspection PyProtectedMember
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


class TeacherChoiceField(forms.ModelChoiceField):
    @staticmethod
    def label_from_instance(obj):
        return "{0}: {1} {2}".format(obj.teacher_code, obj.first_name, obj.last_name)


class CourseAdmin(ImportExportModelAdmin, ExportCsvMixin):
    list_display = ('course_code', 'course_name', 'start_day', 'end_day', 'teacher', 'student_count', 'children_display',)
    # list_filter = ('course_code', )
    search_fields = ('course_code',)
    fieldsets = (
        (None, {
            'fields': ('course_code', 'course_name', 'start_day', 'end_day', 'teacher',)
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

    change_list_template = "courses_changelist.html"
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
    """
    def children_display(self, obj):
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
    """
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            reader = csv.reader(csv_file)
            # Create Hero objects from passed in data
            # ...
            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "csv_form.html", payload
        )

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

    def export_as_csv(self, request, queryset):
        pass

    export_as_csv.short_description = "Export Selected"

    # return file name
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

        # writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    """
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    """


admin.site.register(Course, CourseAdmin)
