from rest_framework import serializers

from webapp.models import Data, Report


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ('title', 'subtitle', 'event', 'content', 'image', 'image_caption', 'reference', 'author')


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('data','body', 'reporter')
