# views.py

import requests
from django.shortcuts import redirect, render
from msal import ConfidentialClientApplication


def microsoft_authenticate(request):
    # Your Azure AD application settings
    client_id = 'YOUR_CLIENT_ID'
    client_secret = 'YOUR_CLIENT_SECRET'
    redirect_uri = 'https://your-django-app.com/microsoft/callback/'

    scopes = ['User.Read', 'Calendars.ReadWrite']  # Adjust the required scopes as needed

    authority = 'https://login.microsoftonline.com/YOUR_TENANT_ID'

    app = ConfidentialClientApplication(
        client_id,
        authority=authority,
        client_credential=client_secret
    )

    # Get the Microsoft authorization URL
    auth_url = app.get_authorization_request_url(
        scopes,
        redirect_uri=redirect_uri
    )

    # Redirect the user to Microsoft login
    return redirect(auth_url)


def microsoft_callback(request):
    # Handle the callback after the user logs in
    client_id = 'YOUR_CLIENT_ID'
    client_secret = 'YOUR_CLIENT_SECRET'
    redirect_uri = 'https://your-django-app.com/microsoft/callback/'

    app = ConfidentialClientApplication(
        client_id,
        authority=authority,
        client_credential=client_secret
    )

    token = app.acquire_token_by_authorization_code(
        code=request.GET.get('code'),
        scopes=['User.Read', 'Calendars.ReadWrite'],
        redirect_uri=redirect_uri
    )

    # Store the acquired token data for the authenticated user (e.g., using UserMicrosoftCredentials model)



    access_token = token['access_token']

    # Use the access_token to make requests to Microsoft Graph API
    # For example, get the user's events:
    response = requests.get('https://graph.microsoft.com/v1.0/me/events',
                            headers={'Authorization': f'Bearer {access_token}'})
    events_data = response.json()

    # Process the events_data as needed

    return render(request, 'microsoft_calendar.html', {'events': events_data})
