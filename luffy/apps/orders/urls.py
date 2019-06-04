from django.urls import path
from rest_framework.routers import SimpleRouter

from rest_framework_jwt.views import obtain_jwt_token

from orders.views import OrderModelViewSetAPI, OrderDetailAPIView
from user import views

urlpatterns = [
    path('', OrderModelViewSetAPI.as_view()),
    path('detail/<int:order_id>/', OrderDetailAPIView.as_view())
]
