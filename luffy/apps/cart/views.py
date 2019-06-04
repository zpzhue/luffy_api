from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from courses import models
from orders.models import OrderDetail

class CartAPIView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        '''获取购物车中信息'''

        # 1、 从redis中取出购物车数据
        conn = get_redis_connection('cart')
        course_list = conn.hgetall(f'cart_{request.user.id}')
        select_list = conn.smembers(f'cart_select_{request.user.id}')

        data = []
        for course_id, price in course_list.items():
            try:
                course = models.Course.objects.get(id=course_id, is_delete=False, status=0)
            except models.Course.DoesNotExist:
                return Response({'msg': '请求数据有误，请联系客服'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)
            # 手动序列化数据
            data.append({
                'id': course_id.decode(),
                'name': course.name,
                'price': price.decode(),
                'selected': course_id in select_list,
                'course_img': course.course_img.url,
                'effective_time': OrderDetail.EFFECTIVE_CHOICES
            })
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        # 1、 获取、校验参数
        course_id = request.data.get('course_id')
        if not course_id:
            return Response({'msg': '参数错误，缺少课程id'}, status=status.HTTP_400_BAD_REQUEST)

        # 2、 校验课程是否存在
        try:
            course = models.Course.objects.get(id=course_id, is_delete=False, status=0)
        except models.Course.DoesNotExist:
            return Response({'msg': '课程不存在或已下架'}, status=status.HTTP_400_BAD_REQUEST)

        # 3、 加入购物车
        conn = get_redis_connection('cart')
        pipeline = conn.pipeline()
        pipeline.multi()

        # 保存购物车记录
        pipeline.hset(f'cart_{request.user.id}', course_id, str(course.price))
        # 保存购物车课程勾选状态
        pipeline.sadd(f'cart_select_{request.user.id}', course_id)

        pipeline.execute()

        return Response({'msg': '添加成功'}, status=status.HTTP_200_OK)

    def patch(self, request):
        '''修改商品勾中状态'''
        course_id = request.data.get('course_id')
        is_selected = request.data.get('is_selected')

        if not (course_id and is_selected is not None):
            return Response({'msg': '参数错误或参数不完整'}, status=status.HTTP_400_BAD_REQUEST)

        # 校验课程id
        course = self.get_course(course_id)
        if not course:
            return Response({'msg': '课程信息错误，请练习客服'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

        conn = get_redis_connection('cart')
        if is_selected:
            conn.sadd(f'cart_select_{request.user.id}', course_id)
        else:
            conn.srem(f'cart_select_{request.user.id}', course_id)

        return Response({'msg':'修改成功', 'status_code': 0}, status=status.HTTP_200_OK)


    def delete(self, request):
        course_id = request.data.get('course_id')

        if not course_id:
            return Response({'msg': '参数错误或参数不完整'}, status=status.HTTP_400_BAD_REQUEST)

        course = self.get_course(course_id)
        if not course:
            return Response({'msg': '课程信息错误，请练习客服'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

        conn = get_redis_connection('cart')
        pipline = conn.pipeline()
        pipline.multi()
        pipline.hdel(f'cart_{request.user.id}', course_id)
        pipline.srem(f'cart_select_{request.user.id}', course_id)
        pipline.execute()
        return Response({'msg': '修改成功', 'status_code': 0}, status=status.HTTP_200_OK)

    def get_course(self, id):
        try:
            course = models.Course.objects.get(id=id, is_delete=False, status=0)
        except models.Course.DoesNotExist:
            course = None

        return course



