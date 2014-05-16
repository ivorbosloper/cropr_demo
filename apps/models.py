from django.db import models

class AccessToken(models.Model):
    user = models.OneToOneField('auth.User', related_name='access_token')
    access_token = models.CharField(max_length=100)


