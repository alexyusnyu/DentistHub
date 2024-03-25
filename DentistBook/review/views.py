from datetime import datetime
from django.contrib.auth import mixins as auth_mixins
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic as views
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReviewForm
from .models import Review
from ..dentistsoffice.models import DentistsofficeProfile
from ..client.models import ClientProfile
from ..reservation.models import Reservation


@login_required
def create_review(request, slug):
    dentistsoffice = DentistsofficeProfile.objects.get(slug=slug)
    user = request.user
    user_is_client = hasattr(user, 'clientprofile')
    has_reserved = Reservation.objects.filter(user=user, dentistsoffice=dentistsoffice, date__lte=datetime.today(), time__lt=datetime.now()).exists()
    has_reviewed = Review.objects.filter(user=user, dentistsoffice=dentistsoffice).exists()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.dentistsoffice = dentistsoffice
            review.save()
            return redirect('dentistsoffice-details', slug=dentistsoffice.slug)

    else:
        form = ReviewForm()

    context = {
        'user_is_client': user_is_client,
        'has_reserved': has_reserved,
        'has_reviewed': has_reviewed,
        'dentistsoffice': dentistsoffice,
        'form': form,
    }

    return render(request, 'review/create-review.html', context)


class DentistsofficeReviewsListView(views.ListView):
    model = Review
    template_name = 'review/dentistsoffice-reviews-list.html'
    context_object_name = 'reviews'
    paginate_by = 6

    def get_queryset(self):
        dentistsoffice = get_object_or_404(DentistsofficeProfile, slug=self.kwargs['slug'])
        queryset = Review.objects.filter(dentistsoffice=dentistsoffice).order_by('-date_created')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dentistsoffice = get_object_or_404(DentistsofficeProfile, slug=self.kwargs['slug'])
        context['dentistsoffice'] = dentistsoffice

        return context


class ClientReviewsListView(auth_mixins.LoginRequiredMixin, views.ListView):
    model = Review
    template_name = 'review/client-reviews-list.html'
    context_object_name = 'reviews'
    paginate_by = 6

    def get_queryset(self):
        user = get_object_or_404(ClientProfile, pk=self.kwargs['pk'])
        queryset = Review.objects.filter(user=user.pk).order_by('-date_created')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(ClientProfile, pk=self.kwargs['pk'])
        context['user'] = user

        return context


class EditReviewView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    model = Review
    template_name = 'review/edit-review.html'
    fields = ['rating', 'comment']
    success_url = reverse_lazy('client-details')

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)


class DeleteReviewView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    model = Review
    template_name = 'review/delete-review.html'
    success_url = reverse_lazy('client-details')

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)
