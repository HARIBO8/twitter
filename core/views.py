from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


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
    filter_type = request.GET.get('filter', 'all')

    if filter_type == 'follow':
        # フォロー中ユーザーの投稿（リプライを除く）
        following_ids = Follow.objects.filter(follower=request.user).values_list('following__id', flat=True)
        tweets = Tweet.objects.filter(
            user__id__in=following_ids,
            parent__isnull=True
        ).order_by('-created_at')
    else:
        # 全ユーザーの投稿（リプライを除く）
        tweets = Tweet.objects.filter(
            parent__isnull=True
        ).order_by('-created_at')

    return render(request, 'core/home.html', {
        'tweets': tweets,
        'filter_type': filter_type,
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
    profile_user = request.user  # 自分のプロフィール
    profile = profile_user.profile
    tweets = Tweet.objects.filter(user=profile_user, parent__isnull=True).order_by('-created_at')
    return render(request, 'core/profile.html', {
        'profile_user': profile_user,
        'profile': profile,
        'tweets': tweets,
        'is_owner': True  # 自分自身なのでTrue
    })

@login_required
def profile_view(request, user_id=None):
    if user_id:
        profile_user = get_object_or_404(User, id=user_id)
    else:
        profile_user = request.user
    profile = profile_user.profile
    tweets = Tweet.objects.filter(user=profile_user, parent__isnull=True).order_by('-created_at')
    is_owner = request.user == profile_user
    return render(request, 'core/profile.html', {
        'profile_user': profile_user,
        'profile': profile,
        'tweets': tweets,
        'is_owner': is_owner
    })


from django.http import JsonResponse
from .models import Follow

@login_required
def toggle_follow(request, user_id):
    target = get_object_or_404(User, id=user_id)
    if target == request.user:
        return JsonResponse({'error': '自分はフォローできません。'}, status=400)

    follow_obj, created = Follow.objects.get_or_create(follower=request.user, following=target)
    if not created:
        follow_obj.delete()
        return JsonResponse({'status': 'unfollowed'})
    else:
        return JsonResponse({'status': 'followed'})
    

@login_required
def get_followers(request, user_id):
    user = get_object_or_404(User, id=user_id)
    followers = user.follower_set.select_related('follower')
    data = [{'username': f.follower.username} for f in followers]
    return JsonResponse(data, safe=False)

@login_required
def get_following(request, user_id):
    user = get_object_or_404(User, id=user_id)
    followings = user.following_set.select_related('following')
    data = [{'username': f.following.username} for f in followings]
    return JsonResponse(data, safe=False)


from django.http import JsonResponse
from .models import Like, Tweet

@login_required
def toggle_like(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    like, created = Like.objects.get_or_create(user=request.user, tweet=tweet)
    if not created:
        like.delete()
        status = 'unliked'
    else:
        status = 'liked'
    return JsonResponse({'status': status, 'count': tweet.likes.count()})


@login_required
def reply_tweet(request, tweet_id):
    parent = get_object_or_404(Tweet, id=tweet_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Tweet.objects.create(user=request.user, content=content, parent=parent)
            return redirect('home')
    
    return render(request, 'core/reply.html', {'parent': parent})


@login_required
def retweet(request, tweet_id):
    original = get_object_or_404(Tweet, id=tweet_id)

    # 同じ投稿をリツイート済かどうかチェック（1回のみ許可）
    already = Tweet.objects.filter(user=request.user, original=original).exists()
    if not already:
        Tweet.objects.create(user=request.user, original=original)
    
    return redirect('home')

@login_required
def search(request):
    query = request.GET.get('q', '')
    tweets = []

    if query.startswith('#'):
        # ハッシュタグ検索
        tag = query[1:]  # 先頭の # を除去
        tweets = Tweet.objects.filter(content__icontains=f'#{tag}', parent__isnull=True).order_by('-created_at')

    return render(request, 'core/search.html', {
        'query': query,
        'tweets': tweets,
    })


from django.http import JsonResponse

@login_required
def toggle_retweet(request, tweet_id):
    original = get_object_or_404(Tweet, id=tweet_id)
    existing = Tweet.objects.filter(user=request.user, original=original).first()

    if existing:
        existing.delete()
        status = 'unretweeted'
    else:
        Tweet.objects.create(user=request.user, original=original)
        status = 'retweeted'

    count = original.retweets.count()
    return JsonResponse({'status': status, 'count': count})


@login_required
def edit_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id, user=request.user)

    if request.method == 'POST':
        tweet.content = request.POST.get('content')
        tweet.save()
        return redirect('profile')

    return render(request, 'core/edit_tweet.html', {'tweet': tweet})

@login_required
def delete_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id, user=request.user)
    tweet.delete()
    return redirect('profile')


def tweet_detail(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    replies = tweet.replies.all()  # 親がこのtweetのリプライたち
    return render(request, 'core/tweet_detail.html', {
        'tweet': tweet,
        'replies': replies,
    })


from .forms import ProfileForm

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # プロフィールページに戻る
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'core/edit_profile.html', {'form': form})

