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
from .import models, forms
from playlist import models as PlaylistModels


@login_required
def home(request):
	songs_list = PlaylistModels.Songs.objects.filter(user = request.user).order_by('-timestamp')
	return HttpResponse(render(request, 'account/homepage.html', {'songs_list' : songs_list}))



@login_required
def logout(request):
	auth_logout(request)
	return redirect(reverse('root'))



@csrf_exempt
@require_http_methods(['GET', 'POST'])
def root(request):
	if request.user.is_authenticated():
		return redirect(reverse('home'))

	if request.method == 'GET':
		form = forms.LoginForm()
		return HttpResponse(render(request, 'account/login-form.html', {'form' : form}))

	form = forms.LoginForm(request.POST)

	if not form.is_valid():
		return HttpResponse(render(request, 'account/login-form.html', {'form' : form}))

	username = request.POST.get('username')
	password = request.POST.get('password')
	user = authenticate(username = username, password = password)

	if not user:
		return HttpResponse(render(request, 'account/login-form.html', {'form' : form}))

	auth_login(request, user)
	return redirect(reverse('home'))



@require_http_methods(['GET', 'POST'])
def signup(request):
	if request.user.is_authenticated():
		return redirect(reverse('home'))

	if request.method == 'GET':
		form = forms.SignupForm()
		return HttpResponse(render(request, 'account/signup-form.html', {'form' : form}))

	form = forms.SignupForm(request.POST)

	if not form.is_valid():
		return HttpResponse(render(request, 'account/signup-form.html', {'form' : form}))

	username = form.cleaned_data['username']
	password = form.cleaned_data['password']
	email = form.cleaned_data['email']

	user = models.CustomUser(username = username, email = email)
	user.set_password(password)
	user.save()

	otp = models.createOTP(user, 'AA')

	subject = 'Verify your account'
	sender = settings.EMAIL_HOST_USER
	recipient_email = email
	link = 'teamdefianzracing.in:8000/account/confirm/AA/' + username + '/' + str(user.id) + '/' + str(otp)
	content = loader.render_to_string('account/sentMail-aa.html', {'link' : link})

	message = EmailMultiAlternatives(subject, content, sender, [recipient_email])
	message.send()

	return HttpResponse(render(request, 'common/message.html', {'message' : 'Go to your email to verify your account.'}))



def confirm(request, purpose, username, userID, code):
	if request.user.is_authenticated():
		return redirect(reverse('home'))

	user = models.CustomUser.objects.get(username = username)
	otpObject = models.OTP.objects.get(code = code)

	if not user or not otpObject or int(user.id) != int(userID) or otpObject.user != user:
		return HttpResponse(render(request, 'common/message.html', {'message' : 'Trying to access something that does not exist.'}))

	if otpObject.purpose == 'AA':
		user.is_active = True
		user.save()
		otpObject.delete()
		return HttpResponse(render(request, 'common/message.html', {'message' : 'Verification Complete.'}))

	else:
		if request.method == 'GET':
			form = forms.ResetPasswordForm()
			context = {
				'form' : form,
				'purpose' : purpose,
				'username' : username,
				'userID' : userID,
				'code' : code			
			}
			return HttpResponse(render(request, 'account/reset-password.html', context))

		form = forms.ResetPasswordForm(request.POST)

		if not form.is_valid():
			context = {
				'form' : form,
				'purpose' : purpose,
				'username' : username,
				'userID' : userID,
				'code' : code			
			}
			return HttpResponse(render(request, 'account/reset-password.html', context))

		targetUser = models.CustomUser.objects.get(username = username)
		targetUser.set_password(request.POST.get('password'))
		targetUser.save()
		otpObject = models.OTP.objects.get(user = targetUser)
		otpObject.delete()
		return HttpResponse(render(request, 'common/message.html', {'message' : 'Password updated successfully.'}))



@require_http_methods(['GET', 'POST'])
def forgot_password(request):
	if request.user.is_authenticated():
			return redirect(reverse('home'))

	if request.method == 'GET':
		form = forms.UsernameForm()
		return HttpResponse(render(request, 'account/forgot-password.html', {'form' : form}))

	form = forms.UsernameForm(request.POST)

	if not form.is_valid():
		return HttpResponse(render(request, 'account/forgot-password.html', {'form' : form}))

	targetUser = models.CustomUser.objects.get(username = form.cleaned_data['username'])
	recipient_email = targetUser.email
	sender = settings.EMAIL_HOST_USER
	subject = 'Forgot Password'

	otp = models.createOTP(targetUser, 'FP')
	link = 'teamdefianzracing.in:8000/account/confirm/FP/' + targetUser.username + '/' + str(targetUser.id) + '/' + str(otp)
	content = text_message = loader.render_to_string('account/sentMail-fp.html', {'link' : link})
	message = EmailMultiAlternatives(subject, content, sender, [recipient_email])
	message.send()

	return HttpResponse(render(request, 'common/message.html', {'message' : 'Go to your email to reset your password.'}))

























