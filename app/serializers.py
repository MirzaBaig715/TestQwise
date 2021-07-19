from datetime import datetime

from rest_framework import serializers

from app.models import Todo


class TodoSerializer(serializers.ModelSerializer):
    days_since_completion = serializers.SerializerMethodField(read_only=True)

    def get_days_since_completion(self, instance):
        if instance.completion_time != None and instance.is_complete:
            duration = datetime.now().astimezone() - instance.completion_time
            return duration.days

    class Meta:
        model = Todo
        fields = ['id', 'title', 'completion_time', 'is_complete','created', 'days_since_completion']

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.is_complete = validated_data.get('is_complete', instance.is_complete)
        instance.completion_time = validated_data.get('completion_time', instance.completion_time)
        instance.save()
        return instance
