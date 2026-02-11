from django.db import models
from django.contrib.auth.models import User

class Feedback(models.Model):
    ISSUE_CHOICES = [
        # ('Pothole', 'Pothole'),
        # ('Street Light', 'Street Light Not Working'),
        ('Garbage', 'Garbage Dump'),
        ('Drainage', 'Drainage Blockage'),
        # ('Road Crack', 'Cracked or Damaged Road'),
        # ('Signage', 'Missing or Damaged Sign Board'),
        # ('Other', 'Other'),
    ]

    SEVERITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    issue_type = models.CharField(max_length=50, choices=ISSUE_CHOICES, default='Other')
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='Low')
    location = models.CharField(max_length=255, default='Unknown Location')
    landmark = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='feedback_images/', blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.issue_type} - {self.status} ({self.location})"
