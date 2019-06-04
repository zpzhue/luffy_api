from datetime import datetime

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from alipay import AliPay

from orders.models import Order


class PaymentsAPIView(APIView):

    def get(self, request, order_id):
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist():
            return Response({"msg": "当前订单不存在!"}, status=status.HTTP_400_BAD_REQUEST)

        alipay = AliPay(
            appid=settings.ALIPAY_APP_ID,
            app_notify_url=None,  # 默认回调url
            # 应用私钥
            app_private_key_path=settings.APP_PRIVATE_KEY_PATH,
            # 支付宝的公钥,
            alipay_public_key_path=settings.ALIPAY_PUBLIC_KEY_PATH,
            sign_type="RSA2",  # 密码加密的算法
            # 开发时属于调试模式
            debug=settings.ALIPAY_DEBUG  # 默认False
        )

        # 生成参数
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order.order_number,
            total_amount=float(order.total_price),  # 订单价格,单位:元 / RMB
            subject=order.order_desc,  # 订单标题
            return_url=settings.ALIPAY_RETURN_URL,
            notify_url=settings.ALIPAY_NOTIFY_URL  # 可选, 不填则使用默认notify url
        )
        # 拼接成完整的链接地址
        pay_url = settings.APIPAY_GATEWAY + "?" + order_string

        return Response({"pay_url": pay_url}, status=status.HTTP_200_OK)


class PayResultAPIView(APIView):
    def get(self,request):
        """处理get返回结果的数据"""
        # 接受数据
        data = request.query_params.dict()
        print(data)
        # sign 不能参与签名验证
        signature = data.pop("sign")
        # print(json.dumps(data))
        # print(signature)
        alipay = AliPay(
            appid=settings.ALIPAY_APP_ID,
            app_notify_url=None,  # 默认回调url
            app_private_key_path=settings.APP_PRIVATE_KEY_PATH,         # 应用私钥
            alipay_public_key_path=settings.ALIPAY_PUBLIC_KEY_PATH,     # 支付宝的公钥
            sign_type="RSA2",                                           # 密码加密的算法
            debug = settings.ALIPAY_DEBUG                               # 开发时属于调试模式,  默认False
        )

        # verify验证支付结果,布尔值
        success = alipay.verify(data, signature)

        if success:
            # 支付成功
            order = Order.objects.get(order_number=data.get("out_trade_no"))
            order.order_status = 1 # 修改订单状态
            order.pay_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            order.save()


            return Response({
                "length":order.order_course.count(),
                "paytime": order.pay_time,
                "price":order.total_price,
                "info":order.order_desc,
                'staus': 'OK',
            },status=status.HTTP_200_OK)

        return Response({"message":"订单没有变化"})

    def post(self,request):
        """提供给支付宝发送post数据"""
        # 参考上面的代码实现
        # 接受数据
        data = request.data.dict()

        # sign 不能参与签名验证
        signature = data.pop("sign")
        # print(json.dumps(data))
        # print(signature)
        alipay = AliPay(
            appid=settings.ALIPAY_APP_ID,
            app_notify_url=None,  # 默认回调url
            # 应用私钥
            app_private_key_path=settings.APP_PRIVATE_KEY_PATH,
            # 支付宝的公钥,
            alipay_public_key_path=settings.ALIPAY_PUBLIC_KEY_PATH,
            sign_type="RSA2",  # 密码加密的算法
            # 开发时属于调试模式
            debug=settings.ALIPAY_DEBUG  # 默认False
        )

        # verify验证支付结果,布尔值
        success = alipay.verify(data, signature)

        if success:
            # 支付成功
            order = Order.objects.get(order_number=data.get("out_trade_no"))
            order.order_status = 1  # 修改订单状态
            order.pay_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            order.save()

            return Response({
                "length": order.order_course.count(),
                "paytime": order.pay_time,
                "price": order.total_price,
                "info": order.order_desc,
            }, status=status.HTTP_200_OK)

        return Response({"message": "订单没有变化"})
