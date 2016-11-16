# bümerang API [![Build Status](https://travis-ci.com/CFedderly/bumerang-server.svg?token=4tb5XXwWhvkN4pTxLEdz&branch=master)](https://travis-ci.com/CFedderly/bumerang-server)
## Endpoints
* `/request`
  * To create a new request `POST` with the following parameters:
   ```JSON
   'title': 'Title of the request',
   'description': 'Details of the request', # not required
   'duration': x, # minutes
   'distance': x. # meters
   ```
* `/request/{id}`
  * To get a request send a `GET` with the `{id}` slug equal to the id of the desired request 
* `/profile`
  * To create a new profile request `POST` with the following parameters:
   ```JSON
   'facebook_id': 'The user's facebook id',
   'first_name': 'First name',
   'last_name': 'Last name',
   'description': 'The about section for the person',
   'phone_number': 'The user's phone number'.
   ```
* `/profile/{id}`
  * To get a profile send a `GET` with the `{id}` slug equal to the id of the desired profile
* `/profile/facebookid/{id}`
  * To get a profile send a `GET` with `{id}` equal to the desired user's facebook id
* `/profile/edit/{id}`
  * To edit an existing profile, send a `POST` with the `{id}` equal to the desired profile,
  along with any of the following parameters:
  ```JSON
  'description': 'The about section for the person',
  'phone_number': 'The user's phone number',
  'device_id': 'The device id as provided by Android'.
  ```
* `/offer`
  * To create a new offer `POST` with the following parameters:
  ```JSON
  'profile_id': profile_id, # id of user creating the request
  'borrow_id': borrow_id. # id of the request being responded to
  ```
* `/offer/{id}`
  * To get an offer, send a 'GET' with the `{id}` equal to the id of the desired offer entry

* `/offer/ids/{ids}`
  * To get a list of offers, send a 'GET' with the `{ids}` equal to a comma delimited list of borrow ids,
  eg. "offer/ids/37,28,11" or "offer/ids/18" 
