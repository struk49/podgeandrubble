from django.shortcuts import render
from .models import Blog_post

# Create your views here.

def all_posts(request):
    """ A view to show all products, including sorting and search queries """

    posts = Blog_post.objects.all()

    context = {
        'posts': posts,
    }

    return render(request, 'blog/blog_post.html', context)