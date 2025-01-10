from django.db import models

class MainTable(models.Model):
    keyword = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    emails = models.TextField()
    phones = models.TextField()
    website = models.URLField()
    visited = models.BooleanField(default=False)  # New field, default is False

    def __str__(self):
        return self.company_name
