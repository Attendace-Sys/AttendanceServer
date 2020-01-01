from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from teacher.models import Teacher
from django import forms
from django.db import models
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class TeacherForm(ModelForm):
    teacher_image = forms.ImageField(required=False)

    class Meta:
        model = Teacher
        fields = ['teacher_code', 'first_name', 'email', 'teacher_image', 'password',
                  'date_joined']

    def save(self, commit=True):
        instance = super(TeacherForm, self).save(commit)
        return instance


class TeacherFormCreationForm(UserCreationForm):
    teacher_image = forms.ImageField(required=False)
    class Meta:
        model = Teacher
        fields = ('teacher_code', 'first_name', 'email')


class TeacherFormChangeForm(UserChangeForm):
    teacher_image = forms.ImageField(required=False)
    class Meta:
        model = Teacher
        fields = ('teacher_code', 'first_name', 'email')
