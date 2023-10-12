from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Max
#todo, addbid: change to get max bid from bids specific to listing instead of max of all bids


from .models import *


def index(request):
    listings = Listing.objects.all()
    
    for listing in listings:
        return render(request, "auctions/index.html", {
            "listings": Listing.objects.all()
        })
 
@login_required        
def addBid(request, listing_id): #add bid to listing
    #create bid object, save bid
        #bid = bidamt and user, get user
    #get all bids
    #compare bids, get biggest bid
    #if this bid is the biggest, add to listing
    #display this bid
    bidUser = request.user
    if request.method == "POST":
        userListing = Listing.objects.get(pk=listing_id)
        bidAmount = request.POST['Bid']
        try: #check if bid amt is valid
            bidAmount = float(bidAmount) #tries to convert text to float, if successful, then valid value for bid
        except ValueError:
            return render(request, "auctions/listing.html", {
                "message": "Enter a valid number"
            })
        bid = Bid(amount=bidAmount, user=bidUser)
        maxBid = Bid.objects.filter(listing=userListing) #gets only bids for this listing
        maxBid = maxBid.aggregate(Max('amount'))['amount__max']
        try: #try convert maxBid to float
            maxBid = float(maxBid)
            if bidAmount > maxBid:
                bid.save()
                return render(request, "auctions/listing.html", {
                    "maxBid": bid
                })
                
        except ValueError: #means there was no maxBid, add this bid to list, new maxBid
            bid.save()
            return render(request, "auction/listing.html", {
                "maxBid": bid
            })      
    return render(request, "auctions/listing.html", {
            "maxBid": maxBid
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
