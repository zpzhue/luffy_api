from django.db import models

from luffy.utils.base_model import BaseModel

class Order(BaseModel):
    """订单记录"""
    status_choices = (
        (0, '未支付'),
        (1, '已支付'),
        (2, '已取消'),
        (3, '待评价')
    )
    order_number = models.CharField(unique=True, max_length=64,verbose_name="订单号")
    order_status = models.SmallIntegerField(choices=status_choices, default=0, verbose_name="订单状态")
    total_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="订单总价", default=0)
    order_desc = models.CharField(max_length=120,verbose_name="订单描述")
    created_time = models.DateTimeField(verbose_name="订单生成时间", auto_now_add=True)
    pay_time = models.DateTimeField(verbose_name="订单支付时间", null=True)
    user = models.ForeignKey('user.User', related_name='orders_user', on_delete=models.DO_NOTHING,verbose_name="用户ID")
    class Meta:
        db_table="lf_order"
        verbose_name= "订单记录"
        verbose_name_plural= "订单记录"


class OrderDetail(BaseModel):
    """订单详情"""
    EFFECTIVE_CHOICES = (
        (0, '永久有效'),
        (1, '1个月有效'),
        (2, '2个月有效'),
        (3, '3个月有效'),
        (4, '6个月有效'),
        (5, '12个月有效'),
    )
    order = models.ForeignKey("Order", related_name='order_course', on_delete=models.CASCADE, verbose_name="订单ID")
    course = models.ForeignKey('courses.Course', related_name='course_order', on_delete=models.CASCADE, verbose_name="课程ID")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="课程购买价格", default=0)
    user = models.ForeignKey('user.User', related_name='odetail_user', null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name="用户ID")
    # effective_time = models.SmallIntegerField(choices=EFFECTIVE_CHOICES, default=2, verbose_name='有效期')

    class Meta:
        db_table="lf_order_detail"
        verbose_name= "订单详情"
        verbose_name_plural= "订单详情"