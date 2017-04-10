from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, get_object_or_404, redirect, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_GET, require_POST,require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.http import JsonResponse
from django.template import Context, Template
from .import models


@login_required
@csrf_exempt
def add_song(request):
	url = request.POST.get('url')
	title = request.POST.get('title')

	new_object = models.Songs.objects.create(user = request.user, title = title, url = url)
	new_object.save()
	return HttpResponse(redirect(reverse('home')))



@login_required
@csrf_exempt
def remove_song(request):
	title = request.POST.get('title')
	url = request.POST.get('url');
	song = models.Songs.objects.filter(user = request.user, title = title, url = url)

	if len(song) > 0:
		song[0].delete()

	return HttpResponse(redirect(reverse('home')))