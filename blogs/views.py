from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Blog, Category

# Create your views here.

def posts_by_category(request, id):
    posts = Blog.objects.filter(status='Published', category=id)
    try:
        category = Category.objects.get(id=id) 
    except:
        return redirect('home')

    context = {
        'posts': posts,
        'category': category
    }
    return render(request, 'posts_by_category.html', context)