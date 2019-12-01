#-*- coding: utf-8 -*-
# @Time    : 2019/11/29 16:42
# @File    : serializers.py.py
# @Author  : 守望@天空~

from rest_framework import serializers
from .models import mocks
from .utils import choices


class MockSerializer(serializers.ModelSerializer):
    class Meta:
        model = mocks
        fields = '__all__'
    id = serializers.CharField()
    status = serializers.ChoiceField(choices=choices.status)
    method=serializers.ChoiceField(choices=choices.methods)
    headers = serializers.JSONField()
    body_type = serializers.ChoiceField(choices=choices.types)
    body = serializers.CharField()