# encoding: utf-8

import os
from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.conf import settings

def handle_uploading(instance, filename):
    username = instance.user.username
    return os.path.join(settings.MEDIA_ROOT, 'contacts', username, 'index.html')


class ContactManager(models.Manager):
    def by_user(self, user):
        queryset = self.filter(user=user)[:1]

        if len(queryset) > 0:
            return queryset[0]
        else:
            return None


class Contact(models.Model):
    user = models.OneToOneField(User)
    html = models.FileField(upload_to=handle_uploading)
    fullname = models.CharField(max_length=255, default='', verbose_name=u'全名')
    email = models.EmailField(default='', verbose_name=u'Email')
    phone = models.CharField(max_length=15, default='', verbose_name=u'电话号码')
    qq = models.CharField(max_length=15, default='', verbose_name=u'QQ 号码')

    objects = ContactManager()


class ContactUploadForm(forms.Form):
    html = forms.FileField(label=u'个人页面 HTML 文件')


class ContactEditForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('fullname', 'email', 'phone', 'qq')
