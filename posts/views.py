from django.shortcuts import render, redirect
from .models import Post
from posts.forms import PostCreateForm
from django.contrib.auth.decorators import login_required


# Регистрация - это создание нового пользователя в базе данных 

# Аунтефикация - это поиск существуюшего пользователя в бвзе данных (по переданым каким то криденшилэсам там наример (логин пароль) коким то таким)

# Афторизация - это когда мы уже нашли пользователя (в базе данных)сушествуюшего. В краце выдача прав то что он может посешять на сайте 



def base_view(request):
    if request.method == "GET":
        return render(request, 'navbar.html')


def html_view(request):
    return render(request, "main.html")


@login_required(login_url='/login/')
def post_list_view(request):
    if request.method == "GET":
        posts = Post.objects.all()
        return render(request, "posts/post_list.html", context={"posts": posts})


@login_required(login_url='/login/')
def post_detail_view(request, post_id):
    if request.method == "GET":
        post = Post.objects.get(id=post_id)
        return render(request, "posts/post_detail.html", context={"post": post})



@login_required(login_url='/login/')
def post_create_view(request):
    if request.method == 'GET':
        form = PostCreateForm()
        return render(request, 'posts/post_create.html', {'form': form})
    
    
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)


        if form.is_valid():
            image = form.cleaned_data.get('image')
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            form.save()
            return redirect('/posts/')
        
        
        else:
            return render(request, 'posts/post_create.html', {'form': form})
