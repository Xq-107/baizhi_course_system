from django.test import TestCase

# Create your tests here.
import django,os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "baizhi_course_system.settings")
django.setup()

from user.models import TUser

# user = TUser.objects.filter(name="王憨憨")
# print(user)
# print(user[0].name)

# user = TUser.objects.filter(name="王二猪")
# if user:
#     print(111)
# else:
#     print(222)
