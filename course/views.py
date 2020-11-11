import datetime
import traceback

from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
from django.urls import reverse

from course.models import TArticle, TCategory


def index(request):
    username = request.COOKIES.get("username")
    username = username.encode('latin-1').decode('utf-8')
    types = request.GET.get("type")
    # 将总页码存入session中
    articles = TArticle.objects.all()
    all_pages = len(articles) // 5 + 1
    request.session["all_pages"] = str(all_pages)
    if types:
        if types == "true_read":
            articles = TArticle.objects.order_by("count")
        elif types == "false_read":
            articles = TArticle.objects.order_by("-count")
        elif types == "true_time":
            articles = TArticle.objects.order_by("publish_time")
        elif types == "false_time":
            articles = TArticle.objects.order_by("-publish_time")
    else:
        articles = TArticle.objects.all()

    cates = TCategory.objects.filter(level=1)
    sub_cates = TCategory.objects.filter(level=2)

    # 获取url中的参数，如果不存在则返回第一页
    number = int(request.GET.get("number", 1))
    # 声明一个分页器对象
    pagtor = Paginator(object_list=articles, per_page=5)
    # 判断页号是否存在
    if number not in pagtor.page_range:
        number = 1
    # 调取某一页面的对象
    page = pagtor.page(number)
    # 将当前页码存入session中，需要在session中将session的周期改为一次会话
    request.session["index_number"] = str(number)
    # 取出排序后的types
    types = request.session.get("types")
    dic = {"username": username, "pages": page, "cates": cates, "sub_cates": sub_cates, "number": number, "type": types}
    return render(request, 'course/index.html', dic)


def course(request):
    username = request.COOKIES.get("username")
    username = username.encode('latin-1').decode('utf-8')

    cates = TCategory.objects.filter(level=1)
    sub_cates = TCategory.objects.filter(level=2)

    level = request.GET.get("level")
    id = request.GET.get("id")
    request.session["course_level"] = level
    request.session["course_id"] = id

    types = request.session.get("types")
    if types:
        if level == "1":
            if types == "true_read":
                articles = TArticle.objects.filter(cate_id__parent_id=int(id)).order_by("count")
            elif types == "false_read":
                articles = TArticle.objects.filter(cate_id__parent_id=int(id)).order_by("-count")
            elif types == "true_time":
                articles = TArticle.objects.filter(cate_id__parent_id=int(id)).order_by("publish_time")
            elif types == "false_time":
                articles = TArticle.objects.filter(cate_id__parent_id=int(id)).order_by("-publish_time")
        elif level == "2":
            if types == "true_read":
                articles = TArticle.objects.filter(cate_id=int(id)).order_by("count")
            elif types == "false_read":
                articles = TArticle.objects.filter(cate_id=int(id)).order_by("-count")
            elif types == "true_time":
                articles = TArticle.objects.filter(cate_id=int(id)).order_by("publish_time")
            elif types == "false_time":
                articles = TArticle.objects.filter(cate_id=int(id)).order_by("-publish_time")
    else:
        if level == "1":
            articles = TArticle.objects.filter(cate__parent_id=int(id))
        elif level == "2":
            articles = TArticle.objects.filter(cate=int(id))
    if level == "1":
        title1 = cates.filter(id=id)[0].title
        title2 = ""
        parent_id = id
        parent_level = level
    else:
        title1 = TCategory.objects.filter(id=TCategory.objects.filter(id=id)[0].parent_id)[0].title
        title2 = sub_cates.filter(id=id)[0].title
        parent_id = TCategory.objects.get(id=id).parent_id
        parent_level = TCategory.objects.get(id=parent_id).level
    # 获取url中的参数，如果不存在则返回第一页
    number = int(request.GET.get("number", 1))

    # 声明一个分页器对象
    pagtor = Paginator(object_list=articles, per_page=5)
    # 判断页号是否存在
    if number not in pagtor.page_range:
        number = 1
    # 调取某一页面的对象
    page = pagtor.page(number)
    #
    # 将当前页码存入session中，需要在session中将session的周期改为一次会话
    request.session["course_number"] = str(number)
    dic = {"username": username, "pages": page, "cates": cates, "sub_cates": sub_cates,
           "level": level, "id": id, "title1": title1, "title2": title2,"number": number,
           "type":types, "parent_id": parent_id, "parent_level": parent_level}
    return render(request, 'course/pythonBase.html', dic)


# def delete(request):
#     try:
#         level = request.GET.get("level")
#         id = request.GET.get("id")
#         delete_id = request.GET.get("delete_id")
#         article = TArticle.objects.filter(id=int(delete_id))
#         with transaction.atomic():
#             article.delete()
#             if level and id:
#                 course_number = request.session.get("course_number")
#                 url = reverse('course:course') + "?level=" + level + "&id=" + id + "&number=" + course_number
#                 return redirect(url)
#             index_number = request.session.get("index_number")
#             url = reverse('course:index') + "?number=" + index_number
#             return redirect(url)
#     except:
#         return redirect('course:index')


def delete(request):
    level = request.POST.get("level")
    id = request.POST.get("id")
    delete_id = request.POST.get("delete_id")
    article = TArticle.objects.filter(id=int(delete_id))
    article.delete()
    if level == "1":
        articles = TArticle.objects.filter(cate__parent_id=int(id))
    elif level == "2":
        articles = TArticle.objects.filter(cate=int(id))
    else:
        articles = TArticle.objects.all()
    # index获取总页码/pythonBase获取当前选择种类的总页码
    all_pages = len(articles) // 5 + 1
    s = len(articles) % 5
    if s == 0:
        all_pages -= 1
    # 获取url中的参数
    number = int(request.POST.get("number"))
    if number > all_pages:
        number -= 1
        # if level and id:
        #     return HttpResponse("level" + str(level) + "id" + str(id) + "number:" + str(number))
        # return HttpResponse("number:" + str(number))
    # 声明一个分页器对象
    pagtor = Paginator(object_list=articles, per_page=5)
    # # 判断页号是否存在
    # if number not in pagtor.page_range:
    #     number = 1
    # 调取某一页面的对象
    page = pagtor.page(number)

    def my_default(u):
        if isinstance(u, TArticle):
            s = u.publish_time.strftime('%Y-%m-%d- %H:%M')
            s = s.replace("-", "年", 1)
            s = s.replace("-", "月", 1)
            s = s.replace("-", "日", 1)
            return {"id": u.id, "title": u.title, "count": u.count,
                    "publish_time": s, "cate": u.cate, "cate_title": u.cate.title,
                    "level": level, "cate_id": id}

    return JsonResponse({"pages": list(page)}, json_dumps_params={"default": my_default})


def add_course(request):
    username = request.COOKIES.get("username")
    username = username.encode('latin-1').decode('utf-8')
    cates = TCategory.objects.filter(level=1)
    sub_cates = TCategory.objects.filter(level=2)
    dic = {"username": username, "cates": cates, "sub_cates": sub_cates}
    return render(request, 'course/addCourse.html', dic)


def add_course_sql(request):
    try:
        name = request.POST.get("name")
        title = request.POST.get("title")
        course_name = request.POST.get("cate_sel")
        with transaction.atomic():
            if course_name == None:
                cates = TCategory.objects.filter(level=1)
                for cate in cates:
                    if cate.title == name:
                        return HttpResponse("yes_no")
                else:
                    TCategory.objects.create(title=name, level=int(title))
                    return HttpResponse("yes")
            elif course_name == "defaultCate":
                return HttpResponse("no")
            else:
                sub_cates = TCategory.objects.filter(level=2)
                for sub_cate in sub_cates:
                    if sub_cate.title == name:
                        return HttpResponse("no_no")
                else:
                    parend_id = TCategory.objects.get(title=course_name).id
                    TCategory.objects.create(title=name, level=int(title), parent_id=parend_id)
                    return HttpResponse("yes")
    except:
        traceback.print_exc()
        return HttpResponse("no")


def add_article(request):
    username = request.COOKIES.get("username")
    username = username.encode('latin-1').decode('utf-8')
    cates = TCategory.objects.filter(level=1)
    sub_cates = TCategory.objects.filter(level=2)
    # pythonBase获取当前选择种类的总页码
    level = request.session.get("course_level")
    id = request.session.get("course_id")
    if level == "1":
        articles = TArticle.objects.filter(cate__parent_id=int(id))
    elif level == "2":
        articles = TArticle.objects.filter(cate=int(id))
    course_pages = len(articles) // 5 + 1
    s = len(articles) % 5
    if s == 0:
        course_pages -= 1
    # index总页码
    all_pages = request.session.get("all_pages")

    dic = {"username": username, "cates": cates, "sub_cates": sub_cates,
           "all_pages": all_pages,"course_pages":course_pages,"level":level,"id":id}
    return render(request, 'course/addArticle.html', dic)


def add_article_sql(request):
    try:
        name = request.POST.get("name")
        cate_sel = request.POST.get("cate_sel")
        course_sel = request.POST.get("course_sel")
        time = request.POST.get("time")
        if time == "":
            return HttpResponse("yes_no")
        text = request.POST.get("text")
        if name == None or course_sel == None or cate_sel == None:
            return HttpResponse("yes_no")
        id = TCategory.objects.get(title=course_sel).id
        with transaction.atomic():
            if text == None:
                text = ""
            TArticle.objects.create(title=name, publish_time=time, cate_id=id, content=text)
            return HttpResponse("yes")
    except:
        traceback.print_exc()
        return HttpResponse("no")


def update(request):
    id = request.GET.get("id")
    request.session["update_id"] = id
    user = TArticle.objects.get(id=id)
    if user.count == 0 or user.count == None or user.count == "":
        user.count = 1
    else:
        user.count += 1
    user.save()
    if user.content == None:
        user.content = ""
    # 所属课程
    course_name = TCategory.objects.get(id=user.cate_id).title
    # 课程分类
    cate_name = TCategory.objects.get(id=TCategory.objects.get(id=user.cate_id).parent_id).title
    username = request.COOKIES.get("username")
    username = username.encode('latin-1').decode('utf-8')
    cates = TCategory.objects.filter(level=1)
    sub_cates = TCategory.objects.filter(level=2)
    index_number = request.session.get("index_number")
    course_number = request.session.get("course_number")
    dic = {"username": username, "article_name": user.title, "cate_name": cate_name,
           "course_name": course_name, "article_content": user.content,
           "cates": cates, "sub_cates": sub_cates,
           "index_number": index_number, "course_number": course_number}
    return render(request, 'course/update.html', dic)


def update_sql(request):
    try:
        id = request.session.get("update_id")
        article = TArticle.objects.get(id=id)
        name = request.POST.get("name")
        # 跳转时的等级
        cate_sel = request.POST.get("cate_sel")
        # 跳转时的id
        course_sel = request.POST.get("course_sel")
        cate_level = TCategory.objects.get(title=course_sel).level
        cate_id = TCategory.objects.get(title=course_sel).id
        print(309,cate_level,cate_id)
        time = request.POST.get("time")
        content = request.POST.get("content")
        with transaction.atomic():
            article.title = name
            article.publish_time = time
            article.cate_id = cate_id
            if content == None:
                article.content = ""
            else:
                article.content = content
            article.save()
            course_number = request.session.get("course_number")
            index_number = request.session.get("index_number")
            if cate_level and cate_id and course_number:
                lis = [cate_level, cate_id, course_number]
            else:
                lis = [index_number]

            def my_default():
                return {"cate_level": cate_level,
                        "cate_id": cate_id,
                        "course_number": course_number}

            return JsonResponse({"list": lis}, json_dumps_params={"default": my_default})
    except:
        traceback.print_exc()
        return HttpResponse("no")


def cate_select(request):
    cate_sel = request.POST.get("cate_sel")
    if cate_sel == "defaultCourse":
        course = TCategory.objects.filter(level=2)
    else:
        course = TCategory.objects.filter(parent_id=TCategory.objects.get(title=cate_sel).id)

    def my_default(u):
        if isinstance(u, TCategory):
            return {"title": u.title}

    return JsonResponse({"course": list(course)}, json_dumps_params={"default": my_default})


def course_select(request):
    course_sel = request.POST.get("course_sel")
    cate = TCategory.objects.get(id=TCategory.objects.get(title=course_sel).parent_id)
    return HttpResponse(cate.title)


def sorting(request):
    types = request.POST.get("type")
    request.session["types"] = types
    number = request.POST.get("number")
    level = request.POST.get("level")
    id = request.POST.get("id")

    def my_default(u):
        if isinstance(u, TArticle):
            s = u.publish_time.strftime('%Y-%m-%d- %H:%M')
            s = s.replace("-", "年", 1)
            s = s.replace("-", "月", 1)
            s = s.replace("-", "日", 1)
            return {"id": u.id, "title": u.title, "count": u.count,
                    "publish_time": s, "cate": u.cate, "cate_title": u.cate.title,
                    "level": level, "cate_id": id}

    if level == "1":
        if types == "true_read":
            articles = TArticle.objects.filter(cate_id__parent_id=int(id)).order_by("count")
        elif types == "false_read":
            articles = TArticle.objects.filter(cate_id__parent_id=int(id)).order_by("-count")
        elif types == "true_time":
            articles = TArticle.objects.filter(cate_id__parent_id=int(id)).order_by("publish_time")
        elif types == "false_time":
            articles = TArticle.objects.filter(cate_id__parent_id=int(id)).order_by("-publish_time")
    elif level == "2":
        if types == "true_read":
            articles = TArticle.objects.filter(cate_id=int(id)).order_by("count")
        elif types == "false_read":
            articles = TArticle.objects.filter(cate_id=int(id)).order_by("-count")
        elif types == "true_time":
            articles = TArticle.objects.filter(cate_id=int(id)).order_by("publish_time")
        elif types == "false_time":
            articles = TArticle.objects.filter(cate_id=int(id)).order_by("-publish_time")
    else:
        if types == "true_read":
            articles = TArticle.objects.order_by("count")
        elif types == "false_read":
            articles = TArticle.objects.order_by("-count")
        elif types == "true_time":
            articles = TArticle.objects.order_by("publish_time")
        elif types == "false_time":
            articles = TArticle.objects.order_by("-publish_time")
    # 声明一个分页器对象
    pagtor = Paginator(object_list=articles, per_page=5)
    # 判断页号是否存在
    if int(number) not in pagtor.page_range:
        number = 1
    # 调取某一页面的对象
    page = pagtor.page(number)
    return JsonResponse({"pages": list(page)}, json_dumps_params={"default": my_default})
