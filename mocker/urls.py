#-*- coding: utf-8 -*-
# @Time    : 2019/11/25 14:55
# @File    : urls.py
# @Author  : 守望@天空~
from django.urls import path
from . import views
urlpatterns = [
    path("<str:msg>",views.mock_data),
    path("<str:msg>/<str:path>",views.mock_data),
]