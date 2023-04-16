from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Instructor, MyClass, Student, Subject, Score, User, Comment, Forum


def get_avatar(self, obj):
    request = self.context['request']
    if obj.avatar.name.startswith('static/'):
        path = "/%s" % obj.avatar.name
    else:
        path = '/static/%s' % (obj.avatar)
    return request.build_absolute_uri(path)

class InstructorSerializer(ModelSerializer):
    avatar = SerializerMethodField(source='image')
    def get_avatar(self, obj):
        return get_avatar(self,obj)
    class Meta:
        model = Instructor
        fields = ['fullname','major','avatar']

class ClassSerializer(ModelSerializer):

    class Meta:
        model = MyClass
        fields = ['name', 'major']

class StudentSerializer(ModelSerializer):
    avatar = SerializerMethodField(source='image')
    myclass = ClassSerializer()
    def get_avatar(self, obj):
        return get_avatar(self,obj)
    class Meta:
        model = Student
        fields = ['fullname', 'myclass' ,'avatar']

class UserSerializer(ModelSerializer):
    instructors = InstructorSerializer()
    students = StudentSerializer()
    class Meta:
        model = User
        fields = ['instructors', 'students']
    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(user.password)
        user.save()
        return user

class SubjectSerializer(ModelSerializer):
    instructor = InstructorSerializer()
    myclass = ClassSerializer
    class Meta:
        model = Subject
        fields = ['name', 'start_time', 'end_time' ,'instructor', 'myclass']

class ScoreSerializer(ModelSerializer):
    subject = SubjectSerializer()
    student = StudentSerializer()
    class Meta:
        model = Score
        fields = ['subject', 'student', 'point', 'score_type', 'ratio']

class ForumSerializer(ModelSerializer):
    class Meta:
        model = Forum
        fields = ['content', 'creator']

class CommentSerializer(ModelSerializer):
    creator = UserSerializer()
    class Meta:
        model = Comment
        fields = ['creator', 'content']