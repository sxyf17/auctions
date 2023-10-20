from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:listingID>", views.listing, name="listing"),
    path("createListing", views.createListing, name="createListing"),
    path("add/<int:listingID>", views.addBid, name="addBid"),
    path("watchlist/<int:listingID>", views.watchlist, name="watchlist"),
    path("viewWatchlist", views.viewWatchlist, name="viewWatchlist"),
    path("closeListing/<int:listingID>", views.closeListing, name="closeListing"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:categoryID>", views.categoryListings, name="categoryListings"),
    path("listing/<int:listingID>/addComment", views.addComment, name="addComment")
]
