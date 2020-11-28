from django import forms
import django_filters
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from .models import PlayerProfile, MatchRecord, PlayerRating, Video, CoachProfile
from accounts.models import Member

STRONG_FOOT = [
    ('-','---'),
    ('Left','Left'),
    ('Right','Right'),
    ('Both','Both')
]
CHOICES = [
    ('-','---'),
    ('Male','Male'),
    ('Female','Female')
]

POSITIONS = [
    ('-','---'),
    ('Attacker','Attacker'),
    ('Defender','Defender'),
    ('Midfielder','Midfielder'),
    ('Goalkeeper','Goalkeeper')
]

CARD_CHOICES = [
    ('-','---'),
    ('Yes','Yes'),
    ('No','No')
]

LEAGUE_CHOICES = [
    ('Others','Others'),
    ('CAF','CAF'),
    ('AFCON','AFCON')
]

VIDEO_CATEGORY = [
    ('-','---'),
    ('goals','Goals'),
    ('dribbles','Dribbles'),
    ('passes','Passes'),
    ('assists','Assists'),
    ('crossing','Crossing'),
    ('aerial duels', 'Aerial duels'),
    ('one-on-one duels', 'One on one duels'),
    ('saves','saves')
]

EDUCATION = [
    ('None','None'),
    ('High School Certificate','High School Certificate'),
    ('Graduate','Graduate'),
    ('Postgraduate','Postgraduate')
]

class PlayerProfileForm(forms.ModelForm):
    profile_photo = forms.FileField(widget=forms.FileInput())
    age = forms.IntegerField(required=True)
    bio = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Your bio should be short and not exceeding 250 characters long'}), max_length=250, required=True)
    education = forms.CharField(widget=forms.Select(choices=EDUCATION), max_length=30, required=True)
    phone = forms.IntegerField(widget=forms.NumberInput(), required=True)
    strong_foot = forms.CharField(widget=forms.Select(choices=STRONG_FOOT))
    position = forms.CharField(widget=forms.Select(choices=POSITIONS))
    nationality = forms.CharField(max_length=30, required=True)
    gender = forms.CharField(widget=forms.Select(choices=CHOICES))
    height = forms.DecimalField(label='Height(inches)', max_digits=4, widget=forms.NumberInput(), decimal_places=2, required=True)
    weight = forms.DecimalField(label='Weight(kg)', max_digits=4, widget=forms.NumberInput(), decimal_places=2, required=True)
    date_of_birth = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Day Month Year, e.g. 21 September 1998'}), max_length=30, required=True)
    team = forms.CharField(max_length=30, required=True)
    team_icon = forms.FileField(widget=forms.FileInput())
    class Meta:
        model = PlayerProfile
        fields = [   
            'age',
            'bio',
            'education',
            'phone',
            'strong_foot',
            'position',
            'nationality',
            'gender',
            'height',
            'weight',
            'date_of_birth',
            'team',
            'team_icon',
            'profile_photo',
        ]

class MatchDetailForm(forms.ModelForm):
    date =  forms.DateField(widget=forms.TextInput(attrs={'type':'date'}))
    venue = forms.CharField(max_length=30, required=True)
    played_against = forms.CharField(max_length=30, required=True)
    team_score = forms.IntegerField(required=True)
    opponent_score = forms.IntegerField(required=True)
    goals_scored = forms.IntegerField(required=False)
    assist = forms.IntegerField(required=False)
    yellow_card = forms.CharField(max_length=5, widget=forms.Select(choices=CARD_CHOICES), required=False)
    red_card = forms.CharField(max_length=5, widget=forms.Select(choices=CARD_CHOICES), required=False)
    league = forms.CharField(max_length=7, widget=forms.Select(choices=LEAGUE_CHOICES), required=False)

    class Meta:
        model = MatchRecord
        fields = [
            'date',
            'venue',
            'played_against',
            'team_score',
            'opponent_score',
            'goals_scored',
            'assist',
            'yellow_card',
            'red_card',
            'league', 
            'shots_on_target',
            'passes_completed',
            'distance_covered',
            'saves',
            'time_in_minutes',
            'opponent_icon',
        ]

    def save(self, commit=True):
        match = super().save(commit=False)
        match.date = self.cleaned_data['date']
        match.venue = self.cleaned_data['venue']
        match.played_against = self.cleaned_data['played_against']
        match.team_score = self.cleaned_data['team_score']
        match.opponent_score = self.cleaned_data['opponent_score']
        match.goals_scored = self.cleaned_data['goals_scored']
        match.assist = self.cleaned_data['assist']
        match.yellow_card = self.cleaned_data['yellow_card']
        match.red_card = self.cleaned_data['red_card']
        match.league = self.cleaned_data['league']
        match.shots_on_target = self.cleaned_data['shots_on_target']
        match.passes_completed = self.cleaned_data['passes_completed']
        match.distance_covered = self.cleaned_data['distance_covered']
        match.saves = self.cleaned_data['saves']
        match.time_in_minutes = self.cleaned_data['time_in_minutes']
        match.opponent_icon = self.cleaned_data['opponent_icon']

        if commit:
            match.save()
        return match

class PlayerRatingsForm(forms.ModelForm):
    class Meta:
        model = PlayerRating
        fields = [
            'stamina', 
            'durability', 
            'speed', 
            'pass_accuracy', 
            'shot_accuracy'
        ]

class UserGroupForm(forms.ModelForm):
    group = forms.ModelChoiceField(label='Register as', queryset=Group.objects.all().exclude(name='admin'), required=True)

    class Meta:
        model = Group
        fields = [
            'group',
        ]

class PlayerCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        ]

        def save(self, commit=True):
            user = super().save(commit=False)
            user.username = self.cleaned_data['username']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            if commit:
                user.save()
            return user

class VideoUploadForm(forms.ModelForm):
    title = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder':'Your title should not be more than 40 characters long'}), required=False)
    category = forms.CharField(max_length=20, widget=forms.Select(choices=VIDEO_CATEGORY), required=True)
    video = forms.FileField(widget=forms.FileInput())
    class Meta:
        model = Video
        fields = [
            'title',
            'category',
            'video'
        ]

    # def save(self, commit=True):
    #     video = super().save(commit=False)
    #     video.title = self.cleaned_data['title']
    #     video.category = self.cleaned_data['category']
    #     video.video = self.cleaned_data['video']
    #     if commit:
    #         vdeo.save()
    #     return video

class CoachProfileForm(forms.ModelForm):
    nationality = forms.CharField(max_length=30, required=True)
    gender = forms.CharField(widget=forms.Select(choices=CHOICES))
    age = forms.IntegerField(required=True)
    bio = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Your bio should be short and not exceeding 250 characters long'}), max_length=250, required=True)
    education = forms.CharField(widget=forms.Select(choices=EDUCATION), max_length=30, required=True)
    phone = forms.IntegerField(widget=forms.NumberInput(), required=True)
    date_of_birth = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Day Month Year, e.g. 21 September 1998'}), max_length=30, required=True)
    address = forms.CharField(max_length=80, widget=forms.TextInput(attrs={'placeholder':'Your address should not be more than 80 characters long'}), required=False)
    profile_photo = forms.FileField(widget=forms.FileInput())
    resume = forms.FileField(widget=forms.FileInput())
    team = forms.CharField(max_length=30, required=True)
    team_icon = forms.FileField(widget=forms.FileInput())

    class Meta:
        model = CoachProfile
        fields = [
            'nationality',
            'gender',
            'age',
            'date_of_birth',
            'bio',
            'education',
            'phone',
            'address',
            'team',
            'profile_photo',
            'resume',
            'team_icon'    
        ]

        def save(self, commit=True):
            profile = super().save(commit=False)
            profile.nationality = self.cleaned_data['nationality']
            profile.gender = self.cleaned_data['gender']
            profile.age = self.cleaned_data['age']
            profile.date_of_birth = self.cleaned_data['date_of_birth']
            profile.bio = self.cleaned_data['bio']
            profile.education = self.cleaned_data['education']
            profile.phone = self.cleaned_data['phone']
            profile.address = self.cleaned_data['address']
            profile.profile_photo = self.cleaned_data['profile_photo']
            profile.resume = self.cleaned_data['resume']
            profile.team = self.cleaned_data['team']
            profile.team_icon = self.cleaned_data['team_icon'] 
            if commit:
                profile.save()
            return profile