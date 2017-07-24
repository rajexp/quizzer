from django.contrib.auth.models import User
from django.shortcuts import render
from django.db.models import Q 
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from .permissions import IsStaffOrTargetUser, IsAdminOrIsSelf
from .serializers import TrackSerializer, TagSerializer, QuizSerializer, \
QuestionSerializer, UserSerializer, UserQuizRecordSerializer
from .models import Track, Tag, Question, Quiz, UserProfile, UserQuizRecord
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
import random

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# @api_view(['GET','POST'])
def profile(request):
    profile = UserProfile.objects.get(user=request.user)
    print(profile)
    return render(request,'profile.html',context={'user':request.user,'user.profile':profile})

def quiz(request):
    return render(request,'quiz.html')

def about(request):
    return render(request,'about.html')

class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    model = User
    queryset = User.objects.all()
 
    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (AllowAny() if self.request.method =='POST'
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
                else IsAuthenticated()),
    @list_route()
    def tracks(self, request):
        track = self.request.query_params.get('track',None)
        track = Track.objects.get(name=track)
        quizzes = Quiz.objects.filter(track=track)
        try:
            quiz = quizzes[random.randint(0,len(quizzes)-1)]
        except:
            quiz = Quiz.objects.get()
        serializer = self.get_serializer(quiz)
        print(serializer.data)
        return Response(serializer.data)

    @detail_route(methods=['get','post'], permission_classes=[IsAuthenticated], url_path='rank')
    def rank(self, request, pk=None):
        request.data.quiz = Quiz.objects.get(pk=pk)
        serializer = UserQuizRecordSerializer(data = request.data )
        if serializer.is_valid():
            serializer.save(user=request.user)
            rank = UserQuizRecord.objects.filter(Q(quiz=request.data.quiz.id),Q(score__gte=request.data.get('score'))).count()
            return Response({'rank':rank}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)