from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from posts.views import (
    BaseView,
    HtmlView,
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    post_list_view,
    post_detail_view,
    post_create_view,
    post_update_view,
)

from users.views import (
    register_view,
    login_view,
    logout_view,
    profile_view
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', BaseView.as_view(), name='base'),
    path('html/', HtmlView.as_view(), name='html'),
    path('posts/', post_list_view, name='post_list_view'),
    path('posts/<int:post_id>/', post_detail_view, name='post_detail'),
    path('posts/create/', post_create_view, name='post_create'),
    path('profile/posts/<int:post_id>/update/', post_update_view, name='post_update'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),



    path('posts/class/', PostListView.as_view(), name='post_list_class'),
    path('posts/class/<int:pk>/', PostDetailView.as_view(), name='post_detail_class'),
    path('posts/create/class/', PostCreateView.as_view(), name='post_create_class'),
    path('profile/posts/class/<int:pk>/update/', PostUpdateView.as_view(), name='post_update_class'),
]

# Статические файлы
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
