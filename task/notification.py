# views.py
from django.conf import settings
# views.py

from push_notifications.models import GCMDevice, APNSDevice
from rest_framework.response import Response
from rest_framework.views import APIView


class SubscriptionView(APIView):
    def post(self, request, format=None):
        registration_id = request.data.get('registration_id')
        device_type = request.data.get('device_type')  # 'android' or 'ios'

        if not registration_id or not device_type:
            return Response({'error': 'Invalid data.'}, status=400)

        if device_type == 'android':
            GCMDevice.objects.get_or_create(registration_id=registration_id)
        elif device_type == 'ios':
            APNSDevice.objects.get_or_create(registration_id=registration_id)

        return Response({'message': 'Subscription successful.'}, status=201)


class SendNotificationView(APIView):
    def post(self, request, format=None):
        title = request.data.get('title')
        body = request.data.get('body')

        if not title or not body:
            return Response({'error': 'Invalid data.'}, status=400)

        # Customize notification options as needed
        notification_options = {
            'title': title,
            'body': body,
            'icon': settings.NOTIFICATION_ICON_URL,
            'sound': settings.NOTIFICATION_SOUND_URL,
            'vibrate': [200, 100, 200],
        }

        # Send push notification to all registered devices
        devices = GCMDevice.objects.all() | APNSDevice.objects.all()
        devices.send_message(None, extra=notification_options)

        return Response({'message': 'Push notification sent successfully.'}, status=200)
