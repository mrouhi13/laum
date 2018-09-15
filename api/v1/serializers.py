from rest_framework import serializers

from web.models import Data, Report


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ('title', 'subtitle', 'event', 'content', 'image', 'image_caption', 'reference', 'author')


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('data', 'body', 'reporter')

    def validate(self, attrs):
        if not attrs['data'].is_active:
            raise serializers.ValidationError()
        return attrs
