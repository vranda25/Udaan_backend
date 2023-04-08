from django.urls import path
from .views import *

urlpatterns = [
    path('post/', ServiceView.as_view()),              #customer can post service and get list of all his booking services
    path('status/', StatusView.as_view()),              #business can change status of service
    path('completed/', CompletedView.as_view()),        #customer check is_completed only if status is accepted and increases job_completed for a particular business
    path('rating/', RatingView.as_view()),                                      #takes service id, post and get rating
    path('rating/all/', AllRatingOfParticularBusiness.as_view()),               #takes user id, get all ratings of a particular business
    path('history/all/', ServicesCompletedByParticularBusiness.as_view()),               #takes user id, get list of past services customer_name, skill_name, rating
]