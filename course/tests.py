import datetime

from django.test import TestCase

# Create your tests here.
import django, os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "baizhi_course_system.settings")
django.setup()

from course.models import TCategory, TArticle

# s = TCategory.objects.get(tarticle=4).title
# print(s)

# cate = TCategory.objects.all()
# for i in cate:
#     if i.id==4:
#         print(i.title)
# r = filter(lambda x:x.id==4,cate)
# print(r)
# for i in r:
#     print(i.title)
# cate = TCategory.objects.filter(id=1)
# print(cate)

# result = TArticle.objects.filter(cate__parent_id=1)
# print(result)
#
# cate = TCategory.objects.filter(level=1)
# print(cate.id)
# print(cate[2-1].title)
# print(cate.filter(id=2)[0].title)

# TCategory.objects.create(title="789",level=1)
# dd = "2020-11-06" + " " + "01:04"
# time = datetime.datetime.strptime(dd,"%Y-%m-%d %H:%M")
# TArticle.objects.create(title="呵呵呵",publish_time=time,cate_id="5")

# s1 = TArticle.objects.get(id=8)
# s2 = TArticle.objects.get(id=9)
# if s1.publish_time > s2.publish_time:
#     print(11111)
# elif s1.publish_time < s2.publish_time:
#     print(22222)
# else:
#     print(333333)

# s = TArticle.objects.get(title='jQuery')
# s = s.publish_time.strftime('%Y-%m-%d- %H:%M')
# s = s.replace("-","年",1)
# s = s.replace("-","月",1)
# s = s.replace("-","日",1)
# print(s)

# articles = TArticle.objects.all()
# print(articles)
# articles = TArticle.objects.order_by("count")
# print(articles)

# articles = TArticle.objects.filter(cate__parent_id=1)
# print(articles)
# articles = articles.order_by("count")
# print(articles)

