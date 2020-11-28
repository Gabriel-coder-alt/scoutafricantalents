# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth.models import Group, User
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.conf import settings
from store.utils import generate_token
from store.models import Transaction

def SignupView(request, uidb64):
    try:
        pk = force_text(urlsafe_base64_decode(uidb64)).decode()
        transaction =  Transaction.objects.get(pk=pk)
        email = transaction.subscriber_email
        user = User.objects.get(email=email)
    except ObjectDoesNotExist:
        pk = None
        transaction = None
        email = None
        user = None
    if transaction is not None and user is None:
        if request.method == "POST":
            form = UserCreationForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.email = email
                instance.save()
        else:
            form = UserCreationForm()
        return render(request, 'accounts/signup.html', {'form':form})
    else:
        return HttpResponse('Signup link is no longer valid, visit our pricing page to subscribe for an account.')

def LoginView(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_active == True:
                login(request, user)
                return redirect('dashboard')
            else:
                return HttpResponse('Your account has been de-activated, renew your subscription to re-activate your account.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form':form})

def LogoutView(request):
    logout(request)
    return redirect('login')

def passwordretrievalform(request):
    if request.method == "POST":
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            user = None
        current_site = get_current_site(request)
        if user is not None:  
            subject = "Reset Your Password"
            message = render_to_string('accounts/mail/password_reset_mail.html', {
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':generate_token.make_token(user)
            })
            mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, to=[user.email])
            mail.send()
            return HttpResponse('Check your mail and follow the password reset link forwarded to you.')
        else:
            return HttpResponse('Account not found.')
    return render(request, 'accounts/password_retrieval_form.html')

def resetpassword(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64)).decode()
        user = User.objects.get(pk=uid)
    except ObjectDoesNotExist:
        uid = None
        user = None
    if user is not None and generate_token.check_token(user, token):
        if request.method == "POST":
            new_password = request.POST['new_password']
            user.set_password(new_password)
            user.save()
            return HttpResponse('Your password was changed sucessfully.')
        return render(request, 'accounts/new_password_form')
    else:
        return HttpResponse('Account with the requested email not found.')