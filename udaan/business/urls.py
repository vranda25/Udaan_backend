from django.urls import path
from .views import *

urlpatterns = [
    path('profile/', ProfileViewForBusiness.as_view()),      #business can get and make its profile+user
    path('skills/', SkillViewForBusiness.as_view()),         #business can make skill and get whole profile+skill+user
    path('profile/all/', ProfileViewForCustomer.as_view()),  #customer can view profile+user along with names of skills for that user
    path('skills/all/', SkillViewForCustomer.as_view()),                            #all skills (only skills without profile)
    path('skills/particular/', ParticularBusinessSkillViewForCustomer.as_view()),   #all skills of a particular user given user id (only skill)
    path('status/', ServicesStatus.as_view()),   #all skills of a particular user given user id (only skill)
]