from django.db import models
from django.utils import timezone


class Process(models.Model):
    """
    Model to store legal process information.
    """
    process_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Process Number"
    )
    process_class = models.CharField(
        max_length=100,
        verbose_name="Process Class"
    )
    subject = models.TextField(
        verbose_name="Subject"
    )
    judge = models.CharField(
        max_length=200,
        verbose_name="Judge"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Created At"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated At"
    )

    class Meta:
        verbose_name = "Process"
        verbose_name_plural = "Processes"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.process_number} - {self.process_class}"

    @property
    def parties_count(self):
        """Return the number of parties in this process."""
        return self.parties.count()
