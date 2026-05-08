from django.shortcuts import render, redirect, get_object_or_404
from blogs.models import Category, Blog
from django.contrib.auth.decorators import login_required, permission_required
from .forms import CategoryForm, BlogPostForm, AddUserForm, EditUserForm 
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


@login_required(login_url='login')
def dashboard(request):
    category_count = Category.objects.all().count()
    blog_count = Blog.objects.all().count()

    context = {
        'category_count':category_count,
        'blog_count':blog_count
    }

    return render(request, 'dashboard/dashboard.html',context)

@login_required(login_url='login')
def categories(request):
    return render(request, 'dashboard/categories.html')

@login_required(login_url='login')
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')    

    form = CategoryForm()
    context = {
        'form':form
    }
    return render(request, 'dashboard/add_category.html', context)

@login_required(login_url='login')
def edit_category(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
    
    form = CategoryForm(instance=category)
    context = {
        'category':category,
        'form':form
    }

    return render(request, 'dashboard/edit_category.html', context)

@login_required(login_url='login')
def delete_category(request, id):
    category = get_object_or_404(Category, id=id)
    category.delete()
    return redirect('categories')

@login_required(login_url='login')
def posts(request):
    posts = Blog.objects.all()
    
    context = {
        'posts': posts
    }
    return render(request, 'dashboard/posts.html', context)

@login_required(login_url='login')
def add_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid:
            post = form.save(commit=False)  #temporarily saving the form
            post.author = request.user
            post.save()

            title = form.cleaned_data['title']
            post.slug = slugify(title) + '-' + str(post.id)
            post.save()
            return redirect('posts')

    form = BlogPostForm()

    context = {
        'form':form
    }

    return render(request, 'dashboard/add_post.html', context)

@login_required(login_url='login')
def edit_post(request, id):
    post = get_object_or_404(Blog, id=id)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        post = form.save()
        post.author = request.user
        
        title = form.cleaned_data['title']
        post.slug = slugify(title) + '-' + str(post.id)
        post.save()
        return redirect('posts')

    form = BlogPostForm(instance=post)
    context = {
        'post':post,
        'form':form
    }
    return render(request, 'dashboard/edit_post.html', context)

@login_required(login_url='login')
def delete_post(request, id):
    post = get_object_or_404(Blog, id=id)
    post.delete()
    return redirect('posts')

@login_required(login_url='login')
def user(request):
    users = User.objects.all()
    context = {
        'users':users
    } 
    return render(request, 'dashboard/user.html', context)

@login_required(login_url='login')
def add_user(request):
    if request.method == "POST":
        form = AddUserForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('users')

    form = AddUserForm()
    context = {
        'form':form
    }
    return render(request, 'dashboard/add_user.html', context)

@login_required(login_url='login')
def edit_user(request, id):
    users = get_object_or_404(User, id=id)
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=users)
        form.is_valid()
        form.save()
        return redirect('users')

    form = EditUserForm(instance=users)
    context = {
        'user':users,
        'form':form
    }
    return render(request, 'dashboard/edit_user.html', context)

@login_required(login_url='login')
def delete_user(request,id):
    user = get_object_or_404(User, id=id)
    user.delete()
    return redirect('users')