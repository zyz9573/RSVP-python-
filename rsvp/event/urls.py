from django.urls import path
from . import views

app_name = 'event'

urlpatterns = [
    path('', views.IndexView.as_view(),name='index'),
    path('<int:pk>',views.DetailView.as_view(),name='detail'),
    path('<int:pk>/answer',views.answer,name='answer'),
    #path('event/add/',views.EventCreate.as_view(),name='event-add'),
    path('event/<int:pk>',views.EventUpdate.as_view(),name='event-update'),
    path('event/<int:pk>/delete/',views.EventDelete.as_view(),name='event-delete'),
    path('user/',views.event_view,name='user-homepage'),
    path('event/add/',views.event_add,name='add-event'),
    path('eventdetail/',views.event_detail,name='event-detail'),
    path('editquestion/',views.editQuestion,name='question'),
    path('addquestion/',views.addQuestion,name='addquestion'),
    path('add_one/',views.addMultiple,name='add_one'),
    path('add_two/',views.addText,name='add_two'),
    path('add_option/',views.addOption,name='add_option'),
    path('addoptionA/',views.addOptionA,name='add_optionA'),
    path('addmultiplequestion/',views.addMultipleChoice,name='add_multiple'),
    path('inviteowner/',views.inviteowner,name='invite'),
    path('invitevendor/',views.invitevendor,name='invite'),
    path('inviteguest/',views.inviteguest,name='invite'),
]
