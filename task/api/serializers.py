from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from task.maps import get_estimated_distance, get_route_suggestions
from task.models import Location, Task, ExternalCalendarEvent, Progress


class LocationSerializer(ModelSerializer):
    tasks = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Location
        fields = ['name', 'address', 'city', 'county', 'postcode', 'coordinates', 'tasks']

    @staticmethod
    def get_tasks(obj):
        return obj.tasks.all().count()


class TaskSerializer(ModelSerializer):
    location = LocationSerializer()
    estimated_distance = serializers.SerializerMethodField(read_only=True)
    estimated_time = serializers.SerializerMethodField(read_only=True)
    route_suggestion = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Task
        fields = ['title', 'description', 'location', 'estimated_distance', 'start_date', 'end_date', 'priority',
                  'task_type', 'estimated_time', 'route_suggestion', 'id']

    def get_estimated_distance(self, obj):
        request = self.context.get('request')
        distance = get_estimated_distance(request, obj.location.coordinates)
        if distance.get('distance'):
            return distance.get('distance')
        return None

    def get_estimated_time(self, obj):
        request = self.context.get('request')
        distance = get_estimated_distance(request, obj.location.coordinates)
        if distance.get('duration'):
            return distance.get('duration')
        return None

    def get_route_suggestion(self, obj):
        request = self.context.get('request')
        suggestion = get_route_suggestions(request, obj.location.coordinates)
        if suggestion:
            return suggestion
        return None


class CalendarTaskSerializer(ModelSerializer):
    start = serializers.SerializerMethodField(read_only=True)
    end = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Task
        fields = ['title', 'start', 'end', 'id']

    @staticmethod
    def get_start(obj):
        print(obj.start_date)
        return obj.start_date

    @staticmethod
    def get_end(obj):
        print(obj.end_date)
        return obj.end_date


class CalendarEventsSerializer(ModelSerializer):
    start = serializers.SerializerMethodField(read_only=True)
    end = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ExternalCalendarEvent
        fields = ['title', 'start', 'end', 'id', 'event_id']

    @staticmethod
    def get_start(obj):
        return obj.start_date

    @staticmethod
    def get_end(obj):
        return obj.end_date


class TaskProgressSerializer(ModelSerializer):
    task = TaskSerializer()

    class Meta:
        model = Progress
        fields = ['task', 'progress', 'created', 'updated']
