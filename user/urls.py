from django.urls import path
from user import views

app_name = "user"

urlpatterns = [
    path('login/', views.login, name="login"),
    path('login_sql/', views.login_sql, name="login_sql"),
    path('register/', views.register, name="register"),
    path('register_sql/', views.register_sql, name="register_sql"),
    path('register_username/', views.register_username, name="register_username"),
    path('register_captcha/', views.register_captcha, name="register_captcha"),
    path('active/', views.active, name="active"),
    path('get_captcha/', views.get_captcha, name="get_captcha"),
    path('forget_pwd/', views.forget_pwd, name="forget_pwd"),
    path('forget_sql/', views.forget_sql, name="forget_sql"),
    path('reset_pwd/', views.reset_pwd, name="reset_pwd"),
    path('reset_pwd_sql/', views.reset_pwd_sql, name="reset_pwd_sql"),
    path('logout/', views.logout, name="logout"),
]
