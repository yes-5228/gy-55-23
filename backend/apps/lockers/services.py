from django.db import transaction
from django.utils import timezone

from apps.parcels.models import Parcel
from .models import LockerCell, OpenAuditLog


@transaction.atomic
def open_locker_cell_manually(cell_id, operator="", note=""):
    cell = (
        LockerCell.objects.select_for_update()
        .filter(id=cell_id)
        .exclude(status=LockerCell.Status.MAINTENANCE)
        .first()
    )
    if not cell:
        return None

    now = timezone.now()
    cell.status = LockerCell.Status.OPEN
    cell.last_opened_at = now
    cell.save(update_fields=["status", "last_opened_at", "updated_at"])

    parcel = Parcel.objects.filter(
        locker_cell=cell,
        status__in=[Parcel.Status.STORED, Parcel.Status.RETURN_PENDING],
    ).first()

    OpenAuditLog.objects.create(
        locker_cell=cell,
        source=OpenAuditLog.Source.MANUAL,
        operator=operator,
        parcel=parcel,
        note=note,
    )

    return cell
