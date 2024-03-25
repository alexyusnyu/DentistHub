from django.urls import path
from DentistBook.review.views import create_review, DentistsofficeReviewsListView, ClientReviewsListView, EditReviewView, \
    DeleteReviewView

urlpatterns = [
    path('create-review/<slug:slug>/', create_review, name='create-review'),
    path('reviews/<slug:slug>/', DentistsofficeReviewsListView.as_view(), name='dentistsoffice-reviews-list'),
    path('my-reviews/<int:pk>/', ClientReviewsListView.as_view(), name='client-reviews-list'),
    path('edit-review/<int:pk>/', EditReviewView.as_view(), name='edit-review'),
    path('delete-review/<int:pk>/', DeleteReviewView.as_view(), name='delete-review')
]