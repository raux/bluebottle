from StringIO import StringIO

import requests
from django.core.files import File
from rest_framework import serializers

from bluebottle.members.serializers import UserCreateSerializer
from bluebottle.projects.serializers import ManageProjectSerializer
from bluebottle.bluebottle_drf2.serializers import ImageSerializer


class RemoteImageSerializer(ImageSerializer):
    def to_internal_value(self, data):
        with open('./bluebottle/bb_projects/test_images/upload.png') as file:
            data = File(file)

            data.content_type = 'image/png'

            return super(RemoteImageSerializer, self).to_internal_value(data)


class OwnerField(serializers.Field):
    def to_internal_value(self, data):
        import ipdb; ipdb.set_trace()


class UserSerializer(UserCreateSerializer):
    pass


class ProjectSerializer(ManageProjectSerializer):
    image = RemoteImageSerializer()

    def validate_status(self, value):
        return value
