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
    option = ArrayField(models.CharField(max_length=250, blank=False, null=False),size=4)
    answer = models.IntegerField(choices=((1,'1'),(2,'2'),(3,'3'),(4,'4')))
    description = models.TextField(blank=True,null=True)
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

    def __str__(self):
        return self.user.first_name+' '+self.user.last_name+' : '+self.tracks.name

class UserQuizRecord(models.Model):
    user = models.ForeignKey(User)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='userrecord')
    score = models.FloatField(default=0.00)

class Feedback(models.Model):
    user = models.ForeignKey(User) 
    content = models.TextField(max_length=500)
    created_on = models.DateTimeField(editable=False)

    def __str(self):
        return self.user + '...' + self.content[:len(self.content) if len(self.content)<10 else 10]
        
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_on = timezone.now()
        return super(Feedback, self).save(*args, **kwargs)

class Contribution(models.Model):
    user = models.ForeignKey(User)
    question = models.IntegerField(default=0)
    feedback = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    modified_on = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        self.modified_on = timezone.now()
        return super(Contribution, self).save(*args, **kwargs)
        
    def __str(self):
        return self.user+'_'+self.points

# 'BIRTHDAY','CONTEST','TRENDING','QUIZ','CHALLENGE','POINTS','FOLLOW','NEW_CONTENT'
class Notification(models.Model):
    category = models.CharField(max_length=20,choices=(('BIRTHDAY','BIRTHDAY'), ('CONTEST','CONTEST'), ('TRENDING','TRENDING'), ('QUIZ','QUIZ'), ('CHALLENGE','CHALLENGE'), ('POINTS','POINTS'), ('FOLLOW','FOLLOW'), ('NEW_CONTENT','NEW_CONTENT'), ('UNLOCK','UNLOCK')))
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    id_first = models.CharField(max_length=100)
    time = models.DateTimeField(default=timezone.now)
    score = models.CharField(max_length=10)
    name_second = models.CharField(max_length=50)
    id_second = models.CharField(max_length=100)
    created_on  = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_on = timezone.now()
        return super(Notification, self).save(*args, **kwargs)

class Contest(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    quiz = models.ForeignKey(Quiz)
    datetime = models.DateTimeField(default=timezone.now)
    published = models.BooleanField(default=False)


# {
#     'name':'Day 1 Classic', //CONTEST
#     'id':'13411',
#     'time':'12/01/23:9:00:45',
# }
# {
#     'name':'India Quiz I', //TRENDING
#     'id':'23423',
# }
# {   
#     'name':'Some Quiz', //QUIZ
#     'id':'23413',
#     'score':'90',
# }
# {
#     'name':'SOme User', //CHALLENGE
#     'id':'8741345',
#     'state':'Win/Lost',
#     'quiz':'India Quiz I',
#     'id': '875385'
# }
# {
#     'name':'India Quiz I', //POINTS
#     'id':'8741345',
#     'score':'10'
# }
# {
#     'name':'General Quiz', //FOLLOW
#     'id':'8741345',
# }
# {
#     'name':'India Quiz I', //NEW_CONTENT
#     'id':'8741345',
#     'type':'Quiz/Feature'
# }
# {
#     'name':'Create Quiz', //UNLOCK
#     'id':'8741345'
# }



