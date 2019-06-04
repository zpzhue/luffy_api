from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from courses import models
from courses.serializers import CourseCategorySerializer, CourseSerializer, CourseDetailModelSerializer


class CourseCategroyAPIView(ListAPIView):
    queryset = models.CourseCategory.objects.filter(is_delete=False, is_show=True).order_by('order')
    serializer_class = CourseCategorySerializer


class StandarPageNumberPagination(PageNumberPagination):
    max_page_size = 10
    page_size_query_param = 'page_size'


class CourseAPIView(ListAPIView):
    queryset = models.Course.objects.filter(is_delete=False, status=0).order_by('-order', '-studys')
    serializer_class = CourseSerializer

    # 分页
    pagination_class = StandarPageNumberPagination

    # 过滤、排序
    filter_fields = ['course_category']
    ordering = ('id', 'studys', 'price', 'pub_date')
    filter_backends = (OrderingFilter, DjangoFilterBackend)


class CourseDetailAPIView(RetrieveAPIView):
    queryset = models.Course.objects.filter(is_show=True, is_delete=False)
    serializer_class = CourseDetailModelSerializer
