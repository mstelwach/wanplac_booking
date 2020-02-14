from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db import transaction
# from django.shortcuts import render
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, FormView

from reservation.forms import ReservationCreateUpdateForm, ReservationKayakFormSet
from reservation.models import Reservation
from reservation.tasks import check_quantity_kayak


def home_page(request):
    return render(request, 'index.html')


class Login(LoginView):
    template_name = 'reservation/login.html'
    form_class = AuthenticationForm

    def form_valid(self, form):
        check_quantity_kayak.delay()
        return super(Login, self).form_valid(form)


class Logout(LoginRequiredMixin, LogoutView):
    next_page = '/'


class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'reservation/list.html/'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationCreateUpdateForm
    template_name = 'reservation/create.html'
    success_url = reverse_lazy('reservation:list')

    def get_context_data(self, **kwargs):
        data = super(ReservationCreateView, self).get_context_data(**kwargs)

        if self.request.POST:
            data['kayaks'] = ReservationKayakFormSet(self.request.POST, instance=self.object)
        else:
            data['kayaks'] = ReservationKayakFormSet(instance=self.object)

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        kayaks = context['kayaks']
        with transaction.atomic():
            if not form.cleaned_data['first_name']:
                form.instance.first_name = self.request.user.first_name
            if not form.cleaned_data['last_name']:
                form.instance.last_name = self.request.user.last_name
            form.instance.user = self.request.user
            # self.object = form.save()
            if kayaks.is_valid():
                reservation = form.save()
                for form in kayaks:
                    kayak = form.save(commit=False)
                    kayak.reservation = reservation
                    kayak.save()

                # kayaks.instance = self.object
                # kayaks.save()
                for item in kayaks.instance.kayaks.all():
                    item.kayak.quantity -= item.quantity
                    item.kayak.save()
        return super(ReservationCreateView, self).form_valid(form)

