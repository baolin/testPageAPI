from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect

from social_django.models import UserSocialAuth
from django.http import JsonResponse
import Posts
import ManageMultiPagesForOneUser

from . import models

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password1')
            )
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

 
def home(request):
    #user = request.user
    #print(user)
    #social = user.social_auth.get(provider='facebook')
    #at = social.extra_data['access_token']
    #models.get_all_pages(at)
    return render(request, 'core/home.html', {'access_token':''})

 
def doit(request):
    # print(request.GET['func'])
    userid = request.GET['userid']
    access_token = request.GET['access_token']
    func = request.GET['func']

    if func == 'get_most_liked_posts':
        pages = ManageMultiPagesForOneUser.getPagesForUser(userid, access_token)
        one_page = None
        for page in pages:
            one_page = page[1]
        
        posts = Posts.get_most_liked_posts(one_page, access_token)
        return JsonResponse(posts, safe=False)

    if func == 'pages_insights':
        pages_insights = ManageMultiPagesForOneUser.get_aggregated_insights_cross_pages(userid, access_token)
        return JsonResponse(pages_insights, safe=False)

    res = ManageMultiPagesForOneUser.get_aggregated_top_n(
        userid,
        access_token,
    )
    return JsonResponse(res, safe=False)

@login_required
def settings(request):
    user = request.user

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None
    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None
    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'core/settings.html', {
        'github_login': github_login,
        'twitter_login': twitter_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })

@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'core/password.html', {'form': form})
# Create your views here.
