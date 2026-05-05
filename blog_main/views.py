from django.shortcuts import render
from django.http import HttpResponse
from blogs.models import Category, Blog

def home(request):
    categories = Category.objects.all()
    featured_posts = Blog.objects.filter(is_featured=True, status='Published').order_by('updated_at')
    recent_posts = Blog.objects.filter(is_featured=False, status='Published')
    
    context = {
        'categories':categories,
        'featured_posts': featured_posts,
        'posts': recent_posts
    }
    return render(request, 'home.html', context)