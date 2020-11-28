from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PlayerProfile(models.Model):
    player = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='uploads/player_profile', default='user-profile.png')
    age = models.IntegerField(blank=True, null=True)
    bio = models.CharField(max_length=200, blank=True, null=True)
    education = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    strong_foot = models.CharField(max_length=20, blank=True, null=True)
    position = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    nationality = models.CharField(max_length=40, blank=True, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    date_of_birth = models.CharField(max_length=20, blank=True, null=True)
    team = models.CharField(max_length=30, blank=True, null=True)
    team_icon = models.ImageField(upload_to='uploads/team_icon', default=None)

    def __str__(self):
        return self.player.username

#Table for Player Match Record
class MatchRecord(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.CharField(max_length=10, blank=True, null=False)
    venue = models.CharField(max_length=30, blank=True, null=False)
    played_for = models.CharField(max_length=30, blank=True, null=False)
    played_against = models.CharField(max_length=30, blank=True, null=False)
    team_score = models.IntegerField(blank=True, null=False)
    opponent_score = models.IntegerField(blank=True, null=False)
    goals_scored = models.IntegerField(blank=True, null=False)
    assist = models.IntegerField(blank=True, null=False)
    yellow_card = models.CharField(max_length=5, blank=True, null=False)
    red_card = models.CharField(max_length=5, blank=True, null=False)
    league = models.CharField(max_length=30, blank=True, null=True)
    team_icon = models.ImageField(upload_to='uploads/team_icon', default=None)
    opponent_icon = models.ImageField(upload_to='uploads/opponent_icon', default=None)
    shots_on_target = models.IntegerField(blank=True, null=True)
    passes_completed = models.IntegerField(blank=True, null=True)
    distance_covered = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    saves = models.IntegerField(blank=True, null=True)
    time_in_minutes =  models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date_of_publish = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.player.username

    # def save(self, *args, **kwargs):
    #     self.team_icon.save()
    #     self.opponent_icon.save()
    #     super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.team_icon.delete()
        self.opponent_icon.delete()
        super().delete(*args, **kwargs)

class PlayerRating(models.Model):
    player = models.OneToOneField(User, on_delete=models.CASCADE)
    stamina = models.DecimalField(max_digits=4, decimal_places=2, blank=False, null=False)
    durability = models.DecimalField(max_digits=4, decimal_places=2, blank=False, null=False)
    speed = models.DecimalField(max_digits=4, decimal_places=2, blank=False, null=False)
    pass_accuracy = models.DecimalField(max_digits=4, decimal_places=2,  blank=False, null=False)
    shot_accuracy = models.DecimalField(max_digits=4, decimal_places=2, blank=False, null=False)

    def __str__(self):
        return self.player.username

class Video(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=40, blank=True, null=True)
    category = models.CharField(max_length=20, blank=False, null=False)
    video = models.FileField(upload_to='videos/', default=None)
    date_of_publish = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.player.username

class CoachProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, blank=True, null=True)
    nationality = models.CharField(max_length=40, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=80, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='uploads/player_profile', default='user-profile.png')
    age = models.IntegerField(blank=True, null=True)
    bio = models.CharField(max_length=200, blank=True, null=True)
    education = models.CharField(max_length=20, blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', default=None)
    date_of_birth = models.CharField(max_length=20, blank=True, null=True)
    team = models.CharField(max_length=30, blank=True, null=True)
    team_icon = models.ImageField(upload_to='uploads/team_icon', default=None)

class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    time_in = models.CharField(max_length=10, blank=True, null=True)
    time_out = models.CharField(max_length=10, blank=True, null=True)