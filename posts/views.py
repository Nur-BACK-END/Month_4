from django.shortcuts import render, redirect
from .models import Post
from posts.forms import PostCreateForm, SearchForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q


# Регистрация - это создание нового пользователя в базе данных 

# Аунтефикация - это поиск существуюшего пользователя в бвзе данных (по переданым каким то криденшилэсам там наример (логин пароль) коким то таким)

# Афторизация - это когда мы уже нашли пользователя (в базе данных)сушествуюшего. В краце выдача прав то что он может посешять на сайте 

"""
posts = [post1, post2, post3, post4, post5, post6, post7, post8, post9, post10, ]
limit = 2
page = 3

start = (page - 1) * limit
end = page * limit

start = (3-1) * 2 = 4
end = 3 * 2 = 6




"""

def base_view(request):
    if request.method == "GET":
        return render(request, 'navbar.html')


def html_view(request):
    return render(request, "main.html")


@login_required(login_url='/login/')
def post_list_view(request):
    form = SearchForm()
    query_params = request.GET
    limit = 5

    if request.method == "GET":
        posts = Post.objects.all()
        search = query_params.get("search")
        category_id = query_params.get("category")
        tags = query_params.getlist("tegs")
        ordering = query_params.get("ordering")
        page = int(query_params.get("page")) if query_params.get("page") else 1
        

        if search:
            posts = posts.filter(
                Q (title__icontains=search) | Q(content__icontains=search)
            )

        if category_id:
            posts = posts.filter(category_id=category_id)
        
        if tags:
            tegs = [int(tag) for tag in tags] 
            posts = posts.filter(tag__id__in=tags)


        if ordering:
            posts = posts.order_by(ordering)

        
        max_pages = posts.count() / limit
        if round(max_pages) < max_pages:
            max_pages = round(max_pages) +1
        else:
            max_pages = round(max_pages)

        start = (page - 1) * limit
        end = page * limit 
        posts = posts[start:end]


        context_data={"posts": posts, "form": form, "max_pages": range(1, max_pages +1)}

        return render(
            request, "posts/post_list.html", 
            context=context_data
            )




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
