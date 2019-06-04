from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from user.models import User


def jwt_response_payload_handler(token, user=None, request=None):
    '''
    自定义jwt认证成功后的数据
    :param token: jwt返回的token
    :param user: 当前登录的用户信息[对象]
    :param request: 当前本次客户端提交过来的数据
    :return: 返回前端所需格式的数据
    '''
    return {
        'id': user.id,
        'username': user.username,
        'token': token
    }


class UsernameMobileAuthBackend(ModelBackend):
    def get_user_by_account(self, account):
        try:
            user = User.objects.get(Q(username=account) | Q(mobile=account))
        except User.DoesNotExist:
            user = None
        return user

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = self.get_user_by_account(username)
        if user is not None and user.check_password(password):
            return user