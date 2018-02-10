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
    path('add/',views.event_add,name='add-event'),

    path('eventdetail/',views.event_detail,name='event-detail'),
    path('eventdetail/owner/',views.event_detail_owner,name='event-detail-owner'),
    path('eventdetail/vendor/',views.event_detail_vendor,name='event-detail-vendor'),
    path('eventdetail/guest/',views.event_detail_guest,name='event-detail-guest'),

    path('inviteowner/',views.inviteowner,name='invite'),
    path('invitevendor/',views.invitevendor,name='invite'),
    path('inviteguest/',views.inviteguest,name='invite'),

    path('addmultichoicequestion/',views.addmultichoicequestion,name='addmcq'),
    path('addtextquestion/',views.addtextquestion,name='addtq'),
    path('editmultichoicequestion/',views.editmultichoicequestion,name='editmcq'),
    path('editsinglechoicequestion/',views.editsinglechoicequestion,name='editscq'),
    path('modifyevent/',views.editevent,name='edite'),
    path('modifychoice/',views.modifychoice,name='modifychoice'),
    path('modifytext/',views.modifytext,name='modifytext'),
    path('modifychoicequestion/',views.modifychoicequestion,name='modifychoicequestion'),

    path('allvendor/',views.allvendor,name='allvendor'),
    path('setvendorauthority/',views.setvendorauthority,name='setvendorauthority'),  
    path('finalization/',views.finalization,name='finalization'), 
]
"""
    path('editquestion/',views.editQuestion,name='question'),
    path('addquestion/',views.addQuestion,name='addquestion'),
    path('add_one/',views.addMultiple,name='add_one'),
    path('add_two/',views.addText,name='add_two'),
    path('add_option/',views.addOption,name='add_option'),
    path('addoptionA/',views.addOptionA,name='add_optionA'),
    path('addmultiplequestion/',views.addMultipleChoice,name='add_multiple'),
"""