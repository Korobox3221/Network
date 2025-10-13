from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,  HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import User, Post, Follow, Likes
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import  FollowSerializer, PostSerializer, LikesSerializer
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
def index(request):
    user = request.user
    if request.method=="POST":
        post_text = request.POST["new_post"]
        post = Post(user = user, post_text = post_text)
        post.save()
    posts = Post.objects.all().order_by('-time')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html",
                  {
                      'posts' : posts,
                      'user' : user,
                      'page_obj' : page_obj,
                  })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
@csrf_exempt
def profile(request, user):

    if not User.objects.filter(username=user).exists():
        return HttpResponse("Nonexisting profile")

    profile_user = User.objects.get(username=user)
    visitor = request.user

    #
    if request.method == 'POST':
        try:
            if not request.user.is_authenticated:
                return JsonResponse({'error': 'Authentication required'}, status=401)

            action = request.POST.get('action')  # 'follow' or 'unfollow'

            if action == 'follow':
                # Create follow relationship
                Follow.objects.get_or_create(
                    follower=visitor,
                    following=profile_user
                )
                return JsonResponse({'status': 'followed'})

            elif action == 'unfollow':
                # Remove follow relationship
                Follow.objects.filter(
                    follower=visitor,
                    following=profile_user
                ).delete()
                return JsonResponse({'status': 'unfollowed'})

            else:
                return JsonResponse({'error': 'Invalid action'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    is_following = Follow.objects.filter(
        follower=visitor,
        following=profile_user
    ).exists()
    profile_post = Post.objects.filter(user = profile_user).order_by('-time')
    paginator = Paginator(profile_post, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/profile.html", {
        'profile_user': profile_user,
        'visitor': visitor,
        'is_following': is_following,
        'followers_count': Follow.objects.filter(following=profile_user).count(),
        'following_count': Follow.objects.filter(follower=profile_user).count(),
        'profile_post': profile_post,
        'page_obj': page_obj
    })

@csrf_exempt
@api_view(['GET'])
def follows(request):
    followers = Follow.objects.all()
    serializer = FollowSerializer(followers, many = True)
    return Response(serializer.data)
@csrf_exempt
@login_required
def following_page(request, user):
    if request.user.username != user:
        return HttpResponseForbidden("You can only view your own following page")


    followed_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
    posts = Post.objects.filter(user__in=followed_users).order_by('-time')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following_page.html", {
        'posts': posts,
        'current_user': request.user,
        'page_obj': page_obj
    })

@csrf_exempt
@api_view(['GET', 'PUT'])
def post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data, partial=True)  # Pass the instance
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST', 'PUT'])
def likes(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        try:
            like, created = Likes.objects.get_or_create(
                user=request.user,
                postID=post
            )

            if not created:
                like.delete()
                return Response({'liked': False})
            return Response({'liked': True})
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=404)
    if request.method == 'PUT':

        current_count = post.like_counter


        post.like_counter = request.data.get('like_counter', current_count + 1)
        post.save()

        return Response({
            'status': 'success',
            'new_count': post.like_counter
        })
