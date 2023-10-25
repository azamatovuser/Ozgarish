from django.db import models
from apps.account.models import Account


class Day(models.Model):
    day = models.CharField(max_length=221)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.day


class Task(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=221)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title