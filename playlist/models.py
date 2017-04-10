from django.db import models
from account import models as AccountModels


class Songs(models.Model):
	id = models.AutoField(primary_key = True)
	timestamp = models.DateTimeField(auto_now_add = True)
	user = models.ForeignKey(AccountModels.CustomUser)
	title = models.CharField(max_length = 100)
	url = models.CharField(max_length = 10000)
