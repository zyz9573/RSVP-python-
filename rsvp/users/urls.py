from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('register/',views.register,name='register'),
    path('<int:pk>',views.detail,name='detail')
]