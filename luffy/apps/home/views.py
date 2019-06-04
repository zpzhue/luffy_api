from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from home.models import BannerInfo
from home.serializer import BannerInfoSerializer


class BannerInfoAPIView(ListAPIView):
    queryset = BannerInfo.objects.filter(Q(is_delete=False) & Q(is_show=True)).order_by('order')
    serializer_class = BannerInfoSerializer
    def list(self, request):
        serializer = self.get_serializer_class()
        queryset = self.get_queryset()
        for item in queryset:
            # item.image = 'http://api.luffycity.cn:8000/static/' + item.image.url
            item.image = item.image.url
        banners = serializer(queryset, many=True)

        return Response(banners.data)


# class BannerInfoAPIView2(APIView):
#     def get(self, request):
#         queryset = BannerInfo.objects.filter(Q(is_delete=False) & Q(is_show=True)).order_by('order')
#
#         # 序列化
#         data = []
#         for item in queryset:
#             data.append({
#                 # 拼接图片的url地址
#                 "image": "/static/" + item.image.url,
#                 "link": item.link,
#                 "name": item.name,
#             })
#         return Response(data)