from django.db import models
from django.utils import timezone
import datetime


class Complaint(models.Model):

    CATEGORY_CHOICES = [
        ('water', 'Water'),
        ('electricity', 'Electricity'),
        ('wifi', 'WiFi'),
        ('mess', 'Mess Food'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('inprogress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    student_name   = models.CharField(max_length=100)
    room_number    = models.CharField(max_length=10)
    category       = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description    = models.TextField()
    priority       = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    upvotes        = models.PositiveIntegerField(default=0)
    satisfaction   = models.PositiveIntegerField(null=True, blank=True)
    date_filed     = models.DateTimeField(auto_now_add=True)
    resolved_date  = models.DateTimeField(null=True, blank=True)

    @property
    def is_overdue(self):
        """Returns True if complaint is unresolved for more than 3 days."""
        if self.status == 'resolved':
            return False
        return timezone.now() - self.date_filed > datetime.timedelta(days=3)

    @property
    def remark_count(self):
        return self.remarks.count()

    def __str__(self):
        return f"{self.student_name} - {self.get_category_display()}"


class Remark(models.Model):
    complaint    = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='remarks')
    student_name = models.CharField(max_length=100)
    content      = models.TextField()
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.student_name} on {self.complaint}"
