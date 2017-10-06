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
def profile(request,user):
    user = User.objects.get(username=user)
    _profile = UserProfile.objects.get(user=user)
    profile = UserProfileSerializer(_profile)
    return render(request,'profile.html',context={'profile':profile.data})

def quiz(request,quiz=None):
    _quiz = Quiz.objects.get(id=quiz)
    quizz = QuizSerializer(_quiz)
    if not request.user.is_authenticated():
        return render(request,'quiz.html',context={'quiz':quizz.data})
    _user = UserProfile.objects.get(user=request.user)
    user = UserProfileSerializer(_user)
    record = dict()
    try:
        _quizrecord = UserQuizRecord.objects.get(user=request.user,quiz=quiz)
        quizrecord = UserQuizRecordSerializer(_quizrecord)
        record['attempted'] = True
        record['record'] = quizrecord.data
    except UserQuizRecord.DoesNotExist:
        record['attempted'] = False
    return render(request,'quiz.html',context={'quiz':quizz.data,"profile":user.data,'record':record})

def tracks(request):
    _tracks = Track.objects.all()
    tracks = TrackSerializer(_tracks,many=True)
    return render(request,'track.html',context={'tracks':tracks.data})

def quizlist(request,track=None):
    _track = Track.objects.get(pk=track)
    _quizzes = Quiz.objects.filter(track=_track) # Optimise only required fields to be sent
    quizzes = QuizSerializer(_quizzes,many=True)
    return render(request,'quizlist.html',context={'quizs':quizzes.data})

def leaderboard(request,quiz=None):
    _quiz = Quiz.objects.get(id = quiz)
    _quizrecord = UserQuizRecord.objects.filter(quiz=_quiz).order_by('-score')
    quizrecord = UserQuizRecordSerializer(_quizrecord,many=True)
    return render(request,'leaderboard.html',context={"leaders":quizrecord.data, "title":_quiz.title})


def about(request):
    return render(request,'about.html')

@api_view(['POST'])
def getsocial(request):
    fb = SocialAccount.objects.filter(user_id=request.data["user"], provider='facebook')
    # fb_uid: False when no social account matches for that user
    if fb:
        return JsonResponse({'fb_uid':fb[0].uid})
    else:
        return JsonResponse({'fb_uid':False})

@api_view(['GET'])
def contribute(request):
    return render(request,'contribute.html')


@api_view(['GET','POST'])
def contribute_question(request):
    if request.method == 'GET':
        return render(request,'question.html')
    elif request.method == 'POST':
        option = list(filter(lambda x: x !="",[request.data.get('opt-a'),request.data.get('opt-b'),request.data.get('opt-c'),request.data.get('opt-d')]))
        tag = request.data.get('tag').split(',')
        tag = [ Tag.objects.filter(name__istartswith=i)[0] if len(Tag.objects.filter(name__istartswith=i)) else None for i in tag ]
        tag = list(filter(lambda x: x is not None,tag))
        data = {'question':request.data.get('question'),'tag':tag,'description':'','answer':request.data.get('answer'),'option':option}
        serializer = QuestionSerializer(data=data)
        if serializer.is_valid():
            print(data)

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
    model = UserProfile
    queryset = UserProfile.objects.all()
 
    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (AllowAny() if self.request.method =='POST'
                else IsStaffOrTargetUser()),
    
    @list_route(methods=['get'], url_path='myprofile')
    def myprofile(self, request):
        profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(profile)
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
    @list_route(methods=['get'], url_path='search')
    def search(self,request,name=None):
        _tags = Tag.objects.filter(name__istartswith=name)
        serializer = TagSerializer(_tags,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

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
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = UserQuizRecordSerializer(data = data )
        if serializer.is_valid():
            serializer.save()
            quiz = UserQuizRecord.objects.filter(Q(quiz=data['quiz']))
            rank = quiz.filter(Q(score__gt=data['score'])).count()+1
            total = quiz.count()
            return Response({'rank':rank,'total':total}, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserQuizRecordView(viewsets.ModelViewSet):
    serializer_class = UserQuizRecordSerializer
    queryset = UserQuizRecord.objects.all()
    model = UserQuizRecord

    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (AllowAny() if self.request.method == 'GET'
                else IsStaffOrTargetUser()),