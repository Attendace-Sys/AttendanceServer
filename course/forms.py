from django import forms
from course.models import Schedule, ScheduleImagesData
from multiupload.fields import MultiFileField


class ScheduleImagesDataForms(forms.ModelForm):
    class Meta:
        model = ScheduleImagesData
        fields = ['schedule', 'image_data']


class ScheduleForms(forms.ModelForm):
    json_data = forms.CharField(max_length=1024, required=False)
    schedule_code = forms.CharField(required=False)
    schedule_number_of_day = forms.IntegerField(required=False)

    class Meta:
        model = Schedule
        fields = ['schedule_code', 'json_data']

    files = MultiFileField(min_num=1, max_num=15)
  
    def save(self, commit=True):
        instance = super(ScheduleForms, form).save(commit)
        for each in self.cleaned_data['files']:
            ScheduleImagesData.objects.create(image_data=each, schedule=instance)
        return instance
