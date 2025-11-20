from django.db import models
from django.conf import settings

MODALITIES = [
    ("xray", "X-Ray"),
    ("mri", "MRI"),
    ("ct", "CT"),
    ("ultrasound", "Ultrasound"),
]

REPORT_STATUS = [
    ("draft", "Draft"),
    ("final", "Finalized"),
    ("signed_off", "Signed Off"),
]


class RadiologyTest(models.Model):
    """Definitions of available radiology tests (admins / radiologists manage this)."""
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50, unique=True)
    modality = models.CharField(max_length=20, choices=MODALITIES)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.get_modality_display()})"


class RadiologyReport(models.Model):
    """Clinical report for a test. Independent of patient model."""
    test = models.ForeignKey(
        RadiologyTest,
        on_delete=models.PROTECT,
        related_name="reports"
    )
    patient_name = models.CharField(max_length=200)
    patient_identifier = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Optional patient id / MRN"
    )

    report_file = models.FileField(upload_to="radiology/reports/", null=True, blank=True)
    findings = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=REPORT_STATUS, default="draft")

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="radiology_created_reports"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    finalized_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="radiology_finalized_reports"
    )
    finalized_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Report #{self.pk} — {self.patient_name} / {self.test.name}"


class RadiologyRecord(models.Model):
    """Raw uploads (images or PDF) optionally attached to a test/report."""
    test = models.ForeignKey(
        RadiologyTest,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="records"
    )
    report = models.ForeignKey(
        RadiologyReport,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="records"
    )

    patient_name = models.CharField(max_length=150)
    patient_identifier = models.CharField(max_length=100, blank=True, null=True)

    pdf_report = models.FileField(upload_to="radiology/records/pdfs/", null=True, blank=True)
    image_file = models.ImageField(upload_to="radiology/records/images/", null=True, blank=True)

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        test_name = self.test.name if self.test else "NoTest"
        return f"{self.patient_name} - {test_name} - {self.uploaded_at:%Y-%m-%d %H:%M}"
