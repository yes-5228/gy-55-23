from django.contrib import admin

from .models import LockerCell, OpenAuditLog


@admin.register(LockerCell)
class LockerCellAdmin(admin.ModelAdmin):
    list_display = ("code", "zone", "size", "status", "temperature", "updated_at")
    list_filter = ("zone", "size", "status")
    search_fields = ("code",)


@admin.register(OpenAuditLog)
class OpenAuditLogAdmin(admin.ModelAdmin):
    list_display = ("locker_cell", "source", "operator", "parcel", "opened_at", "note")
    list_filter = ("source", "opened_at")
    search_fields = ("locker_cell__code", "operator", "parcel__tracking_no")
    readonly_fields = ("opened_at",)
