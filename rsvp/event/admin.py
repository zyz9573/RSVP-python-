from django.contrib import admin
from .models import Event,questionnaire,question,choicequestion,nonchoicequestion,choice,answersheet,answer,singlechoiceanswer,multichoiceanswer,textanswer#Question,QuestionMultiple

# Register your models here.

admin.site.register(Event)
admin.site.register(questionnaire)
#admin.site.register(question)
admin.site.register(choicequestion)
admin.site.register(nonchoicequestion)
admin.site.register(choice)
admin.site.register(answersheet)
#admin.site.register(answer)
admin.site.register(singlechoiceanswer)
admin.site.register(multichoiceanswer)
admin.site.register(textanswer)
"""
admin.site.register(Question)
admin.site.register(QuestionMultiple)
"""