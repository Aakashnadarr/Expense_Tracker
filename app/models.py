from django.db import models
import uuid
from django.contrib.auth.models import User
class Basemodel(models.Model):
     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)
     class Meta:
         abstract = True

class Transaction(Basemodel):
     amount = models.DecimalField(max_digits=10, decimal_places=2)
     description = models.TextField()
     created_by=models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
     class Meta:
          ordering = ['description']
       
     def isNegative(self):
          return self.amount<0