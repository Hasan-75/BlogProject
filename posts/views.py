from urllib.parse import quote_plus

from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def createPost(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form=PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.user = request.user
        instance.save()
        if request.method=='POST':
            messages.success(request,"Posted Successfully!")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        if request.method=='POST':
            messages.error(request, "Failed to post!")
    return render(request, 'posts/create.html', {'form':form})

def index(request):
    firstPage=True
    return render(request, 'posts/index.html',{'firstPage':firstPage})

def updatePost(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    post = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        if request.method=='POST':
            messages.success(request,"Saved!")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        if request.method=='POST':
            messages.error(request,"Editing failed!")
    return render(request, 'posts/create.html', {'post':post,'form':form})

def deletePost(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    post=get_object_or_404(Post, slug=slug)
    post.delete()
    return redirect('list-p')

def listPost(request):
    allPost=Post.objects.all()
    search_query=request.GET.get('q')
    if search_query:
        allPost=allPost.filter(
            Q(title__icontains=search_query)|
            Q(content__icontains=search_query) |
            Q(user__first_name__icontains=search_query)|
            Q(user__last_name__icontains=search_query)
        ).distinct()
    paginator = Paginator(allPost, 5)
    page = request.GET.get('page')
    '''try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)'''
    postList = paginator.get_page(page)
    pageRange=range(1, (postList.paginator.num_pages)+1);
    return render(request, 'posts/postList.html', {'postList':postList, 'pageRange': pageRange})


def postDetail(request, slug=None):
    post=get_object_or_404(Post, slug=slug)
    shareString=quote_plus(post.content)
    return render(request, 'posts/postDetail.html', {'post':post, 'shareString':shareString})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('list-p')
        else:
            messages.error(request, "Incorrect data!")
    return render(request, 'posts/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')