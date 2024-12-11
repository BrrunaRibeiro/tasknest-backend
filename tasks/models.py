from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Category(models.Model):
    """
    Represents a category for tasks.
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Task(models.Model):
    """
    Represents a task in the TASKNEST application with detailed features.

    Attributes:
        title (str): The title of the task.
        description (str): A detailed description of the task.
        due_date (datetime): When the task is due.
        is_overdue (bool): Indicates if the task is overdue.
        attachment (CloudinaryField): An optional file attachment.
        owners (User): Users assigned to the task.
        priority (str): The priority level of the task.
        category (Category): The category of the task.
        state (str): The current state of the task (open, in progress, done).
        created_at (datetime): The date and time when the task was created.
        updated_at (datetime): The date/time when the task was last updated.
    """
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    STATE_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    is_overdue = models.BooleanField(default=False, editable=False)
    attachment = CloudinaryField('attachment', blank=True, null=True)
    owners = models.ManyToManyField(User, related_name='tasks')
    priority = models.CharField(
        max_length=6, choices=PRIORITY_CHOICES, default='medium'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True
    )
    state = models.CharField(
        max_length=11, choices=STATE_CHOICES, default='open'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Overrides the save method to set is_overdue based on due_date.
        """
        from django.utils import timezone
        self.is_overdue = self.due_date and self.due_date < timezone.now()
        super(Task, self).save(*args, **kwargs)
