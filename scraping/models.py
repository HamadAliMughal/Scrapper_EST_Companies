from django.db import models

class Company(models.Model):
    keyword = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    Company_Name = models.CharField(max_length=255, unique=True)
    Emails = models.TextField(blank=True, null=True)
    Phones = models.TextField(blank=True, null=True)
    Website = models.URLField(blank=True, null=True)
    Created_At = models.DateTimeField(auto_now_add=True)  # Automatically set when the record is created

    def __str__(self):
        return self.Company_Name
