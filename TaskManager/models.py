from django.db import models


class Status(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Task(models.Model):
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='tasks',
        null=True, blank=True
    )
    title = models.CharField(max_length=50)
    description = models.TextField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name="status")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title