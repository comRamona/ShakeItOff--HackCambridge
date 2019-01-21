#!/usr/bin/env python
import base64
import urllib
import json
from urllib.parse import urlencode, quote_plus
from urllib.request import Request
import requests
import os
#These are the secrets etc from Fitbit developer

def calories_to_steps(calorie_value):
    return round(calorie_value/40*1000)

def set_goal(calorie_goal):
    calorie_goal = round(calorie_goal)
    step_goal = calories_to_steps(calorie_goal)
    OAuthTwoClientID = os.environ("FITBIT_OAUTH")
    ClientOrConsumerSecret = os.environ["FITBIT_SECRET")

    #This is the Fitbit URL
    #TokenURL = "https://www.fitbit.com/oauth2/authorize"
    TokenURL = "https://api.fitbit.com/oauth2/token"
    #I got this from the first verifier part when authorising my application
    AuthorisationCode = os.environ["FITBIT_CODE")

    access_token = os.environ['FITBIT_TOKEN']
    headers = {'Authorisation': 'Bearer ' + access_token}
    url = 'https://api.fitbit.com/1/user/-/activities/goals/daily.json'


    #Start the request
    data = {'caloriesOut': int(calorie_goal), 'steps': int(step_goal)}
    DataEncoded = (urllib.parse.urlencode(data)).encode('utf-8')
    req = urllib.request.Request(url=url, data=DataEncoded)

    #Add the headers, first we base64 encode the client id and client secret with a : inbetween and create the authorisation header
    req.add_header('Authorization', 'Bearer ' + access_token)

    print(req.header_items())
    print(req.data)
    #Fire off the request
    try:
      response = urllib.request.urlopen(req)

      FullResponse = response.read()

      print("Output >>> " + FullResponse.decode('utf-8'))
      return calorie_goal, step_goal
    except urllib.error.HTTPError as e:
        print('*******')
        print(e.read())
