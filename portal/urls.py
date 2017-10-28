"""portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework import routers
from . import views
from rest_framework.authtoken import views as rviews
admin.autodiscover()
router = routers.DefaultRouter()
router.register(r'accounts', views.UserView, 'list')
router.register(r'tracks', viewset=views.TrackView)
router.register(r'tags', viewset=views.TagView)
router.register(r'questions', viewset=views.QuestionView)
router.register(r'quizzes', viewset=views.QuizView)
router.register(r'users', viewset=views.UserView)
router.register(r'userprofile', viewset=views.UserProfileView)
router.register(r'userquizrecord',viewset=views.UserQuizRecordView)
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.home,name='home'),    
    url(r'^account/', include('allauth.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^profile/@(?P<user>[a-zA-Z0-9]+)',views.profile, name='profile'),
    url(r'^quiz/(?P<quiz>[0-9]+)$',views.quiz,name="quiz"),
    url(r'^quiz/(?P<quiz>[0-9]+)/leaderboard',views.leaderboard,name="leaderboard"),
    url(r'^tracks/$',views.tracks,name="tracks"),
    url(r'^tracks/(?P<track>[0-9]+)',views.quizlist,name="quizlist"),
    url(r'^about/',views.about,name="about"),
    url(r'^social/link',views.getsocial,name="social-link"),
    url(r'^contribute/$',views.contribute,name="contribute"),
    url(r'^explore/$',views.explore,name="explore"),
    url(r'^contributors/$',views.contributors,name="contributors"),
    url(r'^contribute/question$',views.contribute_question,name="contribute_question"),
    url(r'^terms/$',views.terms,name="terms"),
    url(r'^automate/$',views.quiz_automate,name="questionsubmit"),
    url(r'^contests/$',views.contests,name="contests"),  
]
   
urlpatterns += [
    url(r'^api-token-auth/', rviews.obtain_auth_token)
]
