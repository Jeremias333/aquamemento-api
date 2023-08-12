from django.db import models

# Create your models here.
class Info(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    daily_goal = models.FloatField(null=False, blank=False)
    drank = models.FloatField(null=False, blank=False, default=0)
    reached_goal = models.BooleanField(default=False)

    person = models.ForeignKey("Person", on_delete=models.CASCADE, related_name="infos")
    class Meta:
        ordering = ["-created_at"]

class Container(models.Model):
    title = models.CharField(max_length=30, unique=True, blank=False, null=False)
    capacity = models.FloatField(null=False, blank=False) # in ml

class Person(models.Model):
    name = models.CharField(max_length=30, unique=True, blank=False, null=False)
    kg = models.FloatField(null=False, blank=False)

    # Above code is to archive the data of actual drinking info (Info model)
    now_drink = models.FloatField(null=False, blank=False, default=0)