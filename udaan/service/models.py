from django.db import models
from accounts.models import CustomUser
from business.models import Skills


# Create your models here.
class Service(models.Model):
    STATUS_CHOICES = [
        ("1", "pending"),
        ("2", "accept"),
        ("3", "decline"),
    ]
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skills, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="1")
    is_completed = models.BooleanField(default=False)
    is_rated = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)+') '+str(self.customer)+' - '+str(self.skill.user)+' - '+str(self.skill.skill_name)

class Rating(models.Model):
    STAR_CHOICES = [
        ("1", "1 star"),
        ("2", "2 star"),
        ("3", "3 star"),
        ("4", "4 star"),
        ("5", "5 star"),
    ]
    service = models.OneToOneField(Service, on_delete=models.CASCADE)
    star = models.IntegerField(default="1")
    comment = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.id)+') '+str(self.service.customer)+' - '+str(self.service.skill.user)+' - '+str(self.service.skill.skill_name)+' - '+str(self.star)
