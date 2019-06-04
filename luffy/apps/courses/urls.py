from django.urls import path

from courses import views
from courses.views import CourseCategroyAPIView, CourseAPIView, CourseDetailAPIView

urlpatterns = [
    path(r'course_categroy/', CourseCategroyAPIView.as_view()),
    path(r'<int:pk>/', CourseDetailAPIView.as_view()),
    path(r'', CourseAPIView.as_view())
]
