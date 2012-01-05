# encoding: utf-8

from django.db import models


class Notification(models.Model):
    title = models.CharField(max_length=255, verbose_name=u'标题')
    content = models.TextField(verbose_name=u'内容')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = u'通知'
        verbose_name_plural = u'通知'

    def __unicode__(self):
        return self.title
