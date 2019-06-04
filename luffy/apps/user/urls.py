from django.urls import path

from rest_framework_jwt.views import obtain_jwt_token

from user import views

urlpatterns = [
    path(r'login/', obtain_jwt_token),
    path(r'verify/', views.VerifyCode.as_view()),
    path(r'sms_code/', views.SMSCodeAPIView.as_view()),
    path(r'user', views.UserAPIView.as_view())
]