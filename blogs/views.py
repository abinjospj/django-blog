from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Blog, Category, Comment
from django.db.models import Q

def posts_by_category(request, id):
    posts = Blog.objects.filter(status='Published', category=id)
    try:
        category = get_object_or_404(Category, id=id) 
    except:
        return redirect('home')

    context = {
        'posts': posts,
        'category': category
    }
    return render(request, 'posts_by_category.html', context)

def blogs(request,slug):
    single_post = get_object_or_404(Blog, slug=slug, status='Published')
    comments = Comment.objects.filter(blog=single_post)
    comment_count = comments.count()

    if request.method == 'POST':
        comment = Comment()
        comment.user = request.user
        comment.blog = single_post
        comment.comment = (request.POST['comment'])
        comment.save()
        return HttpResponseRedirect (request.path_info)

    context = {
        'single_post': single_post,
        'comments': comments,
        'comment_count': comment_count

    }
    return render(request, 'blogs.html', context)


def search(request):
    keyword = request.GET.get('keyword')
    
    blogs = Blog.objects.filter(Q(title__icontains=keyword) | Q(short_description__icontains=keyword) | Q(blog_body__icontains=keyword), status='Published')
  
    context = {
        'blogs': blogs,
        'keyword': keyword,
    }
    return render(request, 'search.html', context)
