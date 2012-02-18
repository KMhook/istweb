# encoding: utf-8

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from annoying.decorators import render_to
from models import Contact, ContactUploadForm, ContactEditForm
from extractor import extract_contact_info_from_html


def contacts_list(request):
    contacts = Contact.objects.filter(fullname__isnull=False)
    return { 'contacts_list': contacts }


@render_to('contacts/index.html')
def index(request):
    # TODO: pagination
    contacts = Contact.objects.all()

    return { 'contacts': contacts }


@render_to('contacts/upload.html')
def upload(request):
    if request.method == 'GET':
        form = ContactUploadForm()
    elif request.method == 'POST':
        form = ContactUploadForm(request.POST, request.FILES)

        if form.is_valid():
            user = request.user
            contact = Contact.objects.by_user(user) or Contact(user=user)
            contact.html = request.FILES['html']
            contact.save()

            request.session['contact_info'] = extract_contact_info_from_html(contact.html)

            messages.success(request, u'个人页面已成功上传')
            return HttpResponseRedirect(reverse('contacts_edit'))

    return { 'form': form }


@render_to('contacts/edit.html')
def edit(request):
    user = request.user
    contact = Contact.objects.by_user(user)

    if not contact:
        messages.error(request, u'请先上传个人页面')
        return HttpResponseRedirect(reverse('contacts_upload'))

    if request.method == 'GET':
        if request.session.get('contact_info'):
            contact_info = request.session.pop('contact_info')
            contact.fullname = contact_info.get('fullname')
            contact.email = contact_info.get('email')
            contact.phone = contact_info.get('phone')
            contact.qq = contact_info.get('qq')
            contact.douban_id = contact_info.get('douban_id')

        form = ContactEditForm(instance=contact)
    elif request.method == 'POST':
        form = ContactEditForm(request.POST, instance=contact)

        if form.is_valid():
            form.save()
            messages.success(request, u'个人资料已更新')
            return HttpResponseRedirect(reverse('root'))

    return { 'form': form }


@render_to('contacts/me.html')
def me(request):
    return { 'contact': Contact.objects.by_user(request.user) }

def show(request, username):
    user = get_object_or_404(User, username=username)
    contact = Contact.objects.by_user(user)

    if not contact:
        if user == request.user:
            messages.info(request, u'你还没有上传自己的个人页面')
            return HttpResponseRedirect(reverse('contacts_upload'))
        else:
            messages.error(request, u'该用户还没有上传自己的个人页面')
            return HttpResponseRedirect(reverse('root'))

    return HttpResponse(contact.html.chunks())
