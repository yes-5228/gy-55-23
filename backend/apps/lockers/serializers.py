from rest_framework import serializers

from .models import LockerCell, OpenAuditLog


class LockerCellSerializer(serializers.ModelSerializer):
    status_label = serializers.CharField(source="get_status_display", read_only=True)
    size_label = serializers.CharField(source="get_size_display", read_only=True)

    class Meta:
        model = LockerCell
        fields = [
            "id",
            "code",
            "zone",
            "size",
            "size_label",
            "status",
            "status_label",
            "temperature",
            "last_opened_at",
            "updated_at",
        ]


class OpenAuditLogSerializer(serializers.ModelSerializer):
    source_label = serializers.CharField(source="get_source_display", read_only=True)
    locker_cell_code = serializers.CharField(source="locker_cell.code", read_only=True)
    parcel_tracking_no = serializers.CharField(source="parcel.tracking_no", read_only=True, default=None)

    class Meta:
        model = OpenAuditLog
        fields = [
            "id",
            "locker_cell",
            "locker_cell_code",
            "source",
            "source_label",
            "operator",
            "parcel",
            "parcel_tracking_no",
            "opened_at",
            "note",
        ]
