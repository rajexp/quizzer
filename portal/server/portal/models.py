from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.fields import ArrayField

class Tag(models.Model):
    name = models.CharField(max_length = 50, null=False, unique=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    question = models.TextField(blank=False, null=False)
    question_image = models.ImageField(blank=True, null=True, upload_to='question')
    option = ArrayField(models.CharField(max_length=50, blank=False, null=False),size=4)
    answer = models.IntegerField(choices=((1,'1'),(2,'2'),(3,'3'),(4,'4')))
    description = models.TextField(blank=True,null=True )
    tag = models.ManyToManyField(Tag)
    created_on  = models.DateTimeField(default= timezone.now)

    def __str__(self):
        return self.question

class Track(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)

    def __str__(self):
        return self.name

class Quiz(models.Model):
    title = models.TextField(blank=True,null=False )
    track = models.ForeignKey(Track)
    tag = models.ManyToManyField(Tag)
    description = models.TextField(blank=True, )
    question = models.ManyToManyField(Question, related_name="quiz")
    time = models.IntegerField(validators=[MinValueValidator(0)])
    created_on  = models.DateTimeField(editable=False)
    modified_on = models.DateTimeField()

    class Meta:
        index_together = ['title']

    def __str(self):
        return self.title
        
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
    photo = models.ImageField(upload_to='images', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, default='')
    state = models.CharField(max_length=30, blank=True, null=True)
    college = models.CharField(max_length=100, default='', blank=True)
    passout = models.DateField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


class UserTrack(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tracks = models.ForeignKey(Track, related_name='usertrack')

class UserQuizRecord(models.Model):
    user = models.ForeignKey(User)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='userrecord')
    score = models.FloatField(default=0.00)

class Feedback(models.Model):
    user = models.ForeignKey(User) 
    content = models.TextField(max_length=500)
    created_on = models.DateTimeField(editable=False)

    def __str(self):
        return self.user + '...' + self.content[:len(self.content) if len(self.conent)<10 else 10]
        
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_on = timezone.now()
        return super(Feedback, self).save(*args, **kwargs)

class Contribution(models.Model):
    user = models.ForeignKey(User)
    question = models.IntegerField()
    feedback = models.IntegerField()
    points = models.IntegerField()






