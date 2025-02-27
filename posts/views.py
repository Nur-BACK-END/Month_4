from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import Post
from posts.forms import PostCreateForm, PostUpdateForm, SearchForm


def base_view(request):
    if request.method == "GET":
        return render(request, 'navbar.html')

def html_view(request):
    return render(request, "main.html")


@login_required(login_url='/login/')
def post_list_view(request):
    form = SearchForm(request.GET)  
    query_params = request.GET
    limit = 5

    if 'reset' in query_params:
        return redirect('/posts/')  

    if 'reset' in query_params:  
        query_params = {}  
        form = SearchForm() 

    if request.method == "GET":
        posts = Post.objects.all()
        search = query_params.get("search")
        category_id = query_params.get("category")
        tags = query_params.getlist("tegs")
        ordering = query_params.get("ordering")
        min_rating = query_params.get("min_rating")
        max_rating = query_params.get("max_rating")
        page = int(query_params.get("page")) if query_params.get("page") else 1

        if search:
            posts = posts.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )

        if category_id:
            posts = posts.filter(category_id=category_id)

        if tags:
            tags = [int(tag) for tag in tags]
            posts = posts.filter(tag__id__in=tags)

        if min_rating:
            posts = posts.filter(rate__gte=min_rating)
        if max_rating:
            posts = posts.filter(rate__lte=max_rating)

        if ordering:
            posts = posts.order_by(ordering)

        max_pages = (posts.count() // limit) + (1 if posts.count() % limit else 0)

        start = (page - 1) * limit
        end = page * limit
        posts = posts[start:end]

        context_data = {
            "posts": posts,
            "form": form,
            "max_pages": range(1, max_pages + 1),
            "selected_categories": query_params.getlist("category"),
            "selected_tags": query_params.getlist("tegs"),
            "min_rating": min_rating,
            "max_rating": max_rating,
        }

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
            form.save()
            return redirect('/posts/')

        else:
            return render(request, 'posts/post_create.html', {'form': form})


@login_required(login_url='/login/')
def post_update_view(request, post_id):
    try:
        post = Post.objects.get(id=post_id, author=request.user)
    except Post.DoesNotExist:
        return HttpResponse("Post не найден")
    
    if request.method == "GET":
        form = PostUpdateForm(instance=post)
        return render(request, "posts/post_update.html", context={"form": form})
    
    if request.method == "POST":
        form = PostUpdateForm (request.POST, request.FILES, instance=post)

        if not form.is_valid():
            return render(request, "posts/post_update.html", context={"form": form})
        
        elif form.is_valid():
            form.save()
            return redirect("/profile/")
        else:
            return render(request, 'posts/post_create.html', {'form': form})
        
# Классовые ***************************************


class BaseView(TemplateView):
    template_name = 'navbar.html'
    


class HtmlView(TemplateView):
    template_name = 'main.html'



class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        queryset = Post.objects.all()
        query_params = self.request.GET
        search = query_params.get("search")
        category_id = query_params.get("category")
        tags = query_params.getlist("tegs")
        ordering = query_params.get("ordering")
        min_rating = query_params.get("min_rating")
        max_rating = query_params.get("max_rating")

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if tags:
            tags = [int(tag) for tag in tags]
            queryset = queryset.filter(tag__id__in=tags)

        if min_rating:
            queryset = queryset.filter(rate__gte=min_rating)

        if max_rating:
            queryset = queryset.filter(rate__lte=max_rating)

        if ordering:
            queryset = queryset.order_by(ordering)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_params = self.request.GET

        context['form'] = SearchForm(query_params)
        context['selected_categories'] = query_params.getlist("category")
        context['selected_tags'] = query_params.getlist("tegs")
        context['min_rating'] = query_params.get("min_rating")
        context['max_rating'] = query_params.get("max_rating")
        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'



class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'posts/post_create.html'
    success_url = '/posts/'  


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)



class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostUpdateForm
    template_name = 'posts/post_update.html'
    success_url = '/profile/'