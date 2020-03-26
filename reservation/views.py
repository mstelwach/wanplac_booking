from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from reservation.forms import ReservationCreateUpdateForm, ReservationKayakFormSet
from reservation.models import Reservation, Kayak
from reservation.tasks import check_quantity_kayak
import datetime


def home_page(request):
    return render(request, 'index.html')


class Login(LoginView):
    template_name = 'reservation/login.html'
    form_class = AuthenticationForm

    def form_valid(self, form):
        # check_quantity_kayak.delay('dssd')
        return super(Login, self).form_valid(form)


class Logout(LoginRequiredMixin, LogoutView):
    next_page = '/'


class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'reservation/list.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_context_data(self, *args, **kwargs):
        data = super(ReservationListView, self).get_context_data(*args, **kwargs)
        data['today'] = datetime.date.today()
        return data


class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationCreateUpdateForm
    template_name = 'reservation/create.html'

    def get_success_url(self):
        if self.object.payment == 'cash':
            return reverse_lazy('reservation:list')
        return reverse_lazy('reservation:payu-process', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(ReservationCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['kayaks'] = ReservationKayakFormSet(self.request.POST)
        else:
            context['kayaks'] = ReservationKayakFormSet()
        return context

    # GET SELECT KAYAK ID , POST DYNAMIC QUANTITY SELECT FIELD
    def get(self, request, *args, **kwargs):
        if request.is_ajax() and request.GET.get('selectKayakId'):
            kayak_pk = request.GET.get('selectKayakId')
            kayak = Kayak.objects.get(pk=kayak_pk)
            quantity_range = list(range(1, kayak.stock + 1))
            return render(request,
                          'reservation/quantity_dropdown_list_options.html',
                          {'quantity_range': quantity_range})
        if request.is_ajax() and request.GET.get('selectDate'):
            select_date = request.GET.get('selectDate')
            kayaks_select_date = Kayak.objects.filter(date=select_date)
            return render(request,
                          'reservation/kayak_select_date_dropdown_list.html',
                          {'kayaks_select_date': kayaks_select_date})

        return super(ReservationCreateView, self).get(request, *args, **kwargs)

    # GET DYNAMIC DATE FIELD VALUE, POST JSON DATA WITH EXCLUDE TIME
    def post(self, request, *args, **kwargs):
        exclude_date = []
        if request.is_ajax():
            select_date = request.POST.get('selectDate')
            reservations = Reservation.objects.filter(date=select_date)
            for reservation in reservations:
                exclude_date.append((reservation.time.hour, reservation.time.minute))
            return JsonResponse({'exclude_time': exclude_date})
        return super(ReservationCreateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        context = self.get_context_data()
        kayaks = context['kayaks']
        with transaction.atomic():
            if not form.cleaned_data['first_name']:
                form.instance.first_name = self.request.user.first_name
            if not form.cleaned_data['last_name']:
                form.instance.last_name = self.request.user.last_name
            form.instance.user = self.request.user
            reservation = form.save()
            if kayaks.is_valid():
                kayaks.instance = reservation
                kayaks.save()
                for detail in kayaks.instance.details.all():
                    detail.kayak.stock -= detail.quantity
                    if not detail.kayak.stock:
                        detail.kayak.available = False
                    detail.kayak.save()
        return super(ReservationCreateView, self).form_valid(form)


# class ReservationPayUPaymentView(DetailView):
#     model = Reservation
#     template_name = 'reservation/payu_payment.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(ReservationPayUPaymentView, self).get_context_data(**kwargs)
#         context['payment_form'] = PaymentMethodForm(self.object.currency, initial={'order': self.object})
#         return context
