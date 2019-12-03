# Generated by Django 2.2.7 on 2019-12-03 11:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('absent_status', models.BooleanField(default=False)),
                ('image_data', models.FileField(upload_to='media/students/images/{student_code(student_name)}')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_code', models.CharField(max_length=20)),
                ('course_name', models.CharField(default='Course name', max_length=50)),
                ('start_day', models.DateTimeField(null=True)),
                ('end_day', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CourseScheduleDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule_code', models.CharField(max_length=20)),
                ('schedule_date', models.DateTimeField(auto_now_add=True)),
                ('schedule_numberof_day', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='StudentsInCourseDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Course')),
            ],
        ),
    ]
