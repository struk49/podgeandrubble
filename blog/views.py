from django.shortcuts import render, get_object_or_404
from .models import Blog_post

# Create your views here.

def all_posts(request):
    """ A view to show all posts, including sorting and search queries """

    posts = Blog_post.objects.all()

    context = {
        'posts': posts,
    }

    return render(request, 'blog/blog_post.html', context)


def blog_detail(request, post_id):
    """ A view to show individual post details """

    post = get_object_or_404(Blog_post, pk=post_id)

    context = {
        'post': post,
    }

    return render(request, 'blog/blog_detail.html', context)