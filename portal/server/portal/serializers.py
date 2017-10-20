from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from allauth.socialaccount.models import SocialAccount

from .models import Track, Tag, Question, Quiz, UserProfile, UserQuizRecord, Contribution, Feedback
 
 
class UserSerializer(serializers.ModelSerializer):
    def to_representation(self, obj):
        rep = super(UserSerializer, self).to_representation(obj)
        for field in self.fields:
            try:
                if rep[field] is None:
                    rep[field]=""
            except:
                pass
        return rep

    class Meta:
        model = User
        fields = ('id','password', 'first_name', 'last_name', 'email', 'username') # id required in profile view
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('is_staff', 'is_superuser', 'is_active', 'date_joined',)
 
    def create(self, validated_data):
        user = User(email=validated_data['email'], 
        username=validated_data['username'],
        first_name=validated_data.get('first_name'),
        last_name=validated_data.get('last_name'),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self, instance, validated_data):
        instance.username=validated_data.get('username',instance.username)
        instance.first_name=validated_data.get('first_name',instance.first_name)
        instance.last_name=validated_data.get('last_name',instance.last_name)
        instance.set_password(validated_data.get('password',instance.password))
        instance.save()
        return instance

class UserProfileSerializer(serializers.ModelSerializer):
    def to_representation(self, obj):
        rep = super(UserProfileSerializer, self).to_representation(obj)
        rep['user'] = UserSerializer(obj.user).data
        try:
            _social_account = SocialAccount.objects.get(user = obj.user)
            rep['social_site'] = _social_account.provider
            rep['social_id']= _social_account.uid
        except:
            pass
        for field in self.fields:
            try:
                if rep[field] is None:
                    rep[field]=""
            except:
                pass
        return rep

    class Meta:
        model = UserProfile
        fields = ('user','photo','bio','birth_date','state','college','passout')
        read_only_fields = ('user',)

class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ('id','name',)
        read_only_fields = ('id',)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id','name',)
        read_only_fields = ('id',)


class QuestionSerializer(serializers.ModelSerializer):
    # tag = TagSerializer(many=True)
    def to_representation(self, obj):
        rep = super(QuestionSerializer, self).to_representation(obj)
        rep['tag'] = []
        for i in obj.tag.all():
            rep['tag'].append(TagSerializer(i).data)
        if rep["description"] is None:
            rep["description"] = ""
        if rep["question_image"] is None:
            rep["question_image"] = ""
        return rep
    
    def to_internal_value(self,rep):
        try:
            rep['tag'] = [ Tag.objects.get(id=i.get('id')) for i in rep.get('tag')]
        except:
            pass
        return rep

    class Meta:
        model = Question
        fields = ('id', 'question', 'question_image', 'option', 'answer', 'description', 'tag')
        read_only_fields = ('id', 'created_on',)

class QuizSerializer(serializers.ModelSerializer):
    def to_representation(self, obj):
        rep = super(QuizSerializer, self).to_representation(obj)
        rep['tag'] = []
        for i in obj.tag.all():
            rep['tag'].append(TagSerializer(i).data)
        rep['question'] = []
        for i in obj.question.all():
            rep['question'].append(QuestionSerializer(i).data)
        rep['track'] = TrackSerializer(obj.track).data
        rep['total'] = len(rep['question'])
        return rep
    
    def to_internal_value(self,rep):
        try:
            rep['track'] = Track.objects.get(id=rep.get('track').get('id'))
        except:
            pass
        try:
            rep['tag'] = [ Tag.objects.get(id=i.get('id')) for i in rep.get('tag')]
        except:
            pass
        try:
            rep['question'] = [ Question.objects.get(id=i.get('id')) for i in rep.get('question')]
        except:
            pass
        return rep

    class Meta:
        model = Quiz
        fields = ('id','title','track','tag','description','question','time')
        read_only_fields = ('id','created_on','modified_on')

class UserQuizRecordSerializer(serializers.ModelSerializer):
    def to_representation(self, obj):
        rep = super(UserQuizRecordSerializer, self).to_representation(obj)
        rep['profile'] = UserProfileSerializer(UserProfile.objects.get(user=obj.user)).data
        rep['quiz'] = QuizSerializer(Quiz.objects.get(id=rep['quiz'])).data
        return rep

    class Meta:
        model = UserQuizRecord
        fields = ('user', 'quiz','score')
        validators = [
            UniqueTogetherValidator(
                queryset = UserQuizRecord.objects.all(),
                fields = ('user','quiz')
            )
        ]

class ContributionSerializer(serializers.ModelSerializer):
    def to_representation(self, obj):
        rep = super(ContributionSerializer, self).to_representation(obj)
        rep['profile'] = UserProfileSerializer(UserProfile.objects.get(user=obj.user)).data
        return rep
    class Meta:
        model = Contribution
        fields = ('id','user','question','feedback','points','modified_on')
        read_only_fields = ('id','modified_on')

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('id','user','content','created_on')
        read_only_fields = ('id','created_on')