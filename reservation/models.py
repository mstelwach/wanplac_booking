from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Kayak(models.Model):
    NUMBER_SEATS = [
        ('1', 'Jednoosobowy'),
        ('2', 'Dwuosobowy'),
        ('3', 'Trzyosobowy'),
        ('4', 'Czteroosobowy')
    ]

    name = models.CharField(max_length=32)
    kind = models.CharField(max_length=32, choices=NUMBER_SEATS)
    available = models.BooleanField()
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='kayak', blank=True)

    def __str__(self):
        return 'Model: {} - {} | Cena: {} PLN'.format(self.name,
                                                      self.get_kind_display(),
                                                      self.price)


class StockDateKayak(models.Model):
    kayak = models.ForeignKey(Kayak, on_delete=models.CASCADE)
    date = models.DateField()
    stock = models.IntegerField()

    def __str__(self):
        return 'Kajak: {} | Data: {} | Ilość: {}'.format(self.kayak.name,
                                                         self.date,
                                                         self.stock)


class Route(models.Model):
    start = models.CharField(max_length=64)
    end = models.CharField(max_length=64)
    length = models.CharField(max_length=16)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='route/%Y/%m/%d', blank=True)

    def __str__(self):
        return '{} -> {}'.format(self.start, self.end)


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
    # phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
    #                              message="Phone number must be entered in the format: '+999999999'. Up to 15 digits "
    #                                      "allowed.")
    # phone = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    phone = models.CharField(max_length=17, blank=True)
    currency = models.CharField(max_length=16, default='PLN')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Rezerwacja: {} | Trasa: {} | Data: {}, {}'.format(self.user,
                                                                  self.route,
                                                                  self.date,
                                                                  self.time)

    def get_total_cost(self):
        return sum(detail.get_cost() for detail in self.details.all())


class ReservationDetail(models.Model):
    reservation = models.ForeignKey(Reservation, related_name='details', on_delete=models.CASCADE)
    kayak = models.ForeignKey(Kayak, related_name='reservation_kayaks', on_delete=models.CASCADE)
    quantity = models.IntegerField(choices=[(0, '-------')] + [(number, str(number)) for number in range(1, 25)])

    def get_cost(self):
        return self.kayak.price * self.quantity

# getpaid.register_to_payment(Reservation, unique=False, related_name='payments')
