from django import forms
from .import models



class LoginForm(forms.Form):
	username = forms.CharField(max_length = 35)
	password = forms.CharField(max_length = 35, widget = forms.PasswordInput)

	def clean_username(self):
		username = self.cleaned_data['username']
		if models.CustomUser.objects.filter(username = username).count() != 1:
			raise forms.ValidationError('No such user exists.')
		return username



class ResetPasswordForm(forms.Form):
	password = forms.CharField(max_length = 35, widget = forms.PasswordInput)
	confirm_password = forms.CharField(max_length = 35, widget = forms.PasswordInput)

	def clean(self):
		password = self.cleaned_data['password']
		confirm_password = self.cleaned_data.get('confirm_password')

		if password != confirm_password:
			raise forms.ValidationError('Two passwords do not match')
		return password



class UsernameForm(forms.Form):
	username = forms.CharField(max_length = 35)

	def clean_username(self):
		user = models.CustomUser.objects.get(username = self.cleaned_data['username'])

		if not user:
			raise forms.ValidationError('No such user exists')

		return self.cleaned_data['username']


class SignupForm(forms.Form):
	username = forms.CharField(max_length = 35)
	email = forms.CharField(max_length = 100)
	password = forms.CharField(max_length = 35, widget = forms.PasswordInput)
	confirm_password = forms.CharField(max_length = 35, widget = forms.PasswordInput)

	def clean_username(self):
		username = self.cleaned_data['username']
		if models.CustomUser.objects.filter(username = username).count() != 0:
			raise forms.ValidationError('Username already taken')
		return username

	def clean_email(self):
		email = self.cleaned_data['email']
		if models.CustomUser.objects.filter(email = email).count() != 0:
			raise forms.ValidationError('Email already registered')
		return email

	def clean_password(self):
		password = self.cleaned_data['password']
		confirm_password = self.cleaned_data['confirm_password']

		if password != confirm_password:
			raise forms.ValidationError('Two passwords do not match')
		return password