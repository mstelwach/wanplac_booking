from django.contrib import admin

from reservation.models import Reservation, Kayak, Route, ReservationItem


class ReservationItemInline(admin.TabularInline):
    model = ReservationItem
    raw_id_fields = ['kayak']


class ReservationAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'user', 'route', 'term', 'time']
    inlines = [ReservationItemInline]


admin.site.register(Reservation, ReservationAdmin)


class KayakAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'available']


admin.site.register(Kayak, KayakAdmin)


class RouteAdmin(admin.ModelAdmin):
    list_display = ['name', 'length']


admin.site.register(Route, RouteAdmin)