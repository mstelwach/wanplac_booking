from django.contrib.auth.models import User
from django.db import models


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

    def __str__(self):
        return 'Model: {} | Stock: {} | {}'.format(self.name, self.stock, self.kind)


class Route(models.Model):
    start = models.CharField(max_length=64)
    end = models.CharField(max_length=64)
    length = models.CharField(max_length=16)
    description = models.TextField(blank=True)

    def __str__(self):
        return 'Route: {} --> {}'.format(self.start, self.end)


class Reservation(models.Model):

    STATUS_BOOKING = [
        ('unconfirmed', 'Unconfirmed'),
        ('active', 'Active'),
        ('completed', 'Completed')
    ]

    first_name = models.CharField(max_length=32, blank=True)
    last_name = models.CharField(max_length=32, blank=True)
    date = models.DateField()
    time = models.TimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    # kayak = models.ManyToManyField(Kayak, through='ReservationDetail')
    status = models.CharField(max_length=32, choices=STATUS_BOOKING, default=[0][0])
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Reservation: {} | Route: {} | Date: {}, {}'.format(self.user,
                                                                   self.route,
                                                                   self.date,
                                                                   self.time)


class ReservationDetail(models.Model):
    reservation = models.ForeignKey(Reservation, related_name='details', on_delete=models.CASCADE)
    kayak = models.ForeignKey(Kayak, related_name='reservation_kayaks', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

