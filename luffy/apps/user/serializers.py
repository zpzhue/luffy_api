import re

from django_redis import get_redis_connection
from rest_framework import serializers

from user.models import User


class UserModleSerializer(serializers.ModelSerializer):
    sms_code = serializers.CharField(label='手机验证码', required=True, write_only=True, allow_null=False, allow_blank=False)
    password2 = serializers.CharField(label='确认密码', required=True, write_only=True, allow_null=False, allow_blank=False)
    token = serializers.CharField(label='jwt', read_only=True)
    verify_code = serializers.CharField(label='极验验证码校验码', write_only=True)

    class Meta:
        fields = ('id','sms_code', 'mobile', 'password','password2', 'token', 'verify_code')
        model = User
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
        }


    def validate_mobile(self, value):
        if not re.match('0?(13|14|15|17|18|19)[0-9]{9}', value):
            print('请输入正确的手机号')
            raise serializers.ValidationError('请输入正确的手机号')

        try:
            User.objects.get(mobile=value)
            print('该手机号已经注册')
            raise serializers.ValidationError('该手机号已经注册')
        except User.DoesNotExist: pass

        return value

    def validate_password(self, value):
        if len(value) < 6 or len(value) > 20:
            print('密码最少6位，最长20位')
            raise serializers.ValidationError('密码最少8位，最长20位')

        if re.search('\W', value):
            print('密码不能包含特殊字符')
            raise serializers.ValidationError('密码不能包含特殊字符')

        return value

    def validate_verify_code(self, value):
        conn = get_redis_connection('verify_code')
        verify_code = conn.get(value)
        print(verify_code)
        if not verify_code:
            raise serializers.ValidationError('验证码失效')
        return value

    def validate(self, data):
        print('全局校验')
        # 全局校验
        # 获取数据
        password = data.get('password')
        password2 = data.get('password2')
        sms_code = data.get('sms_code')
        mobile = data.get('mobile')

        if password != password2:
            print('两次输入密码不一致')
            raise serializers.ValidationError('两次输入密码不一致')

        # 验证短信验证码
        conn = get_redis_connection('sms_code')
        redis_sms_code = conn.get(f'sms_{mobile}')

        if not(redis_sms_code and redis_sms_code.decode() == sms_code):
            print('手机验证码无效')
            raise serializers.ValidationError('手机验证码无效')

        return data

    def create(self, validated_data):
        del validated_data['sms_code']
        del validated_data['password2']
        del validated_data['verify_code']
        validated_data['username'] = validated_data['mobile']
        print(validated_data)

        # 继续调用ModelSerializer内置的添加数据功能
        user = super().create(validated_data)
        # 对密码加密
        user.set_password(user.password)
        user.save()

        # 删除redis中验证码的数据
        conn = get_redis_connection()
        conn.delete(f'sms_{validated_data["mobile"]}')

        from rest_framework_jwt.settings import api_settings
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        user.token = jwt_encode_handler(payload)

        return user

