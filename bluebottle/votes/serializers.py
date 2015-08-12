from bluebottle.votes.models import Vote
from bluebottle.bb_accounts.serializers import UserPreviewSerializer
from rest_framework import serializers


class VoteSerializer(serializers.ModelSerializer):
    voter = UserPreviewSerializer(read_only=True)
    project = serializers.SlugRelatedField(source='project', slug_field='slug')

    class Meta:
        model = Vote
        fields = ('id', 'voter', 'project', 'created')