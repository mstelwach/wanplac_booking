# from _decimal import Decimal
#
#
# def new_payment_query_listener(sender, reservation=None, payment=None, **kwargs):
#     """
#     Here we fill only two obligatory fields of payment, and leave signal handler
#     """
#     payment.amount = Decimal(reservation.get_total_cost()).quantize(Decimal('.01'))
#     payment.currency = reservation.currency


# def payment_status_changed_listener(sender, instance, old_status, new_status, **kwargs):
#     """
#     Here we will actually do something, when payment is accepted.
#     E.g. lets change an order status.
#     """
#     if old_status != 'paid' and new_status == 'paid':
#         # Ensures that we process order only one
#         instance.reservation.status = 'active'
#         instance.reservation.save()


