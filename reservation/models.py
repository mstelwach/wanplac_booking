from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Kayak(models.Model):

    NUMBER_SEATS = [
        ('1', 'Jednoosobowy'),
        ('2', 'Dwuosobowy'),
        ('3', 'Trzyosobowy')
    ]

    name = models.CharField(max_length=32)
    kind = models.CharField(max_length=32, choices=NUMBER_SEATS)
    stock = models.IntegerField()
    available = models.BooleanField()
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField()

    def __str__(self):
        return 'Model: {} | Stock: {} | {} | Cena: {} PLN'.format(self.name, self.stock, self.get_kind_display(), self.price)


class Route(models.Model):
    start = models.CharField(max_length=64)
    end = models.CharField(max_length=64)
    length = models.CharField(max_length=16)
    description = models.TextField(blank=True)

    def __str__(self):
        return 'Route: {} --> {}'.format(self.start, self.end)


PAYMENT_METHOD = [
    ('payu', 'PayU'),
    ('paypal', 'PayPal'),
    ('cash', 'Cash Payment'),
]

STATUS_BOOKING = [
    ('unconfirmed', 'Unconfirmed'),
    ('active', 'Active'),
    ('completed', 'Completed')
]


class Reservation(models.Model):
    first_name = models.CharField(max_length=32, blank=True)
    last_name = models.CharField(max_length=32, blank=True)
    date = models.DateField()
    time = models.TimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    status = models.CharField(max_length=32, choices=STATUS_BOOKING, default='unconfirmed')
    payment = models.CharField(max_length=64, choices=PAYMENT_METHOD)
    paid = models.BooleanField(default=False)
    phone = PhoneNumberField()
    currency = models.CharField(max_length=16, default='PLN')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Reservation: {} | Route: {} | Date: {}, {}'.format(self.user,
                                                                   self.route,
                                                                   self.date,
                                                                   self.time)

    def get_total_cost(self):
        return sum(detail.get_cost() for detail in self.details.all())


class ReservationDetail(models.Model):
    reservation = models.ForeignKey(Reservation, related_name='details', on_delete=models.CASCADE)
    kayak = models.ForeignKey(Kayak, related_name='reservation_kayaks', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def get_cost(self):
        return self.kayak.price * self.quantity


# getpaid.register_to_payment(Reservation, unique=False, related_name='payments')
