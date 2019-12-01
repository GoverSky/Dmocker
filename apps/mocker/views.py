# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .utils import content_type
from .serializers import  MockSerializer
from .models import mocks
from django.http import Http404
import json

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def mock_data(request, pk, format=None):
    def get_object(pk):
        try:
            return mocks.objects.get(pk=pk)
        except mocks.DoesNotExist:
            raise Http404

    serializer = MockSerializer(get_object(pk))
    data= serializer.data
    return Response(json.loads(data['body']), status=data['status'], headers=json.loads(data['headers']),
                    content_type=data['body_type'])

