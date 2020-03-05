from django.apps import AppConfig
from getpaid import signals


class ReservationConfig(AppConfig):
    name = 'reservation'
    verbose_name = 'Reservations'

    def ready(self):
        from . import signals as listeners
        signals.new_payment_query.connect(listeners.new_payment_query_listener)
        # signals.payment_status_changed.connect(listeners.payment_status_changed_listener)
