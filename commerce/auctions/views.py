from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from .models import *
#to do: fix showing winner of closed listing (get a maxBidUser)

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
    maxBid, maxBidUser = getMaxBid(listingID,bidUser)
    
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
                maxBid=bid
                maxBidUser = maxBid.user
                return redirect('listing', listingID=listingID)
            else:
                return render(request, "auctions/listing.html", {
                    "listings": listings,
                    "maxBid": maxBid,
                    "maxBidUser": maxBidUser,
                    "message": "Bid must be greater than current bid."
                    })   
        except ValueError: #means there was no maxBid, add this bid to list, new maxBid
            bid.save()
            return render(request, "auction/listing.html", {
                "listings": listings,
                "maxBid": bid
            })
    return render(request, "auctions/listing.html")


@login_required
def addComment(request, listingID):
    user = request.user
    
    if request.method == "POST":
        userComment = request.POST['comment']
        listing = Listing.objects.get(pk=listingID)
        comment = Comment(comment=userComment, user=user, listing=listing)
        comment.save()
        listing.comments.add(comment)
        comments = Comment.objects.filter(listing=listing)
        watchlist, created = Watchlist.objects.get_or_create(user=request.user)
        maxBid, maxBidUser = getMaxBid(listingID, user)
        
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "comments": comments,
            "watchlist": watchlist,
            "maxBid": maxBid,
            "maxBidUser": maxBidUser
        })

    return redirect('listing', listingID=listingID)
        
    

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

@login_required
def closeListing(request, listingID):
    listingToClose = Listing.objects.get(pk=listingID)
    listingToClose.isActive = False
    listingToClose.save()
    return HttpResponse("Listing Closed Successfully")


@login_required
def createListing(request):
    if request.method == "POST":
        user = request.user
        title = request.POST['title']
        description = request.POST['description']
        imageUrl = request.POST['imageUrl']
        
        category, created = Category.objects.get_or_create(category=request.POST['category'])
        tempListing = Listing(owner=user,title=title,description=description,imageUrl=imageUrl,category=category)
        tempListing.save()
        bid = Bid(amount=request.POST['bid'],user=user,listing=tempListing)
        bid.save()
        tempListing.bid = bid
        tempListing.save()
        
        
        return render(request, "auctions/createListing.html", {
            "message": f"Your listing: {title}, has been succesfully added!"
        })
    return render(request, "auctions/createListing.html")


def getMaxBid(listingID, bidUser):
    userListing = Listing.objects.get(pk=listingID)
    maxBid = Bid.objects.filter(listing=userListing) #gets only bids for this listing
    maxBid = maxBid.aggregate(Max('amount'))['amount__max'] #compare bids, get biggest bid
    try:
        maxBidUser = Bid.objects.get(amount=maxBid,user=bidUser,listing=userListing)
        maxBidUser = maxBidUser.user
    except Bid.DoesNotExist:
        maxBidUser = None  # Handle the case where there is no maxBidUser
    return maxBid, maxBidUser
        
              
def listing(request, listingID):
    # Get the specific listing based on listingID
    listing = Listing.objects.get(pk=listingID)
    bidUser = request.user
    # Get the maximum bid for this listing
    maxBid, maxBidUser = getMaxBid(listingID, bidUser)
    
    comments = Comment.objects.filter(listing=listing)

    # Render the template with the specific listing
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "maxBid": maxBid,
        "maxBidUser": maxBidUser,
        "comments": comments
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
    
        
