# import requests

# access_token = 'b852dd05-4c24-4099-95e8-508e09cea02e'

# location_query = 'New Delhi'

# headers = {
#     'Authorization': f'Bearer {access_token}'
# }

# # Make the request to the Geocode API
# response = requests.get(f'https://atlas.mapmyindia.com/api/places/geocode?address={location_query}', headers=headers)


# # Parse the response
# if response.status_code == 200:
#     data = response.json()
#     print(data)
#     if data.get('copResults'):
#         # Extract latitude and longitude from the first result
#         latitude = data['copResults']['latitude']
#         longitude = data['copResults']['longitude']
#         print(f'Latitude: {latitude}, Longitude: {longitude}')
#     else:
#         print('No results found')
# else:
#     print(f'Error: {response.status_code}, {response.text}')


import requests

headers = {
    'User-Agent': 'YourAppName/1.0 (your.email@example.com)'  # Include your app name and email
}
location_query = 'New Delhi'
response = requests.get(f'https://nominatim.openstreetmap.org/search?q={location_query}&format=json&limit=1', headers=headers)

if response.status_code == 200:
    data = response.json()
    print(data)
    if data:
        latitude = data[0]['lat']
        longitude = data[0]['lon']
        print(f'Latitude: {latitude}, Longitude: {longitude}')
    else:
        print('No results found')
else:
    print(f'Error: {response.status_code}, {response.text}')
