from django.contrib import admin
from .models import Question, Quiz, Track, Tag, UserProfile, UserTrack, UserQuizRecord

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    fields = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = ('name',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fields = ('question', 'question_image', 'option', 'description', 'answer', 'tag')
    list_display = ('question', 'option', 'description', 'answer','created_on')
    empty_value_display = '-empty-'

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    fields = ('title', 'track', 'tag', 'description', 'question', 'time')
    list_display = ('title', 'track', 'description', 'time', 'created_on')
    empty_value_display = '-empty-'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    fields = ('user', 'photo', 'bio', 'state', 'college', 'passout', 'birth_date')
    list_display = ('user', 'photo', 'bio', 'state', 'college', 'passout', 'birth_date')
    empty_value_display = '-empty-'

@admin.register(UserTrack)
class UserTrackAdmin(admin.ModelAdmin):
    fields = ('user', 'tracks')
    empty_value_display = '-empty-'

@admin.register(UserQuizRecord)
class UserQuizRecordAdmin(admin.ModelAdmin):
    fields = ('user', 'quiz', 'score')
    list_display = ('user', 'quiz', 'score')
    empty_value_display = '-empty-'

    