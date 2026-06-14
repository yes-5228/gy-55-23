from django.db.models import Count
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import LockerCell, OpenAuditLog
from .serializers import LockerCellSerializer, OpenAuditLogSerializer
from .services import open_locker_cell_manually


class LockerCellViewSet(viewsets.ModelViewSet):
    queryset = LockerCell.objects.all()
    serializer_class = LockerCellSerializer

    @action(detail=False, methods=["get"])
    def summary(self, request):
        total = LockerCell.objects.count()
        by_status = {
            item["status"]: item["count"]
            for item in LockerCell.objects.values("status").annotate(count=Count("id"))
        }
        return Response(
            {
                "total": total,
                "empty": by_status.get(LockerCell.Status.EMPTY, 0),
                "occupied": by_status.get(LockerCell.Status.OCCUPIED, 0),
                "open": by_status.get(LockerCell.Status.OPEN, 0),
                "maintenance": by_status.get(LockerCell.Status.MAINTENANCE, 0),
            }
        )

    @action(detail=True, methods=["post"])
    def mark_maintenance(self, request, pk=None):
        cell = self.get_object()
        cell.status = LockerCell.Status.MAINTENANCE
        cell.save(update_fields=["status", "updated_at"])
        return Response(self.get_serializer(cell).data)

    @action(detail=True, methods=["post"])
    def reset(self, request, pk=None):
        cell = self.get_object()
        cell.status = LockerCell.Status.EMPTY
        cell.last_opened_at = timezone.now()
        cell.save(update_fields=["status", "last_opened_at", "updated_at"])
        return Response(self.get_serializer(cell).data)

    @action(detail=True, methods=["post"])
    def open_manual(self, request, pk=None):
        operator = request.data.get("operator", "")
        note = request.data.get("note", "")
        cell = open_locker_cell_manually(pk, operator=operator, note=note)
        if not cell:
            return Response(
                {"success": False, "message": "柜格不存在或处于维护中，无法开箱。"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {
                "success": True,
                "message": f"柜格 {cell.code} 已人工开箱。",
                "cell": self.get_serializer(cell).data,
            }
        )

    @action(detail=False, methods=["get"])
    def open_audit_logs(self, request):
        logs = OpenAuditLog.objects.select_related("locker_cell", "parcel").all()
        return Response(OpenAuditLogSerializer(logs, many=True).data)
