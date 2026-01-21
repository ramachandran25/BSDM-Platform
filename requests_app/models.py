from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from decimal import Decimal

class ProjectRequest(models.Model):

    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('ESTIMATED', 'Estimated'),
        ('PAID', 'Paid'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CLOSED', 'Closed'),
    ]

    estimated_cost = models.DecimalField(
    	max_digits=10,
    	decimal_places=2,
    	null=True,
    	blank=True,
    	help_text="Estimated project cost"
    )

    request_id = models.CharField(max_length=20, unique=True, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='NEW'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.request_id:
            last = ProjectRequest.objects.order_by('-id').first()
            next_id = 1 if not last else last.id + 1
            self.request_id = f"PRJREQ{next_id:05d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.request_id

class RequestAttachment(models.Model):
    ATTACHMENT_TYPE_CHOICES = [
        ('USER', 'User Upload'),
        ('ADMIN', 'Admin Upload'),
    ]

    project_request = models.ForeignKey(
        ProjectRequest,
        related_name='attachments',
        on_delete=models.CASCADE
    )
    file = models.FileField(upload_to='request_attachments/')
    uploaded_by = models.CharField(
        max_length=10,
        choices=ATTACHMENT_TYPE_CHOICES
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project_request.request_id} - {self.file.name}"
