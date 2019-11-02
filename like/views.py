from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment, Like
from .forms import PostForm, CommentForm
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def home(request):
    posts = Post.objects.all()
    return render(request, 'home.html', {'posts' : posts})

def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'detail.html', {'post' : post})

def new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit = False)
            post.name = request.user.get_username()
            post.pub_date = timezone.now()
            post.save()
            return redirect('/')
    else:
        form = PostForm()
        return render(request, 'new.html', {'form' : form})

def edit(request, post_id):
    post = Post.objects.get(pk = post_id)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('/' + str(post.id))
    else:
        form = PostForm(instance=post)
        return render(request, 'edit.html', {'post':post, 'form':form})

def delete(request, post_id):
    post = Post.objects.get(pk = post_id)
    post.delete()
    return redirect('/')    

def comment_create(request, post_id):
    
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
        return redirect('/' + str(post.id))
        
    else:
        form = CommentForm()
        return render(request, 'detail.html',{'form':form})

def comment_edit(request, post_id, comment_id):
    
    post = Post.objects.get(pk = post_id)
    comment = Comment.objects.get(pk=comment_id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('/' + str(post.id))
    else:
        form = CommentForm(instance=comment)
        return render(request, 'comment_edit.html', {'post':post, 'form':form, 'comment':comment})

def comment_delete(request, post_id, comment_id):

    post = get_object_or_404(Post, pk=post_id)
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    return redirect('/' + str(post.id))


@login_required 
def post_like(request, post_id):
    # 좋아요 구현 코드 작성
    # 구글링 시 '새로고침이 필요한 좋아요'로 찾으면 바로 나옵니다 !
    post = get_object_or_404(Post, pk=post_id)
    # 중간자 모델 Like 를 사용하여, 현재 post와 request.user에 해당하는 Like 인스턴스를 가져온다.
    post_like, post_like_created = post.like_set.get_or_create(user=request.user)
    
    if not post_like_created:
        post_like.delete()
        
    return redirect('/detail/' + str(post.id))

















































def signup(request):
    if request.method == 'POST':
        if request.POST['username'] == '' or request.POST['password'] == '':
            return render(request, 'signup.html', {'error' : '아이디 비밀번호는 필수입니다'})
        
        if request.POST['password'] != request.POST['con_password']:
            return render(request, 'signup.html', { 'error' : '비밀번호 불일치'})
        
        try:
            user = User.objects.get(username = request.POST['username'])
            return render(request, 'signup.html', {'error' : '이미 존재하는 이름'})

        except User.DoesNotExist:
            user = User.objects.create_user(username = request.POST['username'], password = request.POST['password'])

            auth.login(request, user)
    else:
        return render(request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(request, username = username, password = password)

        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            return render(request, 'login.html', {'error' : '아이디 비밀번호 확인 '})

    else:
        return render(request, 'login.html')

def signout(request):
    auth.logout(request)
    return redirect('/')