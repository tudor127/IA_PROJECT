from django.urls import path
from . import views
import aiml
urlpatterns=[
    path('',views.index ),
    path('bot_response/',views.bot_response ),
    path('get_category/',views.get_category),
    path('get_aiml/',views.get_aiml),
    path('administration/',views.administration ),
    path('login/', views.login),
    path('logout/', views.logout),
    path('toggle_category/',views.toggle_category)
]