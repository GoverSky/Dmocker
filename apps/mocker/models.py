from django.db import models
# Create your models here.
from .utils import choices
from shortuuidfield import ShortUUIDField

class mocks(models.Model):
    id = ShortUUIDField(editable=False, primary_key=True, verbose_name='ID')
    status = models.IntegerField(verbose_name="响应状态", choices=choices.status, default=200)
    method=models.IntegerField(verbose_name="请求", choices=choices.methods)
    headers = models.TextField(verbose_name="响应头")
    body_type = models.CharField(verbose_name="响应体类型", choices=choices.types, max_length=30)
    body = models.TextField(verbose_name="响应体")