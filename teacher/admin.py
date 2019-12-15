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
from django.utils.safestring import mark_safe
from django.contrib.auth import authenticate
from .forms import TeacherFormCreationForm, TeacherFormChangeForm


class ImageInline(admin.TabularInline):
    model = StudentImagesData
    fields = ('student', 'image_data'),
    extra = 1
    classes = 'collapse',


class TeacherAdmin(ImportExportModelAdmin):

    list_display = ('teacher_code', 'get_full_name', 'email', 'username', 'password', 'date_joined',
                    'teacher_image_show', 'days_since_creation', 'is_staff', 'is_superuser')
    search_fields = ('teacher_code',)
    date_created = 'date_joined'
    list_per_page = 10
    actions = ['delete_media', ]
    readonly_fields = ['date_joined', 'days_since_creation', 'teacher_full_image_show']

    fieldsets = (
        (None, {
            'fields': (
                'teacher_code', 'first_name', 'email', 'teacher_image',
                'username', 'password', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions', ),
        }),
        ('Advance options', {
            'fields': ('date_joined', 'teacher_full_image_show'),
            'description': 'option advance',
            'classes': ('collapse',),
        }),
    )
    list_filter = (
        ('teacher_code', DropdownFilter),
        # ('Course', RelatedDropdownFilter)
    )

    filter_horizontal = ('groups', 'user_permissions')

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ['teacher_code', ]
        return self.readonly_fields

    @staticmethod
    def teacher_image_show(teacher):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=teacher.teacher_image.url,
            # width=teacher.teacher_image.width,
            width=80,
            # height=teacher.teacher_image.height,
            height=80
        )
        )

    @staticmethod
    def teacher_full_image_show(teacher):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=teacher.teacher_image.url,
            width=teacher.teacher_image.width,
            height=teacher.teacher_image.height,
        )
        )

    teacher_full_image_show.short_description = 'Full Image'

    def get_full_name(self, teacher):
        return teacher.first_name + teacher.last_name

    get_full_name.short_description = 'Full Name'

    @staticmethod
    def get_odering(request):
        if request.user.is_superuser:
            return 'teacher_code', 'first_name',
        return 'teacher_code',

    def delete_media(self, request, queryset):
        count = queryset.update(teacher_image=False)
        self.message_user(request, '{} The selected name have been delete'.format(count))

    delete_media.short_description = 'Delete image'

    def days_since_creation(self, teacher):
        diff = timezone.now().day - teacher.date_joined.day
        return (diff + 1).__str__() + ' Day since creation'

    days_since_creation.short_description = 'Date since created'

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super(TeacherAdmin, self).save_model(request, obj, form, change)


# Register your models Teacher.
admin.site.register(Teacher, TeacherAdmin)
