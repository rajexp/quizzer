from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

class Tag(models.Model):
    name = models.CharField(max_length = 50)

# class Option(object):
#     def _init__(self, first=None, second=None, third=None, forth=None, answer=None):
#         self.first = first
#         self.second = second
#         self.third = third
#         self.forth = forth
#         self.answer = answer

class Question(models.Model):
    question = models.TextField(blank=False, null=False)
    question_image = models.ImageField(blank=True, null=True, upload_to='question')
    opt_first = models.CharField(max_length=50, blank=False, null=False)
    opt_second = models.CharField(max_length=50, blank=False, null=False)
    opt_third = models.CharField(max_length=50, blank=False, null=False)
    opt_forth = models.CharField(max_length=50, blank=False, null=False)
    answer = models.CharField(max_length=1, choices=(('1','1'),('2','2'),('3','3'),('4','4')))
    description = models.TextField(blank=True,null=True )
    tag = models.ManyToManyField(Tag)
    created_on  = models.DateTimeField(default= timezone.now)

class Track(models.Model):
    name = models.CharField(max_length=50, null=False)

class Quiz(models.Model):
    title = models.TextField(blank=True, )
    track = models.OneToOneField(Track)
    tag = models.ManyToManyField(Tag)
    description = models.TextField(blank=True, )
    question = models.ManyToManyField(Question, related_name="quiz")
    time = models.IntegerField(validators=[MinValueValidator(0)])
    created_on  = models.DateTimeField(editable=False)
    modified_on = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_on = timezone.now()
        self.modified_on = timezone.now()
        return super(Quiz, self).save(*args, **kwargs)

class Comment(models.Model):
    content = models.TextField(blank=False, null=False)
    question = models.ForeignKey(Question, related_name='comment')
    user = models.OneToOneField(User, related_name='comment')
    created_on  = models.DateTimeField(editable=False)
    modified_on = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_on = timezone.now()
        self.modified_on = timezone.now()
        return super(Comment, self).save(*args, **kwargs)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='images', null=True)
    bio = models.TextField(max_length=500, blank=True, default='')
    state = models.CharField(max_length=30, blank=True, null=True)
    college = models.CharField(max_length=100, default='')
    passout = models.DateField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


class UserTrack(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tracks = models.ForeignKey(Track, related_name='usertrack')

class UserQuizRecord(models.Model):
    user = models.OneToOneField(User)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='userrecord')
    score = models.FloatField(default=0.00)






