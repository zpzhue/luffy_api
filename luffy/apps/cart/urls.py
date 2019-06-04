from django.urls import path

from cart.views import CartAPIView

urlpatterns = [
    path(r'', CartAPIView.as_view()),
]
