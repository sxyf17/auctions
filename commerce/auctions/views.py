from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Max
#todo, bidlisting: compare user bid to max bid in database, add to database if higher than max and also starting bid

from .models import *


def index(request):
    listings = Listing.objects.all()
    
    for listing in listings:
        return render(request, "auctions/index.html", {
            "listings": Listing.objects.all()
        })
        
def bidListing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    if request.method == "POST":
        bidAmount = request.POST['Bid']
        try:
            bid_amount = float(bidAmount) #tries to convert text to float, if successful, then valid value for bid
        except ValueError:
            return render(request, "auctions/listing.html", {
                "message": "Enter a valid number"
            })
        
        # if bid_amount > largestBid and bid_amount >=
        listing_id = request.POST.get('listing_id') #gets id of listing
        largestBid = Bids.objects.filter(id=listing_id).order_by('-bid_amount')[0]
        return render(request, "auctions/listing.html", {
            "biggest_bid": largestBid
        })
        
        
        
def listing(request):
    return render(request, "auctions/listing.html", {
        "listings": Listing.objects.all()
    })
    

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"] 

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
