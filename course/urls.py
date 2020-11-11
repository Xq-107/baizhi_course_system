from django.urls import path
from course import views


app_name = "course"


urlpatterns = [
    path('index/',views.index,name="index"),
    path('course/',views.course,name="course"),
    path('delete/',views.delete,name="delete"),
    path('add_course/',views.add_course,name="add_course"),
    path('add_course_sql/',views.add_course_sql,name="add_course_sql"),
    path('add_article/',views.add_article,name="add_article"),
    path('add_article_sql/',views.add_article_sql,name="add_article_sql"),
    path('update/',views.update,name="update"),
    path('update_sql/',views.update_sql,name="update_sql"),
    path('cate_select/',views.cate_select,name="cate_select"),
    path('course_select/',views.course_select,name="course_select"),
    path('sorting/',views.sorting,name="sorting"),
]