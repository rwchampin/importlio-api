import requests
from rest_framework.response import Response

def get_user_location():
    url = 'http://ip-api.com/json'
    
    # make the request
    response = requests.get(url)
    
    # if the request was successful
    if(response.status_code == 200):
        # get the response json
        response_json = response.json()
        
        # get the user's location
        user_location = response_json['city'] + ', ' + response_json['regionName'] + ', ' + response_json['country']
        import pdb; pdb.set_trace()
        # return the user's location
        return user_location
    else:
        # return not found response
        return Response({'detail': 'User location not found.'}, status=status.HTTP_404_NOT_FOUND)