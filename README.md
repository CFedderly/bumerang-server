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
  * To create a new request `POST` with the following parameters:
   ```JSON
   'firstname': 'First name',
   'lastname': 'Last name',
   'description': 'The about section for the person'
   ```
* `/profile/{id}`
  * To get a profile send a `GET` with the `{id}` slug equal to the id of the desired profile 
