from import_export import resources
from student.models import Student


class StudentsResource(resources.ModelResource):
    class Meta:
        model = Student
        fields = ('student_code', 'first_name', 'last_name', 'email', 'username', 'password', 'student_video_data')
        export_order = ('student_code', 'first_name', 'last_name', 'email', 'username', 'password', 'student_video_data')
        import_id_fields = ('student_code',)
        skip_unchanged = True
        report_skipped = False
