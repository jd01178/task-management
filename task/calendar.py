import json
import os

from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from rest_framework import status

from .models import UserGoogleCredentials, ExternalCalendarEvent


def google_authenticate(request):
    flow = Flow.from_client_secrets_file(
        os.path.abspath(settings.GOOGLE_CALENDAR_CREDENTIALS_FILE),
        scopes=['https://www.googleapis.com/auth/calendar.readonly'],
        redirect_uri=f"{settings.SECURE_ROOT_URL}{reverse('task:google_callback')}"
    )

    authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
    request.session['google_auth_state'] = state
    print(state)
    return redirect(authorization_url)


def google_callback(request):
    state = request.session.get('google_auth_state', None)
    # need to get refresh token
    print(state)
    flow = Flow.from_client_secrets_file(
        os.path.abspath(settings.GOOGLE_CALENDAR_CREDENTIALS_FILE),
        scopes=['https://www.googleapis.com/auth/calendar.readonly'],
        state=state,
        redirect_uri=f"{settings.SECURE_ROOT_URL}{reverse('task:google_callback')}"
    )

    authorization_response = f"{settings.SECURE_ROOT_URL}{request.get_full_path()}"
    try:
        flow.fetch_token(authorization_response=authorization_response)

        credentials = flow.credentials
        user_cred, _ = UserGoogleCredentials.objects.get_or_create(
            user_id=request.user.id, account_type=UserGoogleCredentials.AccountType.GOOGLE_CALENDAR
        )
        user_cred.access_token = credentials.token
        user_cred.refresh_token = credentials.refresh_token
        user_cred.client_id = credentials.client_id
        user_cred.token_uri = credentials.token_uri
        user_cred.client_secret = credentials.client_secret
        user_cred.scopes = credentials.scopes
        user_cred.expiry = credentials.expiry
        user_cred.save()
    except Exception as e:
        print(e)

    return redirect(reverse('task:fetch_google_calendar_events', kwargs=dict(user_id=request.user.pk)))
    # Redirect to a success page or the next step in your authentication flow


def get_google_calendar_service(credentials):
    creds = Credentials.from_authorized_user_info(info=dict(
        access_token=credentials.access_token,
        refresh_token=credentials.refresh_token,
        token_uri='https://accounts.google.com/o/oauth2/token',
        client_id=credentials.client_id,
        client_secret=credentials.client_secret
    ))

    return build('calendar', 'v3', credentials=creds, cache_discovery=False)


def fetch_google_calendar_events(request, user_id):
    try:
        user_credentials = UserGoogleCredentials.objects.get(user_id=user_id)
        service = get_google_calendar_service(user_credentials)

        events = service.events().list(
            calendarId='primary',  # 'primary' refers to the user's primary calendar
            timeMin='2023-07-01T00:00:00Z',  # Set the minimum time to fetch events from
            maxResults=10,  # Set the number of events to retrieve
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        items = events.get('items', [])
        for item in items:
            item['start'] = item['start'].get('dateTime', item['start'].get('date'))
            item['end'] = item['end'].get('dateTime', item['end'].get('date'))
            ExternalCalendarEvent.objects.update_or_create(
                user_id=user_id, event_id=item['id'], defaults=dict(
                    html_link=item['htmlLink'],
                    title=item['summary'],
                    description=item.get('description', item['summary']),
                    start_date=item['start'],
                    end_date=item['end'],
                    meeting_link=item.get('hangoutLink', None),
                    account_type=ExternalCalendarEvent.CalendarType.GOOGLE_CALENDAR
                )
            )
        messages.success(request, 'Google calendar Events have been fetched successfully.')
        return redirect('task:tasks_calendar')

    except UserGoogleCredentials.DoesNotExist:
        return JsonResponse({'error': 'User credentials not found.'}, status=status.HTTP_404_NOT_FOUND)

    except HttpError as e:
        return JsonResponse(
            {'error': 'Failed to fetch events: {}'.format(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
