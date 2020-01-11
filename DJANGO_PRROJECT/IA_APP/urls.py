from django.urls import path
from . import views
import aiml
urlpatterns=[
    path('',views.index , name = 'home-page'),
    path('bot_response/',views.bot_response , name = 'bot_response'),
]