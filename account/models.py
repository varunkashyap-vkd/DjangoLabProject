from django.db import models
from django.contrib.auth.models import AbstractUser
from random import randint


class CustomUser(AbstractUser):
	pass


class OTP(models.Model):
	user = models.ForeignKey(CustomUser)
	code = models.IntegerField()
	purpose = models.CharField(max_length = 2)

def createOTP(user, purpose):
	alreadyExisting = OTP.objects.filter(user = user)

	for item in alreadyExisting:
		item.delete()

	code = randint(1000000, 9999999)

	while(OTP.objects.filter(code = code).count() > 0):
		code = randint(100000, 999999)

	OTPObject = OTP.objects.create(user = user, purpose = purpose, code = code)
	OTPObject.save()
	return code
