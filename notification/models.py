# encoding: utf-8

from django.db import models

import smtplib, email, sys
from email.Message import Message

smtpserver='smtp.gmail.com'
smtpuser='kuanmin.hu@gmail.com'
smtppass='hu315165863km'
smtpport='587'
to = 'kuanmin.hu@gmail.com'
subj = ''
text = ''

def connect():
    server=smtplib.SMTP(smtpserver, smtpport)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(smtpuser, smtppass)
    return server

def sendmessage(server, to, subj, content):
    msg = Message()
    msg['Mime-Version']='1.0'
    msg['From'] = smtpuser
    msg['To'] = to
    msg['Subject'] = subj
    msg['Date']= email.Utils.formatdate()
    msg.set_payload(content)
    server.sendmail(smtpuser,to,str(msg))

class Notification(models.Model):
    title = models.CharField(max_length=255, verbose_name=u'标题')
    content = models.TextField(verbose_name=u'内容')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

 ##   def save(self):
 ##      super(Notification, self).save()
       #subj = 
       #server = connect()
       #sendmessage(server, to, subj, text)

    class Meta:
        verbose_name = u'通知'
        verbose_name_plural = u'通知'

    def __unicode__(self):
        return self.title
    
    
