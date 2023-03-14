"""
models.py: Defines database models for the room management application.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    User model representing a user in the system.
    """
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('dpt_staff', 'Department Staff'),
        ('student', 'Student'),
    ]
    STATUS_CHOICES = [
        ('enrolled', 'Enrolled'),
        ('unenrolled', 'Unenrolled'),
    ]
    student_id = models.CharField(max_length=10, unique=True, null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='enrolled')
    rooms_access = models.ManyToManyField('Room', blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TaskList(models.Model):
    """
    TaskList model representing a list of tasks.
    """
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Task(models.Model):
    """
    Task model representing a single task.
    """
    description = models.TextField()
    completed = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)
    task_list = models.ForeignKey(TaskList, on_delete=models.CASCADE)
    recurrence_type = models.CharField(
        max_length=10,
        choices=[('none', 'None'), ('daily', 'Daily'), ('weekly', 'Weekly')],
        default='none'
    )
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Room(models.Model):
    """
    Room model representing a room in the building.
    """
    name = models.CharField(max_length=100)
    floor = models.IntegerField()
    persistent_note = models.TextField(blank=True)
    usual_configuration = models.TextField(blank=True)
    requested_infrastructure = models.TextField(blank=True)
    last_contact_attempt = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class RoomAssignment(models.Model):
    """
    RoomAssignment model representing the assignment of a room to a user.
    """
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    semester = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class RoomCheck(models.Model):
    """
    RoomCheck model representing a room check performed by student staff.
    """
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    room_issue = models.BooleanField(default=False)
    note = models.TextField(blank=True)
    student_staff = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class RoomCheckImage(models.Model):
    """
    RoomCheckImage model representing an image taken during a room check.
    """
    room_check = models.ForeignKey(RoomCheck, on_delete=models.CASCADE)
    image_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ContactAttempt(models.Model):
    """
    ContactAttempt model representing an attempt to contact occupants of a room.
    """
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()
    recipients = models.JSONField()
    email_content = models.TextField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class RoomImage(models.Model):
    """
    RoomImage model representing an image of a room.
    """
    IMAGE_TYPE_CHOICES = [
        ('default', 'Default'),
        ('floorplan', 'Floorplan'),
    ]
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    image_url = models.URLField()
    image_type = models.CharField(max_length=10, choices=IMAGE_TYPE_CHOICES, default='default')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
