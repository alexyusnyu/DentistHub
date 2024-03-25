from django.contrib.auth import mixins as auth_mixins
from django.urls import reverse_lazy
from django.views import generic as views
from DentistBook.dentist.models import Dentist
from DentistBook.dentistsoffice.models import DentistsofficeProfile


class CreateDentistView(auth_mixins.LoginRequiredMixin, views.CreateView):
    model = Dentist
    template_name = 'dentist/create-dentist.html'
    fields = ['name', 'about', 'dentist_picture']

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


class EditDentistView(auth_mixins.LoginRequiredMixin, auth_mixins.UserPassesTestMixin, views.UpdateView):
    model = Dentist
    template_name = 'dentist/edit-dentist.html'
    fields = ['name', 'about', 'dentist_picture']

    def get_success_url(self):
        return reverse_lazy('dentist-details', kwargs={'pk': self.object.pk})

    def test_func(self):
        dentist = self.get_object()
        return dentist.dentistsoffice.user == self.request.user


class DeleteDentistView(auth_mixins.LoginRequiredMixin, auth_mixins.UserPassesTestMixin, views.DeleteView):
    model = Dentist
    template_name = 'dentist/delete-dentist.html'

    def get_success_url(self):
        dentistsoffice = DentistsofficeProfile.objects.get(user=self.request.user)
        return reverse_lazy('dentistsoffice-details', kwargs={'slug': dentistsoffice.slug})

    def test_func(self):
        dentist = self.get_object()
        return dentist.dentistsoffice.user == self.request.user


class DentistDetailsView(views.DetailView):
    model = Dentist
    template_name = 'dentist/dentist-details.html'

