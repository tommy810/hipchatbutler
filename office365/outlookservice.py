import requests
import uuid
import json

# Entity Definision
# https://msdn.microsoft.com/ja-jp/office/office365/api/complex-types-for-mail-contacts-calendar#UseOdataQueryParameters

outlook_api_endpoint = 'https://outlook.office.com/api/v2.0{0}'


# Generic API Sending
def make_api_call(method, url, token, user_email, payload=None, parameters=None):
    # Send these headers with all API calls
    headers = {'User-Agent': 'hipchatbutler/1.0',
               'Authorization': 'Bearer {0}'.format(token),
               'Accept': 'application/json',
               'X-AnchorMailbox': user_email}

    # Use these headers to instrument calls. Makes it easier
    # to correlate requests and responses in case of problems
    # and is a recommended best practice.
    request_id = str(uuid.uuid4())
    instrumentation = {'client-request-id': request_id,
                       'return-client-request-id': 'true'}

    headers.update(instrumentation)

    response = None

    if (method.upper() == 'GET'):
        response = requests.get(url, headers=headers, params=parameters)
    elif (method.upper() == 'DELETE'):
        response = requests.delete(url, headers=headers, params=parameters)
    elif (method.upper() == 'PATCH'):
        headers.update({'Content-Type': 'application/json'})
        response = requests.patch(url, headers=headers, data=json.dumps(payload), params=parameters)
    elif (method.upper() == 'POST'):
        headers.update({'Content-Type': 'application/json'})
        response = requests.post(url, headers=headers, data=json.dumps(payload), params=parameters)

    return response

def get_me(access_token):
  get_me_url = outlook_api_endpoint.format('/Me')

  # Use OData query parameters to control the results
  #  - Only return the DisplayName and EmailAddress fields
  query_parameters = {'$select': 'DisplayName,EmailAddress'}

  r = make_api_call('GET', get_me_url, access_token, "", parameters = query_parameters)

  if (r.status_code == requests.codes.ok):
    return r.json()
  else:
    return "{0}: {1}".format(r.status_code, r.text)

def get_my_events(access_token, user_email):
  get_events_url = outlook_api_endpoint.format('/Me/Events')
  # Use OData query parameters to control the results
  #  - Only first 10 results returned
  #  - Only return the Subject, Start, and End fields
  #  - Sort the results by the Start field in ascending order
  query_parameters = {'$top': '10',
                      '$select': 'Subject,Start,End',
                      '$orderby': 'Start/DateTime ASC'}

  r = make_api_call('GET', get_events_url, access_token, user_email, parameters=query_parameters)

  if (r.status_code == requests.codes.ok):
      return r.json()
  else:
      return "{0}: {1}".format(r.status_code, r.text)


def get_my_calendars(access_token, user_email):
    get_calendars_url = outlook_api_endpoint.format('/Me/Calendars')
    query_parameters = {'$top': '100',
                        '$select': 'Id, Name, Color',
                        '$orderby': 'Id ASC'}


    r = make_api_call('GET', get_calendars_url, access_token, user_email, parameters=query_parameters)

    if (r.status_code == requests.codes.ok):
        return r.json()
    else:
        return "{0}: {1}".format(r.status_code, r.text)
