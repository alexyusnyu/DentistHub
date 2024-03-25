from django.db.models import Avg, Count
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import mixins as auth_mixins
from django.views import generic as views
from DentistBook.dentistsoffice.models import DentistsofficeProfile, DentistsofficeService, DentistsofficeWorkingHours, DentistsofficePicture
from DentistBook.review.models import Review


class EditDentistsofficeProfileView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    model = DentistsofficeProfile
    template_name = 'dentistsoffice/edit-dentistsoffice.html'
    fields = ['name', 'address', 'city', 'geolocation_latitude', 'geolocation_longitude', 'about', 'dentistsoffice_picture']

    def get_success_url(self):
        dentistsoffice = DentistsofficeProfile.objects.get(user=self.request.user)
        return reverse_lazy('dentistsoffice-details', kwargs={'slug': dentistsoffice.slug})

    def get_object(self, queryset=None):
        return DentistsofficeProfile.objects.get(user_id=self.request.user)

    def form_valid(self, form):
        if self.request.user != self.get_object().user:
            return redirect('home-page')

        result = super().form_valid(form)

        return result


class DentistsofficeProfileDetailsView(views.DetailView):
    model = DentistsofficeProfile
    template_name = 'dentistsoffice/dentistsoffice-details.html'
    context_object_name = 'dentistsoffice_profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dentistsoffice_rating = Review.objects.filter(dentistsoffice=self.object.pk).aggregate(Avg('rating'))['rating__avg']
        dentistsoffice_reviews_count = Review.objects.filter(dentistsoffice=self.object.pk).count()
        context['dentistsoffice_rating'] = dentistsoffice_rating
        context['dentistsoffice_reviews_count'] = dentistsoffice_reviews_count
        return context


class DentistsofficeListView(views.ListView):
    model = DentistsofficeProfile
    template_name = 'dentistsoffice/dentistsoffices-list.html'
    context_object_name = 'dentistsoffices'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(avg_rating=Avg('review__rating'))
        queryset = queryset.annotate(reviews_count=Count('review'))

        return queryset


class CreateDentistsofficeServiceView(auth_mixins.LoginRequiredMixin, views.CreateView):
    model = DentistsofficeService
    template_name = 'services/create-service.html'
    fields = ['category', 'service_name', 'price']

    def get_success_url(self):
        dentistsoffice = DentistsofficeProfile.objects.get(user=self.request.user)
        return reverse_lazy('dentistsoffice-details', kwargs={'slug': dentistsoffice.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dentistsoffice = DentistsofficeProfile.objects.get(user=self.request.user)
        context['dentistsoffice'] = dentistsoffice
        return context

    def form_valid(self, form):
        form.instance.dentistsoffice = DentistsofficeProfile.objects.get(user=self.request.user)
        return super().form_valid(form)


class EditDentistsofficeServiceView(auth_mixins.LoginRequiredMixin, auth_mixins.UserPassesTestMixin, views.UpdateView):
    model = DentistsofficeService
    template_name = 'services/edit-service.html'
    fields = ['category', 'service_name', 'price']

    def get_success_url(self):
        dentistsoffice = DentistsofficeProfile.objects.get(user=self.request.user)
        return reverse_lazy('service-details', kwargs={'pk': self.object.pk, 'slug': dentistsoffice.slug})

    def test_func(self):
        dentist = self.get_object()
        return dentist.dentistsoffice.user == self.request.user


class DeleteDentistsofficeServiceView(auth_mixins.LoginRequiredMixin, auth_mixins.UserPassesTestMixin, views.DeleteView):
    model = DentistsofficeService
    template_name = 'services/delete-service.html'

    def get_success_url(self):
        dentistsoffice = DentistsofficeProfile.objects.get(user=self.request.user)
        return reverse_lazy('dentistsoffice-details', kwargs={'slug': dentistsoffice.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dentistsoffice = DentistsofficeProfile.objects.get(user=self.request.user)
        context['dentistsoffice'] = dentistsoffice

    def test_func(self):
        dentist = self.get_object()
        return dentist.dentistsoffice.user == self.request.user


class DentistsofficeServicesDetailsView(views.DetailView):
    model = DentistsofficeService
    template_name = 'services/service-details.html'


class DentistsofficeWorkingHoursDetailsView(auth_mixins.LoginRequiredMixin, auth_mixins.UserPassesTestMixin, views.DetailView):
    model = DentistsofficeWorkingHours
    template_name = 'dentistsoffice/working-hours-details.html'

    def test_func(self):
        dentist = self.get_object()
        return dentist.dentistsoffice.user == self.request.user


class EditDentistsofficeWorkingHoursView(auth_mixins.LoginRequiredMixin, auth_mixins.UserPassesTestMixin, views.UpdateView):
    model = DentistsofficeWorkingHours
    template_name = 'dentistsoffice/edit-working-hours.html'
    fields = ['start_time', 'end_time']

    def get_success_url(self):
        dentistsoffice = DentistsofficeProfile.objects.get(user=self.request.user)
        return reverse_lazy('dentistsoffice-details', kwargs={'slug': dentistsoffice.slug})

    def test_func(self):
        dentist = self.get_object()
        return dentist.dentistsoffice.user == self.request.user


class CreateDentistsofficePictureView(auth_mixins.LoginRequiredMixin, views.CreateView):
    model = DentistsofficePicture
    template_name = 'pictures/create-picture.html'
    fields = ['image']

    def get_success_url(self):
        dentistsoffice = DentistsofficeProfile.objects.get(user=self.request.user)
        return reverse_lazy('dentistsoffice-details', kwargs={'slug': dentistsoffice.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dentistsoffice = DentistsofficeProfile.objects.get(user=self.request.user)
        context['dentistsoffice'] = dentistsoffice
        return context

    def form_valid(self, form):
        form.instance.dentistsoffice = DentistsofficeProfile.objects.get(user=self.request.user)
        return super().form_valid(form)


class DeleteDentistsofficePictureView(auth_mixins.LoginRequiredMixin, auth_mixins.UserPassesTestMixin, views.DeleteView):
    model = DentistsofficePicture
    template_name = 'pictures/delete-picture.html'

    def get_success_url(self):
        dentistsoffice = DentistsofficeProfile.objects.get(user=self.request.user)
        return reverse_lazy('dentistsoffice-details', kwargs={'slug': dentistsoffice.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dentistsoffice = DentistsofficeProfile.objects.get(user=self.request.user)
        context['dentistsoffice'] = dentistsoffice
        return context

    def test_func(self):
        dentist = self.get_object()
        return dentist.dentistsoffice.user == self.request.user


class DentistsofficePictureDetailsView(views.DetailView):
    model = DentistsofficePicture
    template_name = 'pictures/picture-details.html'
