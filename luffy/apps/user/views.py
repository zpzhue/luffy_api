import random

from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from luffy.lib.geetest import GeetestLib
from luffy.lib.yuntongxun.sms import CCP
from user.models import User
from user.serializers import UserModleSerializer


class VerifyCode(APIView):
    def get(self, request):
        """获取验证码"""
        user_id = random.randint(1, 100)
        APP_ID = "ace55c545adc865bc56e5e8856d4b2e2"
        APP_KEY = "fab724cde1d14717df1d0c67c7aa58e4"
        gt = GeetestLib(APP_ID, APP_KEY)

        status = gt.pre_process(user_id)
        request.session[gt.GT_STATUS_SESSION_KEY] = status
        request.session["user_id"] = user_id
        data = gt.get_response_str()
        # return Response(data, headers={"Access-Control-Allow-Credentials": True})
        return Response(data)

    def post(self, request):
        """校验验证码"""
        APP_ID = "ace55c545adc865bc56e5e8856d4b2e2"
        APP_KEY = "fab724cde1d14717df1d0c67c7aa58e4"
        gt = GeetestLib(APP_ID, APP_KEY)
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        challenge = request.data.get(gt.FN_CHALLENGE)
        validate = request.data.get(gt.FN_VALIDATE)
        seccode = request.data.get(gt.FN_SECCODE)
        user_id = request.session["user_id"]

        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)

        if result:
            # 如果验证通过，则生成遗传随机码保存到redis中，让用户提交数据是校验验证码数据的唯一性
            verify_code = '%08d' % random.randint(0, 99999999)
            conn = get_redis_connection('verify_code')
            conn.setex(verify_code, 60 * 5, 1)
            result = {"status": "success", 'code': verify_code}
        else:
            result = {"status": "fail", 'code': -1}

        # return Response(result, headers={"Access-Control-Allow-Credentials": True})
        return Response(result)


class SMSCodeAPIView(APIView):
    def get(self, request):
        '''短信验证码'''
        # 生成验证码
        sms_code = '%06d' % random.randint(0, 999999)
        mobile = request.query_params.get('mobile')

        if not mobile:
            return Response({'message': '请输入手机号', 'status': status.HTTP_400_BAD_REQUEST})
        try:
            User.objects.get(mobile=mobile)
            return Response({'message': '当前手机号已经注册', 'status': status.HTTP_400_BAD_REQUEST})
        except: pass

        conn = get_redis_connection('sms_code')  # 获取redis连接
        if conn.get(f'times_{mobile}'):
            return Response({'message': '当前手机号已经在一分钟之内发送过短信', 'status': status.HTTP_400_BAD_REQUEST})


        # todo:使用手机号发送短信验证码
        ccp = CCP()
        result = ccp.send_template_sms(mobile, [sms_code, '5分钟'], 1)
        if result == 0:
            # todo: 保存验证码到redis中
            pipeline = conn.pipeline()                      # 获取管道，使用管道发送数据，提高性能
            pipeline.multi()                                # 声明接下来会在管道中执行多条命令

            SMS_EXPIRE_TIME = 5 * 60                        # 短信验证码的有效时间
            SMS_SEND_TIME = 60                              # 验证码的发送间隔时间
            pipeline.setex(f'sms_{mobile}', SMS_EXPIRE_TIME, sms_code)
            pipeline.setex(f'sms_times_{mobile}', SMS_SEND_TIME, 1)

            pipeline.execute()                              # 统一执行管道中的命令

        return Response({'message': result, 'status': status.HTTP_200_OK})


class UserAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserModleSerializer
