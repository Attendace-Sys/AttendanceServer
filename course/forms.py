from django import forms
from course.models import Schedule, ScheduleImagesData
from multiupload.fields import MultiFileField


class ScheduleImagesDataForms(forms.ModelForm):
    class Meta:
        model = ScheduleImagesData
        fields = ['schedule', 'image_data']


class ScheduleForms(forms.ModelForm):
    json_data = forms.CharField(max_length=1024)

    class Meta:
        model = Schedule
        fields = ['schedule_code']

    files = MultiFileField(min_num=1, max_num=15)
  
 