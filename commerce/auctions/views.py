from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from .models import *
#to do: fix imgurl, 'create listing' page, ability to close listing, comments,

def index(request):
    listings = Listing.objects.all()
    
    for listing in listings:
        return render(request, "auctions/index.html", {
            "listings": Listing.objects.all()
        })
 
@login_required        
def addBid(request, listingID): #add bid to listing
    bidUser = request.user
    listings = Listing.objects.all()
    userListing = Listing.objects.get(pk=listingID)
    maxBid = getMaxBid(listingID)
    
    if request.method == "POST":
        
        bidAmount = request.POST['Bid']
        try: #check if bid amt is valid
            bidAmount = float(bidAmount) #tries to convert text to float, if successful, then valid value for bid
        except ValueError:
            return render(request, "auctions/listing.html", {
                "message": "Enter a valid number"
            })
        bid = Bid(amount=bidAmount, user=bidUser, listing=userListing) #create bid object, save bid
        try: #try convert maxBid to float
            maxBid = float(maxBid)
            if bidAmount > maxBid: #if this bid is the biggest, add to listing
                bid.save()
                
                return redirect('listing', listingID=listingID)
            else:
                return render(request, "auctions/listing.html", {
                    "listings": listings,
                    "maxBid": maxBid,
                    "message": "Bid must be greater than current bid."
                    })   
        except ValueError: #means there was no maxBid, add this bid to list, new maxBid
            bid.save()
            return render(request, "auction/listing.html", {
                "listings": listings,
                "maxBid": bid
            })
    return render(request, "auctions/listing.html")
    

def categories(request):
    categories = Category.objects.all()
    listings = Listing.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories,
        "listings": listings
    })
    
def categoryListings(request, categoryID):
    category = Category.objects.get(pk=categoryID)
    listings = Listing.objects.filter(category=category)
    if category is not None:
        for listing in listings:
            return render(request, "auctions/categoryListings.html", {
                "listings": listings
            })
    
    return render(request, "auctions/categories.html", {
        "message": f"No items in this category: {category}"
    })

def closeListing(request, listingID):
    listingToDelete = Listing.objects.get(pk=listingID)
    listingToDelete.delete()
    return HttpResponse("Listing Deleted Successfully")

def getMaxBid(listingID):
    userListing = Listing.objects.get(pk=listingID)
    maxBid = Bid.objects.filter(listing=userListing) #gets only bids for this listing
    maxBid = maxBid.aggregate(Max('amount'))['amount__max'] #compare bids, get biggest bid
    return maxBid
        
              
def listing(request, listingID):
    listingImage = None
    maxBid = getMaxBid(listingID)

    return render(request, "auctions/listing.html", {
        "listings": Listing.objects.all(),
        "maxBid": maxBid
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
    
def watchlist(request, listingID):
    # Get the listing
    listing = Listing.objects.get(pk=listingID)

    # Get the user's watchlist or create it if it doesn't exist
    watchlist, created = Watchlist.objects.get_or_create(user=request.user)

    if listing in watchlist.listings.all():
        # If the listing is already in the watchlist, remove it
        watchlist.listings.remove(listing)
        
    else:
        # If the listing is not in the watchlist, add it
        watchlist.listings.add(listing)
        
    # Redirect back to the listing's detail page
    return HttpResponseRedirect(reverse("listing", args=[listingID]))

def viewWatchlist(request):
    watchlist = request.user.watchlist #gets user's watchlist and displays it
    if watchlist:
        listings = watchlist.listings.all()  # Get all listings in the watchlist
        return render(request, "auctions/watchlist.html", {
            "watchlist": watchlist,
            "listings": listings,
            "message": f"{request.user}'s Watchlist"
        })
    else:
        return render(request, "auctions/watchlist.html", {
            "message": "No items in watchlist"
        })
    
        
