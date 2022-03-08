from django.db import models
from acceso.models import User
class Wish(models.Model):
    wisher = models.CharField(max_length=50)
    item = models.CharField(max_length=50)
    desc = models.CharField(max_length=50)
    date_granted = models.DateField(null=True, blank=True)
    uploaded_by = models.ForeignKey(User, related_name = 'wishes', on_delete= models.CASCADE)
    users_who_liked = models.ManyToManyField(User, related_name="liked_wishes")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

# Create your models here.
