from django.contrib import admin
from exam.models import Question, QuestionText, Answer, Level, Lang, AnswerText
# Register your models here.

admin.site.register(Question)
admin.site.register(QuestionText)
admin.site.register(Answer)
admin.site.register(Level)
admin.site.register(Lang)
admin.site.register(AnswerText)
