from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from orders.serializers import OrderSerializer, OrderDetailSerializer
from . import models


class OrderModelViewSetAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrderSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response({'msg': '提交成功', 'order_id': order.id}, status=status.HTTP_200_OK)


class OrderDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        queryset = models.OrderDetail.objects.filter(order_id=order_id, is_delete=False)
        if not queryset:
            return Response({'status_code':1, 'data': None, 'msg': '未查询到结果'})
        serailizer = OrderDetailSerializer(queryset, many=True)
        return Response({'status_code':0, 'data': serailizer.data, 'msg': 'ok'})