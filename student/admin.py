from django.contrib import admin
from .models import Student
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
from django.utils.safestring import mark_safe


class ImageInline(admin.TabularInline):
    model = StudentImagesData
    fields = ('student', 'image_data'),
    extra = 1
    classes = 'collapse',


class StudentAdmin(ImportExportModelAdmin):
    list_display = (
        'student_code', 'first_name', 'last_name', 'email', 'username', 'password', 'student_video_data',
        'comment',)
    list_filter = ('student_code',)
    search_fields = ('student_code',)
    inlines = (ImageInline,)
    fieldsets = (
        (None, {
            'fields': ('student_code', 'first_name', 'last_name', 'email', 'student_video_data', 'comment',)
        }),
        ('Advance options', {
            'fields': ('username', 'password',),
            'description': 'option advance',
            'classes': ('collapse',),
        }),
    )
    summernote_fields = 'comment'

    resource_class = StudentsResource

    """
    @staticmethod
    def student_image_show(student):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=teacher.student_image.url,
            # width=teacher.teacher_image.width,
            width=80,
            # height=teacher.teacher_image.height,
            height=80
        )
        )

    @staticmethod
    def student_full_image_show(student):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=student.student_image.url,
            width=student.student_image.width,
            height=student.student_image.height,
        )
        )

    student_full_image_show.short_description = 'Full Image'
    """


# Register your models Student.
admin.site.register(Student, StudentAdmin)
