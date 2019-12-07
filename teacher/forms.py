from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from teacher.models import Teacher
from django.db import models

class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        # fields = ['']
        fields = ['teacher_code', 'first_name', 'last_name', 'email', 'teacher_image', 'username', 'password']
 
    def save(self, commit=True):
        instance = super(TeacherForm, self).save(commit)
        return instance
