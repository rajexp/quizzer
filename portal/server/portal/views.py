from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q 
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from .permissions import IsStaffOrTargetUser, IsAdminOrIsSelf
from .serializers import TrackSerializer, TagSerializer, QuizSerializer, \
QuestionSerializer, UserSerializer, UserProfileSerializer, UserQuizRecordSerializer
from .models import Track, Tag, Question, Quiz, UserProfile, UserQuizRecord
from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from django.core import serializers
import random
import json

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# @api_view(['GET','POST'])
def profile(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request,'profile.html',context={'user':request.user,'user.profile':profile})

def quiz(request,quiz=None):
    _quiz = Quiz.objects.get(id=quiz)
    quiz = QuizSerializer(_quiz)
    return render(request,'quiz.html',context={'quiz':quiz.data})

def tracks(request):
    _tracks = Track.objects.all()
    tracks = TrackSerializer(_tracks,many=True)
    return render(request,'track.html',context={'tracks':tracks.data})

def quizlist(request,track=None):
    print(track)
    _track = Track.objects.get(pk=track)
    _quizzes = Quiz.objects.filter(track=_track)
    quizzes = QuizSerializer(_quizzes,many=True)
    return render(request,'quizlist.html',context={'quizs':quizzes.data})

def about(request):
    return render(request,'about.html')

def getsocial(request):
    fb = SocialAccount.objects.filter(user_id=request.user.id, provider='facebook')
    user_list = User.objects.all()
    user_list = json.loads(serializers.serialize('json',user_list))
    return JsonResponse(user_list,safe=False)
    return JsonResponse({'fb_uid':fb[0].uid})

class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    model = User
    queryset = User.objects.all()
 
    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (AllowAny() if self.request.method =='POST'
                else IsStaffOrTargetUser()),

class UserProfileView(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    model = User
    queryset = User.objects.all()
 
    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (AllowAny() if self.request.method =='POST'
                else IsStaffOrTargetUser()),
    
    @list_route(methods=['get'], url_path='myprofile')
    def myprofile(self, request):
        profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(profile)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

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
            quiz = Quiz.objects.all()[0]
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