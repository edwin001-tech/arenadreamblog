from django.urls import path
from .views import *

urlpatterns=[
path('email-signup/', email_list_signup, name='email-list-signup'),
]