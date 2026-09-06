from django.shortcuts import render
from .models import Blog
from .forms import BlogForm, UserRegistrationForm
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.utils.http import url_has_allowed_host_and_scheme
# Create your views here.
def index(request):
    blogs = Blog.objects.all().order_by("-created_at")
    return render(request, 'blog_list.html', {'blogs': blogs, 'show_actions': False})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('blog_list')
    else:
        form = AuthenticationForm(request)
    return render(request, 'registraion/login.html', {'form': form})

def blog_list(request):
    blogs = Blog.objects.all().order_by("-created_at")
    return render(request, 'blog_list.html', {'blogs': blogs, 'show_actions': True})

@login_required
def blog_create(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog =  form.save(commit=False)
            blog.user = request.user
            blog.save()
            return redirect('blog_list') 
    else:
        form = BlogForm()
    return render(request, 'blog_create.html', {"form" :form})

@login_required
def blog_edit(request, blog_id):
    blog = get_object_or_404(Blog, pk = blog_id, user = request.user)
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES, instance = blog)
        if form.is_valid():
            blog =  form.save(commit=False)
            blog.user = request.user
            blog.save()
            return redirect('blog_list') 
        
    else:
        form = BlogForm(instance = blog)
    return render(request, 'blog_create.html', {"form" :form})

@login_required
def blog_delete(request, blog_id):
    blog = get_object_or_404(Blog, pk = blog_id, user = request.user)
    if request.method == "POST":
        blog.delete()
        return redirect('blog_list')
    return render(request, 'blog_confirm_delete.html', {"blog" : blog})

def register(request):
    next_url = request.GET.get('next', 'blog_list')
    if request.method == 'POST':
       form = UserRegistrationForm(request.POST)
       if form.is_valid():
          user =form.save(commit=False)
          user.set_password(form.cleaned_data['password1'])
          user.save()
          login(request, user)
          if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
              return redirect(next_url)
          return redirect('blog_list')
    else :
        form = UserRegistrationForm()
    return render(request, 'registraion/register.html', {"form" : form, "next": next_url})

