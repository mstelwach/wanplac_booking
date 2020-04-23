from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from reservation.forms import ReservationCreateForm, ReservationKayakFormSet, ReservationUpdateForm
from reservation.models import Reservation, Kayak, Route, StockDateKayak
from reservation.tasks import check_quantity_kayak


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
        return Reservation.objects.filter(user=self.request.user)


class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationCreateForm
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
            select_date = request.GET.get('selectDate')
            kayak = Kayak.objects.get(pk=kayak_pk)
            stock_date_kayak = StockDateKayak.objects.get(kayak=kayak, date=select_date)
            quantity_range = list(range(1, stock_date_kayak.stock + 1))
            return render(request,
                          'reservation/quantity_dropdown_list_options.html',
                          {'quantity_range': quantity_range})

        if request.is_ajax() and request.GET.get('selectDate'):
            select_date = request.GET.get('selectDate')
            kayaks_filter_date = Kayak.objects.filter(stockdatekayak__date=select_date)
            return render(request,
                          'reservation/kayak_select_date_dropdown_list.html',
                          {'kayaks_filter_date': kayaks_filter_date})
        return super(ReservationCreateView, self).get(request, *args, **kwargs)

    # GET DYNAMIC DATE FIELD VALUE, POST JSON DATA WITH EXCLUDE TIME
    def post(self, request, *args, **kwargs):
        exclude_time = []
        if request.is_ajax():
            select_date = request.POST.get('selectDate')
            reservations = Reservation.objects.filter(date=select_date)
            for reservation in reservations:
                exclude_time.append((reservation.time.hour, reservation.time.minute))
            return JsonResponse({'exclude_time': exclude_time})
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
                date = form.cleaned_data['date']
                for detail in kayaks.instance.details.all():
                    stock_date_kayak = StockDateKayak.objects.get(kayak=detail.kayak, date=date)
                    stock_date_kayak.stock -= detail.quantity
                    # if not stock_date_kayak.stock:
                    #     detail.kayak.available = False
                    # detail.kayak.save()
                    stock_date_kayak.save()
        return super(ReservationCreateView, self).form_valid(form)


class ReservationUpdateView(LoginRequiredMixin, UpdateView):
    model = Reservation
    form_class = ReservationUpdateForm
    template_name = 'reservation/update.html'
    success_url = reverse_lazy('reservation:list')

    def get_context_data(self, **kwargs):
        context = super(ReservationUpdateView, self).get_context_data(**kwargs)
        reservation = self.get_object()
        disable_date = []
        for detail in reservation.details.all():
            stock_date_kayak = StockDateKayak.objects.filter(kayak=detail.kayak)
            for stock_date in stock_date_kayak:
                if stock_date.stock < detail.quantity:
                    disable_date.append([stock_date.date.year, stock_date.date.month-1, stock_date.date.day])
        context['disable_date'] = disable_date
        return context

    # GET DYNAMIC DATE FIELD VALUE, POST JSON DATA WITH EXCLUDE TIME
    def post(self, request, *args, **kwargs):
        exclude_time = []
        if request.is_ajax():
            select_date = request.POST.get('selectDate')
            reservations = Reservation.objects.filter(date=select_date)
            for reservation in reservations:
                if reservation != self.get_object():
                    exclude_time.append((reservation.time.hour, reservation.time.minute))
            return JsonResponse({'exclude_time': exclude_time})
        return super(ReservationUpdateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        # reservation = self.get_object()
        if self.request.POST.get('full_phone'):
            form.instance.phone = self.request.POST.get('full_phone')
        # if reservation.date != form.cleaned_data['date']:
        #     for detail in reservation.details.all():
        #         stock_date_kayak = StockDateKayak.objects.get(kayak=detail.kayak, date=reservation.date)
        #         stock_date_kayak.stock += detail.quantity
        #         stock_date_kayak = StockDateKayak.objects.get(kayak=detail.kayak, date=form.cleaned_data['date'])
        #         stock_date_kayak.stock -= detail.quantity
        #
        return super(ReservationUpdateView, self).form_valid(form)


class ReservationDeleteView(LoginRequiredMixin, DeleteView):
    model = Reservation
    success_url = reverse_lazy('reservation:list')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        delete = super(ReservationDeleteView, self).delete(request, *args, **kwargs)
        return delete


class KayakListView(LoginRequiredMixin, ListView):
    model = Kayak
    template_name = 'kayak/list.html'


class RouteListView(LoginRequiredMixin, ListView):
    model = Route
    template_name = 'route/list.html'


# class ReservationPayUPaymentView(DetailView):
#     model = Reservation
#     template_name = 'reservation/payu_payment.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(ReservationPayUPaymentView, self).get_context_data(**kwargs)
#         context['payment_form'] = PaymentMethodForm(self.object.currency, initial={'order': self.object})
#         return context
