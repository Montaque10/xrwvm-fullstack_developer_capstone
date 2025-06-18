# Uncomment the required imports before adding the code

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.views.decorators.csrf import csrf_exempt
import requests
from django.conf import settings
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
# from .populate import initiate


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

# Create a `logout_request` view to handle sign out request
def logout_user(request):
    """
    Handles user logout requests.
    Terminates the user's session and returns an empty username in JSON response.
    """
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)

# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    context = {}
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False
    email_exist = False
    try:
        User.objects.get(username=username)
        username_exist = True
    except User.DoesNotExist:
        logger.debug("{} is new user".format(username))

    if not username_exist:
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,password=password, email=email)
        login(request, user)
        data = {"userName":username,"status":"Authenticated"}
        return JsonResponse(data)
    else :
        data = {"userName":username,"error":"Already Registered"}
        return JsonResponse(data)

# Update the `get_dealerships` view to render the index page with
# a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "http://localhost:3030/fetchDealers"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Return JSON response
        return JsonResponse(dealerships, safe=False)

# Create a `get_dealer_reviews` view to render the reviews of a dealer
def get_dealer_reviews(request, dealer_id):
    if request.method == "GET":
        url = f"http://localhost:3030/fetchReviews/dealer/{dealer_id}"
        # Get reviews from the URL
        reviews = get_request(url)
        # Return JSON response
        return JsonResponse(reviews, safe=False)

# Create a `get_dealer_details` view to render the dealer details
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = f"http://localhost:3030/fetchDealer/{dealer_id}"
        # Get dealer details from the URL
        dealer_details = get_request(url)
        # Return JSON response
        return JsonResponse(dealer_details, safe=False)

# Create a `add_review` view to submit a review
@csrf_exempt
def add_review(request):
    if request.method == "POST":
        url = "http://localhost:3030/insert_review"
        review = json.loads(request.body)
        json_payload = {"review": review}
        # print(json_payload)
        result = post_request(url, json_payload, dealerId=review.get("dealership"))
        if int(result.status_code) == 200:
            print("Review posted successfully")
        else:
            print("Failed to post review")
        return HttpResponse("Review posted successfully")

# Create an `analyze_review_sentiments` view to call Watson NLU and analyze text
def analyze_review_sentiments(request):
    if request.method == "GET":
        text = request.GET.get("text")
        language = "en"
        version = "2022-04-01"
        authenticator = IAMAuthenticator("YOUR_API_KEY")
        natural_language_understanding = NaturalLanguageUnderstandingV1(
            version=version, authenticator=authenticator
        )
        natural_language_understanding.set_service_url(
            "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/YOUR_INSTANCE_ID"
        )
        response = natural_language_understanding.analyze(
            text=text+"hello hello hello", features=Features(sentiment=SentimentOptions(targets=[text+"hello hello hello"]))
        ).get_result()
        label = json.dumps(response, indent=2)
        label = response['sentiment']['document']['label']
        return JsonResponse({"label": label})

# Create a `get_dealers_from_cf` function to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Return the raw JSON data
        return json_result
    return []

# Create a `get_request` to make HTTP GET requests
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
def post_request(url, json_payload, **kwargs):
    print(f"POST to {url}")
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
    except:
        print("An error occurred while making POST request. ")
    status_code = response.status_code
    print(f"With status {status_code}")
    return response

# Create a CarDealer class to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name
