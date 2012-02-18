# encoding: utf-8

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django import forms
from annoying.decorators import render_to
from django.contrib.auth import logout

from helpers import create_users_from_list

class UserListForm(forms.Form):
    text = forms.CharField(required=True, label=u'用户名列表', widget=forms.Textarea)

@render_to('users/bulkadd.html')
@staff_member_required
def bulkadd(request):
    if request.method == 'GET':
        form = UserListForm()
        return { 'form': form }
    elif request.method == 'POST':
        form = UserListForm(request.POST)
        if form.is_valid():
            create_users_from_list(form.cleaned_data['text'])
            return HttpResponseRedirect(reverse('admin:auth_user_changelist'))
        else:
            return { 'form': form }

