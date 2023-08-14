import requests
from django.conf import settings

api_key = settings.GOOGLE_CALENDAR_API_KEY


def get_address_from_coordinates(latitude, longitude):
    url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={api_key}'

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and data['status'] == 'OK':
        # Extract the formatted address from the API response
        address = data['results'][0]['formatted_address']
        return address
    else:
        return None


def get_addresses(request, destination_address):
    user_latitude = request.COOKIES.get('latitude')
    user_longitude = request.COOKIES.get('longitude')

    origin_address = get_address_from_coordinates(user_latitude, user_longitude)
    destination_address = get_address_from_coordinates(destination_address.y, destination_address.x)
    return origin_address, destination_address


def get_estimated_distance(request, destination_address):
    # Get the user's current latitude and longitude (you can get this from the frontend using JavaScript and pass
    # it in the URL)
    origin_address, destination_address = get_addresses(request, destination_address)
    # Create the request URL for the Google Maps Distance Matrix API
    url = f'https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin_address}&destinations={destination_address}&key={api_key}'

    # Send the request to the API
    response = requests.get(url)
    data = response.json()
    # Parse the response and get the distance value
    try:
        distance = data['rows'][0]['elements'][0]['distance']['text']
        duration = data['rows'][0]['elements'][0]['duration']['text']
        return {'distance': distance, 'duration': duration}
    except (KeyError, IndexError):
        return {"error": "Unable to get distance estimation.", **data}


def get_route_suggestions(request, destination_address, travel_mode='driving'):
    origin_address, destination_address = get_addresses(request, destination_address)
    url = f'https://maps.googleapis.com/maps/api/directions/json?origin={origin_address}&destination={destination_address}&mode={travel_mode}&key={api_key}'

    response = requests.get(url)
    data = response.json()
    print(data)
    if response.status_code == 200 and data['status'] == 'OK':
        # Extract route information from the API response
        routes = data['routes']
        if routes:
            # For simplicity, we'll consider only the first route in the response
            route = routes[0]
            distance = route['legs'][0]['distance']['text']
            duration = route['legs'][0]['duration']['text']
            steps = [step['html_instructions'] for step in route['legs'][0]['steps']]

            return {
                'distance': distance,
                'duration': duration,
                'steps': steps
            }
    return None
