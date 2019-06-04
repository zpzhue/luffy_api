import random
from datetime import datetime
from decimal import Decimal

from django.db import transaction
from django_redis import get_redis_connection
from rest_framework import serializers

from user.models import User
from . import models
from courses.models import Course

class OrderSerializer(serializers.ModelSerializer):
    # order_number = serializers.SerializerMethodField(read_only=True)
    # total_price = serializers.SerializerMethodField(read_only=True)
    # order_desc = serializers.SerializerMethodField(read_only=True)
    # user = serializers.SerializerMethodField(write_only=True)

    class Meta:
        model = models.Order
        fields = ('id', 'order_number', 'order_status', 'total_price', 'order_desc')
        extra_kwargs = {
            # 'password': {'write_only': True},
            'id': {'read_only': True},
            'order_number': {'read_only': True},
            'order_status': {'read_only': True},
            'total_price': {'read_only': True},
            'order_desc': {'read_only': True},
        }

    # def get_order_number(self, obj):pass
    # def get_total_price(self, obj):pass
    # def get_order_desc(self, obj):pass


    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        # todo: 计算总价
        conn = get_redis_connection('cart')
        redis_course_list = conn.smembers(f'cart_select_{user.id}')
        redis_cart_info = conn.hgetall(f'cart_{user.id}')

        total_price = 0
        for cid, price in redis_cart_info.items():
            if cid in redis_course_list:
                total_price += Decimal(price.decode())

        # todo: 设置事务保存点
        save_point = transaction.savepoint()

        # 自己生成一个订单号,# 结合时间戳和当前用户ID来生成，才能保证整站唯一
        order_number = f'{datetime.now().strftime("%Y%m%d%H%M%S")}{user.id:0>6d}{random.randint(0, 9999):0>4d}'

        order = models.Order.objects.create(
            user=user,
            order_number=order_number,
            order_status=0,  # 订单状态默认为未支付
            order_desc=f'路飞学成课程--{Course.objects.get(id=redis_course_list.pop().decode()).name}',  # # 订单描述信息
            total_price=total_price
        )

        if order:
            selected_course_list = conn.smembers(f'cart_select_{user.id}')
            try:
                for cid in selected_course_list:
                    # data = {
                    #     'order_id': {'id': order.id},
                    #     'course_id': Course.objects.get(id=cid.decode()).id,
                    #     'price': Decimal(redis_cart_info.get(cid).decode()),
                    #     'user_id': user.id,
                    # }
                    models.OrderDetail.objects.create(
                        order_id=order.id,
                        course_id=cid.decode(),
                        price=Decimal(redis_cart_info.get(cid).decode()),
                        user_id=user.id,
                    )

                    # 删除购物车记录
                    conn.hdel(f"cart_{user.id}", cid.decode())
                    conn.srem(f"cart_select_{user.id}",  cid.decode())
            except Exception as e:
                transaction.savepoint_rollback(save_point)
                raise
        return order


class OrderDetailSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    course_img = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = models.OrderDetail
        fields = ('name', 'course_img', 'price')
        extra_kwargs = {
            'price': {'read_only': True},
        }

    def get_name(self, obj):
        return obj.course.name

    def get_course_img(self, obj):
        return obj.course.course_img.url

    # def validate_order(self, value):
    #     print('校验order')
    #     try:
    #         models.Order.objects.get(pk=value.get('id'))
    #         print(value)
    #     except models.Order.DoesNotExist:
    #         serializers.ValidationError('获取订单id出错，请联系客服~')
    #     return value
    #
    # def validate_odetail_user(self, value):
    #     print('校验user_id')
    #     try:
    #         User.objects.get(pk=value)
    #         print(value)
    #     except User.DoesNotExist:
    #         serializers.ValidationError('用户不存在')
    #     return value
    #
    # def validate_course_order(self, value):
    #     print('校验course')
    #     try:
    #         Course.objects.get(pk=value)
    #         print(value)
    #     except Course.DoesNotExist:
    #         serializers.ValidationError('课程id不存在')
    #     return value
    #
    # def validate_price(self, value):return value
    #
    # def create(self, validated_data):
    #     print(validated_data)
    #     detail = models.OrderDetail.objects.create(
    #         order=models.Order.objects.get(id=validated_data.get('order')['id']),
    #         course=validated_data.get('course'),
    #         price=validated_data.get('price'),
    #         user=validated_data.get('user'),
    #     )
    #
    #     return detail