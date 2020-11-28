from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from .models import ActivityLog
from django.utils import timezone
import datetime

try:
    admin_group = Group.objects.get(name="admin")
except ObjectDoesNotExist:
    admin_group = None

@receiver(user_logged_in)
def userloggedin(sender, request, user, **kwargs):
    if request.user is not None:
        if admin_group not in request.user.groups.all() and admin_group is None:
            print('Admin group does not Exist in Groups nor User model.')
        elif admin_group in request.user.groups.all() and admin_group is not None:
            print('Admin successfully logged in.')       
        else:
            activity_loggged_in = ActivityLog.objects.create(user=request.user, time_in=timezone.now())
            print('User logged in successfully.')
    else:
        pass

@receiver(user_logged_out)
def userloggedout(sender, request, user, **kwargs):
    if request.user is not None:
        if admin_group not in request.user.groups.all() and admin_group is None:
            print('Admin group does not Exist in Groups nor User model.')
        elif admin_group in request.user.groups.all() and admin_group is not None:
            print('Admin successfully logged out.')       
        else:
            today_log = ActivityLog.objects.get(user=request.user, date=datetime.date.today())
            today_log.time_out = datetime.timezone.now()
            today_log.save()
            print('User logged out successfully.')
    else:
        pass

# @receiver(user_login_failed)
# def faileduserlogin(sender, request, user, **kwargs):
#     if request.user is not None:
#         if admin_group not in request.user.groups.all() and admin_group is None:
#             print('Admin group does not Exist in Groups nor User model.')     
#         else:
#             print('User was unable to logout successfully.') 
#     else:
#         pass