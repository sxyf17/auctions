from django.contrib.auth.models import AbstractUser
from django.db import models




class User(AbstractUser):
    pass

class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listingOwner")
    title = models.CharField(max_length=64) #name of listing
    description = models.CharField(max_length=1024) #allow for short description of item
    startingBid = models.ForeignKey('Bids',on_delete=models.CASCADE, related_name="startingBids",null=True)
    imageUrl = models.CharField(max_length=1024,null=True)
    listingCategory = models.ForeignKey('Category',on_delete=models.CASCADE, related_name="categories",null=True)
    
    def __str__(self):
        return f"{(self.title).capitalize()}"
    

class Bids(models.Model):
    bid_amount = models.PositiveIntegerField()
    bid_listing = models.ForeignKey(Listing, on_delete=models.CASCADE,related_name="bidListings")
    bid_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="bidUsers")
    def __str__(self):
        return f"{self.bid_amount}"
    
class Category(models.Model):
    category = models.CharField(max_length=64)

class Comments(models.Model):
    comment = models.CharField(max_length=256) #comments
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userComment")
    listingComment = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listingComment")
    
    def __str__(self):
        return f"{self.author} commented: '{self.comment}', on '{self.listingComment}'"
    
#watchlist class


