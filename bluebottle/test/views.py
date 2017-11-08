from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from bluebottle.test import serializers


class ResourceList(APIView):
    serializer_map = {
        'user-preview': 'UserSerializer',
        'project': 'ProjectSerializer',
    }

    def post(self, request):
        serializer_cls = getattr(serializers, self.serializer_map[request.data['type']])
        serializer = serializer_cls(data=request.data['data'])

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
