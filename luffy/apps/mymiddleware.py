from django.utils.deprecation import MiddlewareMixin


class TestMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print(request)

        return