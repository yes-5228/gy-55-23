from django.db import models


class LockerCell(models.Model):
    class Size(models.TextChoices):
        SMALL = "small", "小"
        MEDIUM = "medium", "中"
        LARGE = "large", "大"

    class Status(models.TextChoices):
        EMPTY = "empty", "空闲"
        OCCUPIED = "occupied", "已占用"
        OPEN = "open", "已开门"
        MAINTENANCE = "maintenance", "维护中"

    code = models.CharField(max_length=20, unique=True)
    zone = models.CharField(max_length=30, default="A区")
    size = models.CharField(max_length=20, choices=Size.choices, default=Size.MEDIUM)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.EMPTY)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, default=24)
    last_opened_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["zone", "code"]

    def __str__(self):
        return f"{self.zone}-{self.code}"


class OpenAuditLog(models.Model):
    class Source(models.TextChoices):
        PICKUP = "pickup", "取件开箱"
        MANUAL = "manual", "人工开箱"

    locker_cell = models.ForeignKey(
        LockerCell,
        on_delete=models.PROTECT,
        related_name="open_audit_logs",
    )
    source = models.CharField(max_length=20, choices=Source.choices)
    operator = models.CharField(max_length=100, blank=True)
    parcel = models.ForeignKey(
        "parcels.Parcel",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="open_audit_logs",
    )
    opened_at = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["-opened_at"]

    def __str__(self):
        return f"{self.locker_cell} - {self.get_source_display()} at {self.opened_at}"
