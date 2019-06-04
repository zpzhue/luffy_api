from django.urls import path

from home import views


urlpatterns = [
    path('banner/', views.BannerInfoAPIView.as_view()),
    # path('banner/', views.BannerInfoAPIView2.as_view()),
]
