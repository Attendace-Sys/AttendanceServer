# Generated by Django 2.2.7 on 2019-12-20 04:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to=settings.AUTH_USER_MODEL)),
                ('teacher_code', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('teacher_image', models.ImageField(null=True, upload_to='teachers/images')),
            ],
            options={
                'verbose_name_plural': 'Quản lý giáo viên',
            },
            bases=('User.user',),
        ),
    ]