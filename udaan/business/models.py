from django.db import models
from accounts.models import CustomUser
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    business_name = models.CharField(max_length=100, null=True, blank=True)
    contact_no = models.CharField(max_length=10, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    profile_image = models.ImageField(upload_to='business/images/user', blank=True)
    instagram = models.CharField(max_length=200, blank=True, null=True)
    facebook = models.CharField(max_length=200, blank=True, null=True)
    youtube = models.CharField(max_length=200, blank=True, null=True)
    jobs_completed = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)+') '+str(self.user.email)

class Skills(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=50, null=True, blank=True)
    skill_description = models.CharField(max_length=500, null=True, blank=True)
    remuneration = models.CharField(max_length=100, null=True, blank=True)
    skill_image = models.ImageField(upload_to='business/images/skills', blank=True)

    def __str__(self):
        return str(self.id)+') '+str(self.user.email)+' : '+str(self.skill_name)

