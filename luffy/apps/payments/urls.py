from django.urls import path

from payments.views import PaymentsAPIView, PayResultAPIView


urlpatterns = [
    path(r'<int:order_id>/', PaymentsAPIView.as_view()),
    path(r'success/', PayResultAPIView.as_view()),
]