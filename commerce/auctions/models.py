from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    pass

class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listingOwner")
    title = models.CharField(max_length=64) #name of listing
    description = models.CharField(max_length=1024) #allow for short description of item
    bid = models.ForeignKey('Bid',on_delete=models.CASCADE, related_name="startingBids",null=True,blank=True)
    imageUrl = models.TextField(max_length=5000,null=True)
    category = models.ForeignKey('Category',on_delete=models.CASCADE, related_name="categories",null=True)
    comments = models.ManyToManyField('Comment', related_name='listingComments',default=None)
    isActive = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{(self.title).capitalize()}"
    

class Bid(models.Model):
    amount = models.FloatField(null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="bidUsers")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bidListings",null=True)
    def __str__(self):
        return f"{self.amount} made by {self.user} for {self.listing}"
    
class Category(models.Model):
    category = models.CharField(max_length=64)
    listing = models.ManyToManyField(Listing,related_name="listings",blank=True)
    def __str__(self):
        return f"{self.category}"

class Comment(models.Model):
    comment = models.TextField() #comments
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="commentListing", default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userComment")
    
    def __str__(self):
        return f"{self.user} commented: '{self.comment}'"
    
#watchlist class
class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="watchlist")
    listings = models.ManyToManyField('Listing', related_name="watchlist_items")

    def __str__(self):
        return f"{self.user}'s Watchlist"

