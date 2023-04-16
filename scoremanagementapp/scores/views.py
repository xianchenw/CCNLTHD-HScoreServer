from django.db import IntegrityError
from django.shortcuts import render
from rest_framework import viewsets, permissions, authentication
from rest_framework.views import APIView, Response, status
from .models import Student, Score, Subject, Instructor, MyClass, Comment, Forum
from .serializers import StudentSerializer ,ScoreSerializer, ClassSerializer, InstructorSerializer, SubjectSerializer, ForumSerializer, CommentSerializer
# Create your views here.
from django.http import Http404, HttpResponse

def index(request):
    return HttpResponse("Score Management App")


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    permission_classes = [permissions.IsAuthenticated]

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.AllowAny]

class ClassViewSet(viewsets.ModelViewSet):
    queryset = MyClass.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [permissions.IsAuthenticated]

class InstructorViewSet(viewsets.ModelViewSet):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
    permission_classes = [permissions.IsAuthenticated]

class CommentAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    def get(self, request, forum_id):
        comments = Comment.objects.filter(forum_id=forum_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data,
            status=status.HTTP_200_OK)
    def post(self, request, forum_id):
        content = request.data.get('content')
        if content is not None:
            try:
                c = Comment.objects.create(content=content,
                    user=request.user,
                    forum_id=forum_id)
            except IntegrityError:
                err_msg = "Forum does not exist!"
            else:
                return Response(CommentSerializer(c).data,
                    status=status.HTTP_201_CREATED)
        else:
            err_msg = "Content is required!!!"
            return Response(data={'error_msg': err_msg},
                status=status.HTTP_400_BAD_REQUEST)

class ForumViewSet(viewsets.ViewSet):
    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def list(self, request):
        forums = Forum.objects.filter(is_hided=False)
        serializer = ForumSerializer(forums, many=True)
        return Response(data=serializer.data)
    def retrieve(self, request, pk):
        try:
            forum = Forum.objects.get(pk=pk)
        except Forum.DoesNotExist:
            return Http404()
        return Response(ForumSerializer(forum).data)
    def create(self, request):
        d = request.data
        l = Forum.objects.create(content=d['content'], creator=request.user)
        serializer = ForumSerializer(l)
        return Response(serializer.data,
            status=status.HTTP_201_CREATED)
    
class UserView(APIView):
    authentication_classes = [authentication.BasicAuthentication, authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]
    def get(self, request):
        pass
