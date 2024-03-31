from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Blog_post
from django.contrib import messages

from .models import Blog_post, Category
from .forms import BlogForm

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


def add_post(request):
    """ Add a post to the store """
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added post!')
            return redirect(reverse('add_post'))
        else:
            messages.error(request, 'Failed to add post. Please ensure the form is valid.')
    else:
        form = BlogForm()
        
    template = 'blog/add_post.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


def edit_post(request, post_id):
    """ Edit a post in the store """
    post = get_object_or_404(Blog_post, pk=post_id)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated post!')
            return redirect(reverse('blog_detail', args=[post.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = BlogForm(instance=post)
        messages.info(request, f'You are editing {post.name}')

    template = 'blog/edit_post.html'
    context = {
        'form': form,
        'post': post,
    }

    return render(request, template, context)