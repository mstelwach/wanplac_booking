from django.contrib.auth.models import User
from django.db import models


class Kayak(models.Model):
    name = models.CharField(max_length=32)
    quantity = models.IntegerField()
    available = models.BooleanField()

    def __str__(self):
        return 'Model: {} | Quantity: {}'.format(self.name, self.quantity)


class Route(models.Model):
    name = models.CharField(max_length=64)
    length = models.CharField(max_length=16)

    def __str__(self):
        return 'Route: {} --> Length: {}'.format(self.name, self.length)


class Reservation(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    term = models.DateField()
    time = models.TimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # kayak = models.ManyToManyField(Kayak, through='ReservationDetail')
    route = models.ForeignKey(Route, on_delete=models.CASCADE)

    def __str__(self):
        return 'Reservation: {} | Route: {} | Term: {}-{}'.format(self.user,
                                                                  self.route,
                                                                  self.term,
                                                                  self.time)


class ReservationItem(models.Model):
    reservation = models.ForeignKey(Reservation, related_name='kayaks', on_delete=models.CASCADE)
    kayak = models.ForeignKey(Kayak, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

# class ReservationDetail(models.Model):
#     reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
#     kayak = models.ForeignKey(Kayak, on_delete=models.CASCADE)
#     quantity_kayak = models.IntegerField()
