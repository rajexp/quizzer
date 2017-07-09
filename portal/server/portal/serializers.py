from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Track, Tag, Question, Quiz
 
 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'first_name', 'last_name', 'email', 'username')
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
        return rep
    
    def to_internal_value(self,rep):
        try:
            rep['tag'] = [ Tag.objects.get(id=i.get('id')) for i in rep.get('tag')]
        except:
            pass
        return rep

    class Meta:
        model = Question
        fields = ('id', 'question', 'question_image', 'opt_first', 'opt_second', 'opt_third', 'opt_forth', 'answer', 'description', 'tag')
        read_only_fields = ('id', 'created_on',)
    
    # def create(self, validated_data):
    #     tags = validated_data.pop('tag')
    #     question = Question.objects.create(**validated_data)
    #     for tag in tags:
    #         tag, created = Tag.objects.get_or_create(name=tag['name'])
    #         question.tag.add(tag)
    #     return question

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
        fields = ('title','track','tag','description','question','time')
        read_only_fields = ('created_on','modified_on')
    
    # def create(self, validated_data):
    #     questions = validated_data.pop('question')
    #     tags = validated_data.pop('tag')
    #     tracks = validated_data.pop('track')
    #     quiz = Quiz.objects.create(**validated_data)

    #     for question in questions:
    #         question, created = Question.objects.get_or_create(id=question['id'])
    #         recipe.ingredients.add(ingredient)
    #     return recipe