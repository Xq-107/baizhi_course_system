from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class MyMiddleWare(MiddlewareMixin):
    def __init__(self, get_response):  # 初始化
        super().__init__(get_response)
        # print("init1")
        pass


    # view处理请求前执行
    def process_request(self, request):  # 某一个view
        # print("request:", request)
        check_url = [reverse('course:index')]
        if request.path in check_url:
            is_login = request.session.get('is_login')
            if is_login:
                pass
            else:
                return redirect('user:login')
        # pass_url = [reverse('user:login'),reverse('user:register')]
        # if request.path in pass_url:
        #     pass
        # else:
        #     is_login = request.session.get('is_login')
        #     if is_login:
        #         pass
        #     else:
        #         return redirect('user:login')


    # 在process_request之后View之前执行
    def process_view(self, request, view_func, view_args, view_kwargs):
        pass
        # print("view:", request, view_func, view_args, view_kwargs)

    # view执行之后，响应之前执行
    def process_response(self, request, response):
        # print("response:", request, response)
        return response  # 必须返回response

    #
    # 如果View中抛出了异常
    def process_exception(self, request, ex):  # View中出现异常时执行
        pass
        # print("exception:", request, ex)