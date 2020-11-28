from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.
class Member(models.Model):
    player = models.OneToOneField(User, on_delete=models.CASCADE)
    member_group = models.OneToOneField(Group, on_delete=models.CASCADE)
    created_by = models.CharField(max_length=30, blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.player.username