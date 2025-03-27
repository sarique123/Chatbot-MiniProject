from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.utils.timezone import now, timedelta

# Custom User Model
class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('staff', 'Staff'),
        ('visitor', 'Visitor'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    preferred_language = models.CharField(max_length=50, default='en')

    # Fix conflicts with Django's default auth.User model
    groups = models.ManyToManyField(
        "auth.Group", related_name="custom_user_groups", blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission", related_name="custom_user_permissions", blank=True
    )

    def __str__(self):
        return self.username

# User Queries Table
class UserQuery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="queries")
    query_text = models.TextField(db_index=True)  # 🔹 Optimized for faster searching
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Query by {self.user.username} at {self.timestamp}"


# FAQs Table
class FAQ(models.Model):
    question = models.CharField(max_length=255,unique=True, db_index=True)  # 🔹 Index for faster lookup
    answer = models.TextField()
    category = models.CharField(max_length=100, db_index=True)  # 🔹 Index for filtering
    language = models.CharField(max_length=50, default='en')

    def __str__(self):
        return self.question


#  Query Cache Table
def default_expiration():
    return now() + timedelta(days=7)  # This function will return the correct default value

class QueryCache(models.Model):
    query_text = models.CharField(max_length=500, db_index=True)  # 🔹 Index for lookup
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField(default=default_expiration)  # Use function reference

    def __str__(self):
        return f"Cache for query: {self.query_text[:50]}"


#  User Query Patterns Table
class UserQueryPattern(models.Model):
    base_query = models.ForeignKey(FAQ, on_delete=models.CASCADE, related_name="patterns")
    query_variation = models.CharField(max_length=500,unique=True, db_index=True)
    response = models.TextField()

    def __str__(self):
        return self.query_variation



# Event Logs Table
class EventLog(models.Model):
    query = models.ForeignKey(UserQuery, on_delete=models.CASCADE, related_name="logs")
    response_time = models.FloatField()  # 🔹 In seconds
    api_calls = models.IntegerField(default=0)
    cache_hit = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log for Query {self.query.id}"


# Campus Events Table
class CampusEvent(models.Model):
    event_name = models.CharField(max_length=255, db_index=True)  # 🔹 Indexed for faster filtering
    event_date = models.DateField()
    event_time = models.TimeField()
    location = models.CharField(max_length=255)
    details = models.TextField()

    def __str__(self):
        return self.event_name