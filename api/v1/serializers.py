from rest_framework import serializers

from web.models import Page, Report


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('title', 'subtitle', 'event', 'content', 'image', 'image_caption', 'reference', 'author')


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('page', 'body', 'reporter')

    def validate(self, attrs):
        if not attrs['page'].is_active:
            raise serializers.ValidationError()
        return attrs
