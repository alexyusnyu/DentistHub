from django.urls import path, include
from DentistBook.dentist.views import CreateDentistView, EditDentistView, DeleteDentistView, DentistDetailsView

urlpatterns = [
    path('create/', CreateDentistView.as_view(), name='create-dentist'),
    path('<int:pk>/edit/', EditDentistView.as_view(), name='edit-dentist'),
    path('<int:pk>/delete/', DeleteDentistView.as_view(), name='delete-dentist'),
    path('<int:pk>/details/', DentistDetailsView.as_view(), name='dentist-details')
]