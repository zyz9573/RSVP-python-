from django.contrib import admin
from .models import Event,Question,QuestionMultiple,Options

# Register your models here.

admin.site.register(Event)
admin.site.register(Question)
admin.site.register(QuestionMultiple)
admin.site.register(Options)
