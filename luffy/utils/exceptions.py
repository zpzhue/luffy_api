import logging

from django.db import DatabaseError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger('luffy')

def custom_exception_handler(exc, context):
    """
    自定义异常处理
    :param exc: 异常类
    :param context: 抛出异常的上下文
    :return: Response响应对象
    """
    # 先调用drf中原生异常处理方法
    response = exception_handler(exc, context)

    if response is None:
        view = context.get('view')
        if isinstance(exc, DatabaseError):
            # 数据库错误
            logger.error(f'[{view}] {exc}')
            return Response({'message': '服务器内部错误'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

    return response