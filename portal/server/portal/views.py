from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .permissions import IsStaffOrTargetUser
from .serializers import TrackSerializer, TagSerializer, QuizSerializer, \
QuestionSerializer, UserSerializer
from .models import Track, Tag, Question, Quiz
 
 
class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    model = User
    queryset = User.objects.all()
 
    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (AllowAny() if self.request.method == 'POST'
                else IsStaffOrTargetUser()),

class TrackView(viewsets.ModelViewSet):
    serializer_class = TrackSerializer
    queryset = Track.objects.all()
    model = Track

    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (AllowAny() if self.request.method == 'GET'
                else IsStaffOrTargetUser()),

class TagView(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    model = Tag

    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (AllowAny() if self.request.method == 'GET'
                else IsStaffOrTargetUser()),

class QuestionView(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    model = Question

    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (AllowAny() if self.request.method == 'GET'
                else IsStaffOrTargetUser()),

class QuizView(viewsets.ModelViewSet):
    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()
    model = Quiz

    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (AllowAny() if self.request.method in ['GET']
                else IsStaffOrTargetUser()),

# class 