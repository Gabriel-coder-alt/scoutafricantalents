from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from django.db.models import Sum, Avg
from store.models import AccountType
from accounts.models import Member
from .models import PlayerProfile, MatchRecord, PlayerRating, Video, CoachProfile, ActivityLog
from .forms import PlayerProfileForm, MatchDetailForm, PlayerRatingsForm, PlayerCreationForm, VideoUploadForm, CoachProfileForm

# Create your views here.
def Dashboard(request):
    user = request.user
    if user.is_authenticated:
        try:
            activity_log = ActivityLog.objects.get(user=request.user).order_by('date_created')
        except ObjectDoesNotExist:
            activity_log = None
        context = {
            'ActivityLog':activity_log
        }
        return render(request, 'application/dashboard-home.html', context)
    else:
        return redirect('login')

@login_required(login_url='login')
def Profile(request):
    user = User.objects.get(id=request.user.id)
    try:
        profile = PlayerProfile.objects.get(player=user)
        coach_profile = CoachProfile.objects.get(user=user)
    except ObjectDoesNotExist:
        profile = None
        coach_profile = None
    groups = user.groups.all()
    group1 = Group.objects.get(name="Amateur Player")
    group2 = Group.objects.get(name="Pro Player")
    group3 = Group.objects.get(name="Coach")
    context = {
        'profile':profile,
        'coach_profile':coach_profile
        }
    if profile is not None:
        for group in groups:
            if group == group1:
                return render(request, 'application/amateur_playerprofile.html', context)
            elif group == group2:
                return render(request, 'application/pro_playerprofile.html', context)
            else:
                pass
    elif coach_profile is not None:
        return render(request, 'application/coach_profile.html', context)
    else:
        return HttpResponse('First create profile to view this page.')

@login_required(login_url='login')
def EditAccount(request):
    if request.method == "POST":
        userName = request.POST['username']
        firstName = request.POST['first_name']
        lastName = request.POST['last_name']
        user = get_object_or_404(User, username=request.user)
        if user is not None:
            user.username = userName
            user.first_name = firstName
            user.last_name = lastName
            user.save()
            return redirect('profile')
        else:
            return HttpResponse('Something went wrong while trying to update your account, please try again later.')
    return render(request, 'application/edit_account.html')

@login_required(login_url='login')
def UploadPlayerProfile(request):
    if request.method == "POST":
        form = PlayerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.player = request.user
            instance.save()
            return redirect('profile')
    else:
        form = PlayerProfileForm()
    return render(request, 'application/upload_player_profile.html', {'form':form})

@login_required(login_url='login')
def uploadcoachprofile(request):
    if request.method == "POST":
        form = CoachProfileForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('profile')
    else:
        form = CoachProfileForm()
    context = {
        'form':form
    }
    return render(request, 'application/upload_coach_profile.html', context)

@login_required(login_url='login')
def updatecoachprofile(request):
    user = User.objects.get(id=request.user.id)
    try:
        coach_profile = CoachProfile.objects.get(user=user)
    except ObjectDoesNotExist:
        coach_profile = None
    if coach_profile is not None:
        if request.method == "POST":
            coach_profile.nationality = request.POST['nationality']
            coach_profile.gender = request.POST['gender']
            coach_profile.age = request.POST['age']
            coach_profile.date_of_birth = request.POST['date_of_birth']
            coach_profile.bio = request.POST['bio']
            coach_profile.education = request.POST['education']
            coach_profile.phone = request.POST['phone']
            coach_profile.address = request.POST['address']
            coach_profile.team = request.POST['team']
            coach_profile.team_icon = request.POST['team_icon']
            coach_profile.profile_photo = request.POST['profile_photo']
            coach_profile.save()
            return redirect('profile')
    else:
        return HttpResponse('Profile not available. First create a profile.')
    context = {
        'coach_profile':coach_profile
    }
    return render(request, 'application/update_coach_profile.html', context)

@login_required(login_url='login')
def UpdatePlayerProfile(request):
    try:
        user = PlayerProfile.objects.get(player=request.user)
    except ObjectDoesNotExist:
        user = None
    if request.method == "POST":
        age = request.POST['age']
        bio = request.POST['bio']
        strong_foot = request.POST['strong_foot']
        position = request.POST['Attacker']
        nationality = request.POST['nationality']
        gender = request.POST['male']
        education = request.POST['education']
        phone = request.POST['phone']
        height = request.POST['height']
        weight = request.POST['weight']
        dob = request.POST['date_of_birth']
        team = request.POST['team']
        team_icon = request.FILES['team_icon']
        profile_photo = request.FILES['profile_photo']
        if user is not None:
            user.age = age
            user.bio = bio
            user.strong_foot = strong_foot
            user.position = position
            user.nationality = nationality
            user.gender = gender
            user.education = education
            user.phone = phone
            user.height = height
            user.weight = weight
            user.date_of_birth = dob
            user.team = team
            user.team_icon = team_icon
            user.profile_photo = profile_photo
            user.save()
            return redirect('profile')
        else:
            return redirect('upload_player_profile')

    return render(request, 'application/update_player_profile.html')

@login_required(login_url='login')
def ChangePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'application/change_password.html', {'form':form})

@login_required(login_url='login')
def MyStatistics(request):
    match_list = MatchRecord.objects.filter(player=request.user).order_by('date_of_publish')
    appearances = match_list.count()
    total_goals = list(MatchRecord.objects.aggregate(Sum('goals_scored')).values())
    total_assists = list(MatchRecord.objects.aggregate(Sum('assist')).values())
    total_shots_on_target = list(MatchRecord.objects.aggregate(Sum('shots_on_target')).values())
    shots_per_game = list(MatchRecord.objects.aggregate(Avg('shots_on_target')).values())
    total_passes_completed = list(MatchRecord.objects.aggregate(Sum('passes_completed')).values())
    total_distance_covered = list(MatchRecord.objects.aggregate(Sum('distance_covered')).values())
    total_saves = list(MatchRecord.objects.aggregate(Sum('saves')).values())
    page = request.GET.get('page', 1)
    paginator = Paginator(match_list, 10)
    try:
        matches = paginator.page(page)
        try:
            rating = PlayerRating.objects.get(player=request.user)
        except ObjectDoesNotExist:
            rating = None
    except PageNotAnInteger:
        matches = paginator.page(1) 
    except EmptyPage:
        matches = paginator.page(paginator.num_pages)
    context = {
        'matches':matches,
        'rating':rating,
        'appearances':appearances,
        'goals':total_goals,
        'assists':total_assists,
        'passes_completed':total_passes_completed,
        'distance_covered':total_distance_covered,
        'shots':shots_per_game,
        'saves':total_saves
    }
    return render(request, 'application/my_statistics.html', context)

@login_required(login_url='login')
def UploadMatchStatistics(request):
    try:
        profile = PlayerProfile.objects.get(player=request.user)
    except ObjectDoesNotExist:
        profile = None
    if profile is not None:
        if request.method == "POST":
            form = MatchDetailForm(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.player = request.user
                instance.played_for = profile.team
                instance.team_icon = profile.team_icon
                instance.save()
                return redirect('my_statistics')
        else:
            form = MatchDetailForm()
    else:
        return HttpResponse('You need to create a profile before you can upload and update match records')
    return render(request, 'application/upload_match_statistics.html', {'form':form})

@login_required(login_url='login')
def UpdateMatchStatistics(request, id):
    try:
        match = MatchRecord.objects.get(player=request.user, id=id)
    except ObjectDoesNotExist:
        match = None
    if request.method == "POST":
        date = request.POST['date']
        venue =  request.POST['venue']
        played_against = request.POST['played_against']
        team_score = request.POST['team_score']
        opponent_score = request.POST['opponent_score']
        goal_scored = request.POST['goal_scored']
        assist = request.POST['assist']
        yellow_card = request.POST['yellow_card']
        red_card = request.POST['red_card']
        league = request.POST['league']
        shots_on_target = request.POST['shots_on_target']
        passes_completed = request.POST['passes_completed']
        distance_covered = request.POST['distance_covered']
        saves = request.POST['saves']
        time_in_minutes = request.POST['time_in_minutes']
        opponent_icon = request.FILES['opponent_icon']
        if match is not None:
            match.date = date
            match.venue = venue
            match.played_against = played_against
            match.team_score = team_score
            match.opponent_score = opponent_score
            match.goal_scored = goal_scored
            match.assist = assist
            match.yellow_card = yellow_card
            match.red_card = red_card
            match.league = league
            match.shots_on_target = shots_on_target
            match.passes_completed = passes_completed
            match.distance_covered = distance_covered
            match.saves = saves
            match.time_in_minutes = time_in_minutes
            match.opponent_icon = opponent_icon
            match.save()
            return redirect('my_statistics')
        else:
            return HttpResponse('We encountered an error while you were updating your data')
    return render(request, 'application/update_match_statistics.html', {'match':match})

@login_required(login_url='login')
def MatchResults(request, id):
    match = MatchRecord.objects.get(player=request.user, id=id)
    return render(request, 'application/match_detail.html', {'match':match})

@login_required(login_url='login')
def DeleteMatchRecord(request, id):
    match = MatchRecord.objects.get(player=request.user, id=id)
    match.delete()
    return redirect('my_statistics')
    
@login_required(login_url='login')
def UploadPlayerRatings(request):
    if request.method == "POST":
        form = PlayerRatingsForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.player = request.user
            instance.save()
            return redirect('my_statistics')
    else:
        form = PlayerRatingsForm()
    return render(request, 'application/upload_player_ratings.html', {'form':form})

@login_required(login_url='login')
def updateplayerratings(request):
    try:
        ratings = PlayerRating.objects.get(player=request.user)
    except ObjectDoesNotExist:
        ratings = None
    if request.method == "POST":
        stamina = request.POST['stamina']
        durability = request.POST['durability']
        speed = request.POST['speed']
        pass_accuracy = request.POST['pass_accuracy']
        shot_accuracy = request.POST['shot_accuracy']
        if ratings is not None:
            ratings.stamina = stamina
            ratings.durability = durability
            ratings.speed = speed
            ratings.pass_accuracy = pass_accuracy
            ratings.shot_accuracy = shot_accuracy
            ratings.save()
            return redirect('my_statistics')
        else:
            return HttpResponse('We encountered an error while you were updating your data')
    return render(request, 'application/update_player_ratings.html', {'ratings':ratings})

@login_required(login_url='login')
def playerdatabase(request):
    player_list = PlayerProfile.objects.all()

    min_age = request.GET.get('min_age')
    max_age = request.GET.get('max_age')
    min_weight = request.GET.get('min_weight')
    max_weight = request.GET.get('max_weight')
    min_height = request.GET.get('min_height')
    max_height = request.GET.get('max_height')
    strong_foot = request.GET.get('strong_foot')
    position = request.GET.get('position')
    gender = request.GET.get('gender')
    if min_age != '' and min_age is not None and max_age != '' and max_age is not None:
        player_list = player_list.filter(age__range=[min_age, max_age])
    elif min_weight != '' and min_weight is not None and max_weight != '' and max_weight is not None:
        player_list = player_list.filter(weight__range = [min_weight, max_weight])
    elif min_height != '' and min_height is not None and max_weight != '' and max_weight is not None:
        player_list = player_list.filter(height__range=[min_height, max_height])
    elif strong_foot != '' and strong_foot is not None:
        player_list = player_list.filter(strong_foot__icontains=strong_foot)
    elif position != '' and position is not None:
        player_list = player_list.filter(position__icontains=position)
    elif gender != '' and gender is not None:
        player_list = player_list.filter(gender__icontains=gender)
    page = request.GET.get('page', 1)
    paginator = Paginator(player_list, 10)
    try:
        players = paginator.page(page)
    except PageNotAnInteger:
        players = paginator.page(1)
    except EmptyPage:
        players = paginator.page(paginator.num_pages)
    return render(request, 'application/player_database.html', {'players':players})

@login_required(login_url='login')
def PlayerStatistics(request, id):
    user = User.objects.get(id=id)
    match_list = MatchRecord.objects.filter(player=user).order_by('date_of_publish')
    appearances = match_list.count()
    total_goals = list(MatchRecord.objects.aggregate(Sum('goals_scored')).values())
    total_assists = list(MatchRecord.objects.aggregate(Sum('assist')).values())
    total_shots_on_target = list(MatchRecord.objects.aggregate(Sum('shots_on_target')).values())
    shots_per_game = list(MatchRecord.objects.aggregate(Avg('shots_on_target')).values())
    total_passes_completed = list(MatchRecord.objects.aggregate(Sum('passes_completed')).values())
    total_distance_covered = list(MatchRecord.objects.aggregate(Sum('distance_covered')).values())
    total_saves = list(MatchRecord.objects.aggregate(Sum('saves')).values())
    page = request.GET.get('page', 1)
    paginator = Paginator(match_list, 10)
    try:
        matches = paginator.page(page)
        try:
            rating = PlayerRating.objects.get(player=user)
            player_profile = PlayerProfile.objects.get(player=user)
        except ObjectDoesNotExist:
            rating = None
            player_profile = None
    except PageNotAnInteger:
        matches = paginator.page(1) 
    except EmptyPage:
        matches = paginator.page(paginator.num_pages)
    context = {
        'player_profile':player_profile,
        'matches':matches,
        'rating':rating,
        'appearances':appearances,
        'goals':total_goals,
        'assists':total_assists,
        'passes_completed':total_passes_completed,
        'distance_covered':total_distance_covered,
        'shots':shots_per_game,
        'saves':total_saves
    }
    return render(request, 'application/player_statistics.html', context)

# backend for the each match statistics for individual players
@login_required(login_url='login')
def IndividualMatchResult(request, id, mid):
    user = User.objects.get(id=id)
    try:
        match = MatchRecord.objects.get(id=mid, player=user)
    except ObjectDoesNotExist:
        match = None
    return render(request, 'application/match_detail.html',{'match':match})

# @login_required(login_url='login')
# def playersearch(request):
#     min_age = request.GET.get('min_age')
#     max_age = request.GET.get('max_age')
#     min_weight = request.GET.get('min_weight')
#     max_weight = request.GET.get('max_weight')
#     min_height = request.GET.get('min_height')
#     max_height = request.GET.get('max_height')
#     strong_foot = request.GET.get('strong_foot')
#     position = request.GET.get('position')
#     gender = request.GET.get('gender')
#     try:
#         players = PlayerProfile.objects.filter(
#             age__range=[min_age, max_age],
#             weight__range=[min_weight, max_weight],
#             height__range=[min_height, max_height],
#             strong_foot=strong_foot,
#             position=position,
#             gender=gender
#         )
#     except ObjectDoesNotExist:
#         players = None
#     if players is not None:
#         return render(request, 'application/player_search_result.html', {'players':players})
#     else:
#         return HttpResponse('Player with the given parameters cannot be found on our database.')        
#     return render(request, 'application/player_search.html')

@login_required(login_url='login')
def playerscart(request):
    try:
        amateurPlayer = AccountType.objects.get(membership_type="Amateur Player")
        proPlayer = AccountType.objects.get(membership_type="Pro Player")
    except ObjectDoesNotExist:
        amateurPlayer = None
        proPlayer = None
    return render(request, 'application/players_cart.html', {'amateurPlayer':amateurPlayer, 'proPlayer':proPlayer})
    
@login_required(login_url='login')
def addplayer(request, id):
    account = AccountType.objects.get(id=id)
    group = Group.objects.get(name=account.membership_type)
    instance = Member()
    if request.method == "POST":
        form = PlayerCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            group.user_set.add(user)
            instance.player = user
            instance.member_group = group
            instance.created_by = request.user
            instance.save()
            return redirect('manage_players')
    else:
        form = PlayerCreationForm()
    return render(request, 'application/add_player.html', {'account':account, 'form':form})

@login_required(login_url='login')
def playermanagement(request):
    try:
        members = Member.objects.filter(created_by=request.user)
    except ObjectDoesNotExist:
        members = None
    page = request.GET.get('page',1)
    paginator = Paginator(members, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'application/players_management_dashboard.html', {'users':users})

@login_required(login_url='login')
def playerprofile(request, id):
    user = User.objects.get(id=id)
    try:
        profile = PlayerProfile.objects.get(player=user)
    except ObjectDoesNotExist:
        profile = None
    user_groups = user.groups.all()
    group1 = Group.objects.get(name="Amateur Player")
    group2 = Group.objects.get(name="Pro Player")
    for group in user_groups:
        if group == group1:
            return render(request, 'application/amateur_playerprofile.html', {'profile':profile})
        else:
            return render(request, 'application/pro_playerprofile.html', {'profile':profile})

@login_required(login_url='login')
def uploadandupdateplayerprofile(request, id):
    user = User.objects.get(id=id)
    try:
        profile = PlayerProfile.objects.get(player=user)
    except ObjectDoesNotExist:
        profile = None
    user_groups = user.groups.all()
    group1 = Group.objects.get(name="Amateur Player")
    group2 = Group.objects.get(name="Pro Player")
    for group in user_groups:
        if group == group1:
            if request.method == "POST":
                age = request.POST['age']
                phone = request.POST['phone']
                education = request.POST['education']
                nationality = request.POST['nationality']
                gender = request.POST['gender']
                dob = request.POST['date_of_birth']
                profile_photo = request.FILES['profile_photo']
                if profile is not None:
                    profile.age = age 
                    profile.phone = phone
                    profile.education = education
                    profile.nationality = nationality
                    profile.gender = gender
                    profile.date_of_birth = dob
                    profile.profile_photo = profile_photo
                    profile.save()
                    return redirect('manage_players')
                else:
                    new_profile = PlayerProfile(
                        player=user,
                        age=age,
                        phone=phone,
                        education=education,
                        nationality=nationality,
                        gender=gender,
                        date_of_birth=dob,
                        profile_photo=profile_photo
                        )
                    new_profile.save()
                    return redirect('manage_players')
            return render(request, 'application/upload&update_amateur_playerprofile.html', {'profile':profile,'user':user})
        elif group == group2:
            if request.method == "POST":
                age = request.POST['age']
                phone = request.POST['phone']
                education = request.POST['education']
                bio = request.POST['bio']
                strong_foot = request.POST['strong_foot']
                position = request.POST['position']
                nationality = request.POST['nationality']
                gender = request.POST['gender']
                height = request.POST['height']
                weight = request.POST['weight']
                dob = request.POST['date_of_birth']
                team = request.POST['team']
                team_icon = request.FILES['team_icon']
                profile_photo = request.FILES['profile_photo']
                if profile is not None:
                    profile.age = age
                    profile.phone = phone
                    profile.education = education
                    profile.bio = bio
                    profile.strong_foot = strong_foot
                    profile.position = position
                    profile.nationality = nationality
                    profile.gender = gender
                    profile.height = height
                    profile.weight = weight
                    profile.date_of_birth = dob
                    profile.team = team
                    profile.team_icon = team_icon
                    profile.profile_photo = profile_photo
                    profile.save()
                    return redirect('manage_players')
                else:
                    new_profile = PlayerProfile(
                        player=user,
                        age=age,
                        phone=phone,
                        education=education,
                        bio=bio,
                        strong_foot=strong_foot,
                        position=position,
                        nationality=nationality,
                        gender=gender,
                        height=height,
                        weight=weight,
                        date_of_birth=dob,
                        team=team,
                        team_icon=team_icon,
                        profile_photo=profile_photo
                        )
                    new_profile.save()
                    return redirect('manage_players')
            return render(request, 'application/upload&update_pro_playerprofile.html', {'profile':profile, 'user':user})
        else:
            return HttpResponse('No profile upload form available for this account type.')

@login_required(login_url='login')
def editplayeraccount(request, id):
    try:
        user = User.objects.get(id=id)
    except ObjectDoesNotExist:
        user = None
    if user is not None:
        if request.method == "POST":
            user.username = request.POST['username']
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.save()
            return redirect('manage_players')
    else:
        return HttpResponse('Something went wrong while updating the account.')
    return render(request, 'application/edit_player_account.html', {'user':user})

@login_required(login_url='login')
def changeplayerpassword(request, id):
    try:
        instance = User.objects.get(id=id)
    except ObjectDoesNotExist:
        instance = None
    if instance is not None:
        if request.method == "POST":
            form = PasswordChangeForm(instance, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                return redirect('manage_players')
        else:
            form = PasswordChangeForm(instance)
        context = {
            'form':form,
            'instance':instance
            }
        return render(request, 'application/change_player_password.html', context)
    else:
        return HttpResponse('User with the requested account not available')

@login_required(login_url='login')
def playerstatisticsview(request, id):
    user = User.objects.get(id=id)
    item_list = MatchRecord.objects.filter(player=user)
    appearances = item_list.count()
    total_goals = list(MatchRecord.objects.aggregate(Sum('goals_scored')).values())
    total_assists = list(MatchRecord.objects.aggregate(Sum('assist')).values())
    total_shots_on_target = list(MatchRecord.objects.aggregate(Sum('shots_on_target')).values())
    shots_per_game = list(MatchRecord.objects.aggregate(Avg('shots_on_target')).values())
    total_passes_completed = list(MatchRecord.objects.aggregate(Sum('passes_completed')).values())
    total_distance_covered = list(MatchRecord.objects.aggregate(Sum('distance_covered')).values())
    total_saves = list(MatchRecord.objects.aggregate(Sum('saves')).values())
    page = request.GET.get('page', 1)
    paginator = Paginator(item_list, 10)
    try:
        items = paginator.page(page)
        try:
            rating = PlayerRating.objects.get(player=user)
            player_profile = PlayerProfile.objects.get(player=user)
        except ObjectDoesNotExist:
            rating = None
            player_profile = None
    except PageNotAnInteger:
        items = paginator.page(1) 
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    context = {
        'items':items,
        'rating':rating,
        'user':user,
        'player_profile':player_profile,
        'appearances':appearances,
        'goals':total_goals,
        'assists':total_assists,
        'shots':shots_per_game,
        'passes':total_passes_completed,
        'distance_covered':total_distance_covered,
        'saves':total_saves
    }
    return render(request, 'application/manage_player_statistics.html', context)

@login_required(login_url='login')
def uploadplayermatchrecord(request, id):
    user = User.objects.get(id=id)
    try:
        profile = PlayerProfile.objects.get(player=user)
    except ObjectDoesNotExist:
        profile = None
    if profile is not None:
        if request.method == "POST":
            form = MatchDetailForm(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.player = user
                instance.played_for = profile.team
                instance.team_icon = profile.team_icon
                instance.save()
                return redirect('manage_players')
        else:
            form = MatchDetailForm()
        context = {
            'form':form,
            'user':user
        }
        return render(request, 'application/upload_player_match_record.html', context)
    else:
        return HttpResponse('Create Player profile before creating match record.')

@login_required(login_url='login')
def manageplayerratings(request, id):
    user = User.objects.get(id=id)
    try:
        ratings = PlayerRating.objects.get(player=user)
    except ObjectDoesNotExist:
        ratings = None
    if request.method == "POST":
        stamina = request.POST['stamina']
        durability = request.POST['durability']
        speed = request.POST['speed']
        pass_accuracy = request.POST['pass_accuracy']
        shot_accuracy = request.POST['shot_accuracy']
        if ratings is None:
            new_ratings = PlayerRating(
                player=user,
                stamina=stamina,
                durability=durability,
                speed=speed,
                pass_accuracy=pass_accuracy,
                shot_accuracy=shot_accuracy
            )
            new_ratings.save()
            return redirect('manage_players')
        else:
            ratings.player = user
            ratings.stamina = stamina
            ratings.durability = durability
            ratings.speed = speed
            ratings.pass_accuracy = pass_accuracy
            ratings.shot_accuracy = shot_accuracy
            ratings.save()
            return redirect('manage_players')
    context = {
        'user':user,
        'ratings':ratings
    }
    return render(request, 'application/manage_player_ratings.html', context)

@login_required(login_url='login')
def updateplayermatchrecord(request, id, mid):
    user = User.objects.get(id=id)
    try:
        match = MatchRecord.objects.get(player=user, id=mid)
    except ObjectDoesNotExist:
        match = None
    if match is not None:
        if request.method == "POST":
            match.date = request.POST['date']
            match.venue = request.POST['venue']
            match.played_against = request.POST['played_against']
            match.team_score = request.POST['team_score']
            match.opponent_score = request.POST['opponent_score']
            match.goals_scored = request.POST['goals_scored']
            match.assist = request.POST['assist']
            match.yellow_card = request.POST['yellow_card']
            match.red_card = request.POST['red_card']
            match.league = request.POST['league']
            match.shots_on_target = request.POST['shots_on_target']
            match.passes_completed = request.POST['passes_completed']
            match.distance_covered = request.POST['distance_covered']
            match.saves = request.POST['saves']
            match.time_in_minutes = request.POST['time_in_minutes']
            match.opponent_icon = request.FILES['opponent_icon']
            match.save()
            return redirect('manage_players')
    else:
        return HttpResponse('Create Match record before updating match record.')
    context = {
        'user':user,
        'match':match
    }
    return render(request, 'application/update_player_match_record.html', context)

@login_required(login_url='login')
def deleteplayermatchrecord(request, id, mid):
    user =User.objects.get(id=id)
    try:
        match = MatchRecord.objects.get(player=user, id=mid)
    except ObjectDoesNotExist:
        match = None
    match.delete()
    return reverse('manage_players')

@login_required(login_url='login')
def playervideouploadview(request, id):
    user = User.objects.get(id=id)
    if request.method == "POST":
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.player = user
            instance.save()
            return redirect('manage_players')
    else:
        form = VideoUploadForm()
    context = {
        'form':form,
        'user':user
    }
    return render(request, 'application/video_upload_form.html', context)

@login_required(login_url='login')
def manageplayervideos(request, id):
    user = User.objects.get(id=id)
    try:
        video_list = Video.objects.filter(player=user)
    except ObjectDoesNotExist:
        video_list = None
    page = request.GET.get('page',1)
    paginator = Paginator(video_list, 10)
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)
    context = {
        'videos':videos
    }
    return render(request, 'application/manage_player_videos.html', context)

@login_required(login_url='login')
def playervideoview(request, id, vid):
    user = User.objects.get(id=id)
    video = Video.objects.get(player=user, id=vid)
    try:
        related_videos = Video.objects.filter(category=video.category).exclude(id=video.id).order_by('date_of_publish')[:5]
    except ObjectDoesNotExist:
        related_videos = None
    context = {
        'user':user,
        'video':video,
        'related_videos':related_videos
    }
    return render(request, 'application/video_view.html', context)

@login_required(login_url='login')
def deleteplayervideo(request, id, vid):
    user = User.objects.get(id=id)
    try:
        video = Video.objects.get(id=vid, player=user)
    except ObjectDoesNotExist:
        video = None
    if video is not None:
        video.delete()
        return redirect('manage_players')
    else:
        return HttpResponse('This video does not exist.')

@login_required(login_url='login')
def playervideolistview(request, id):
    user = User.objects.get(id=id)
    try:
        player_videos = Video.objects.filter(player=user)
    except ObjectDoesNotExist:
        player_videos = None
    page = request.GET.get('page',1)
    paginator = Paginator(player_videos, 10)
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)
    context = {
        'videos':videos
    }
    return render(request, 'application/player_video_list.html', context)

@login_required(login_url='login')
def myvideouploadview(request):
    if request.method == "POST":
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.player = request.user
            instance.save()
            return redirect('my_video_gallery')
    else:
        form = VideoUploadForm()
    context = {
        'form':form
    }
    return render(request, 'application/personal_video_upload_form.html', context)

@login_required(login_url='login')
def myvideos(request):
    try:
        myVideoList = Video.objects.filter(player=request.user)
    except ObjectDoesNotExist:
        myVideoList = None
    page = request.GET.get('page',1)
    paginator = Paginator(myVideoList, 10)
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)
    context = {
        'videos':videos
    }
    context = {
        'videos':videos
    }
    return render(request, 'application/manage_player_videos.html', context)

@login_required(login_url='login')
def categoryvideos(request, category):
    try:
        myVideos = Video.objects.filter(player=request.user, category=category)
    except ObjectDoesNotExist:
        myVideos = None
    page = request.GET.get('page',1)
    paginator = Paginator(myVideos, 10)
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)
    context = {
        'videos':videos
    }
    return render(request, 'application/category_videos.html', context)