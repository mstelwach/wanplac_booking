from __future__ import absolute_import, unicode_literals

from celery import shared_task
import datetime

from reservation.models import Reservation, Kayak


@shared_task
def check_quantity_kayak():
    now = datetime.date.today()
    yesterday = now - datetime.timedelta(days=1)
    queryset = Reservation.objects.filter(term__endswith=yesterday)
    d = {}
    for reservation in queryset:
        for item in reservation.kayaks.all():
            if item.kayak.name not in d:
                d[item.kayak.name] = item.quantity
            else:
                d[item.kayak.name] += item.quantity

        object = Reservation.objects.get(pk=reservation.id)
        object.delete()

    for name, quantity in d.items():
        object = Kayak.objects.get(name=name)
        object.quantity += quantity
        object.save()

    return 'Baza zauktalizowana: {} kajaki wróciły do nas!'.format(sum(d.values()))
