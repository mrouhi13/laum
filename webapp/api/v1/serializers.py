from rest_framework import serializers

from webapp.models import Data


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ('title', 'subtitle', 'ann_date', 'content', 'image', 'image_caption', 'reference', 'author')
