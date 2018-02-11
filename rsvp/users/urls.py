from django.urls import path
from . import views
from django.views import static
app_name = 'users'
urlpatterns = [
    path('register/',views.register,name='register'),
    path('realuser/',views.detail,name='detail'),
    path('static/<path>',static.serve)
]