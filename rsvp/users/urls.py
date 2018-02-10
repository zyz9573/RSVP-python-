from django.urls import path
from . import views
import django
app_name = 'users'
urlpatterns = [
    path('register/',views.register,name='register'),
    path('realuser/',views.detail,name='detail'),
    path('static/<path>',django.views.static.serve)
]