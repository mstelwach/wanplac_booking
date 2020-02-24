# import django_tables2 as tables
#
# from reservation.models import Reservation
#
#
# class ReservationTable(tables.Table):
#     # actions = tables.TemplateColumn(template_name='reservation/table_actions.html', verbose_name="Actions",
#     #                                 orderable=False)
#
#     class Meta:
#         model = Reservation
#         template = 'tables2_bootstrap4.html'
#         fields = ['first_name', 'last_name', 'term', 'time', 'route']
