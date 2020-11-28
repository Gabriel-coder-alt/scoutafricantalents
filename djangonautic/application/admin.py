from django.contrib import admin
from .models import PlayerProfile, MatchRecord, PlayerRating, Video, CoachProfile, ActivityLog

# Register your models here.
admin.site.register(PlayerProfile)
admin.site.register(MatchRecord)
admin.site.register(PlayerRating)
admin.site.register(Video)
admin.site.register(CoachProfile)
admin.site.register(ActivityLog)