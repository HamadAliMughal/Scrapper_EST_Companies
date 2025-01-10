from django.db import models

class ScrappingToBe(models.Model):
    keyword = models.CharField(max_length=255)
    state = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.keyword} - {self.state}"
