from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})



from .models import Tweet
from django.contrib.auth.decorators import login_required
from .models import Follow

@login_required
def home(request):
    # 全ユーザーの投稿（降順）
    all_tweets = Tweet.objects.all().order_by('-created_at')

    # フォロー中のユーザーの投稿
    following_ids = Follow.objects.filter(follower=request.user).values_list('following__id', flat=True)
    following_tweets = Tweet.objects.filter(user__id__in=following_ids).order_by('-created_at')

    return render(request, 'core/home.html', {
        'all_tweets': all_tweets,
        'following_tweets': following_tweets,
    })


from .forms import TweetForm

@login_required
def create_tweet(request):
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user  # ログイン中のユーザーを紐付け
            tweet.save()
            return redirect('home')
    else:
        form = TweetForm()
    return render(request, 'core/create_tweet.html', {'form': form})



@login_required
def profile_view(request):
    profile = request.user.profile
    tweets = Tweet.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/profile.html', {
        'profile': profile,
        'tweets': tweets
    })


from django.shortcuts import get_object_or_404

@login_required
def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = user.profile
    tweets = Tweet.objects.filter(user=user).order_by('-created_at')

    return render(request, 'core/user_profile.html', {
        'profile_user': user,
        'profile': profile,
        'tweets': tweets,
    })