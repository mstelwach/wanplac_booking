from django.contrib import admin

from reservation.models import Reservation, Kayak, Route, ReservationDetail, StockDateKayak


class ReservationDetailInline(admin.TabularInline):
    model = ReservationDetail
    raw_id_fields = ['kayak']


class ReservationAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'user', 'route', 'date',
                    'time', 'status', 'payment', 'currency', 'created']
    inlines = [ReservationDetailInline]


admin.site.register(Reservation, ReservationAdmin)


class KayakAdmin(admin.ModelAdmin):
    list_display = ['name', 'kind', 'available', 'description', 'price']


admin.site.register(Kayak, KayakAdmin)


class RouteAdmin(admin.ModelAdmin):
    list_display = ['start', 'end', 'length', 'description']


admin.site.register(Route, RouteAdmin)


class StockDateKayakAdmin(admin.ModelAdmin):
    list_display = ['kayak', 'date', 'stock']


admin.site.register(StockDateKayak, StockDateKayakAdmin)
