from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('scores', views.ScoreViewSet)
router.register('students', views.StudentViewSet)
router.register('subjects', views.SubjectViewSet)
router.register('classes', views.ClassViewSet)
router.register('instructors', views.InstructorViewSet)
router.register('forums', views.ForumViewSet, basename='forum')


urlpatterns = [
    path('', include(router.urls)),
    path('forumss/<int:lesson_id>/comments/',
         views.CommentAPIView.as_view())
]