from django.contrib import admin
from .models import Track, Tag, Question, Quiz

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    fields = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = ('name',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fields = ('question', 'opt_first', 'opt_second', 'opt_third', 'opt_forth', 'answer', 'tag')

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    fields = ('title', 'track', 'tag', 'description', 'question', 'time', 'created_on')
