from django.shortcuts import redirect, render
from blog.models import Post
from django.contrib.auth.decorators import login_required
from .forms import PostForm,CreateUserForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate




user = User.objects.get(username='admin')
# Create your views here.

@login_required
def index(request):
    posts = Post.objects.all()
    context = {
        'posts':posts,
    }
    return render(request,'accounts/index.html',context)

@login_required
def create(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = user
            post.save()
            for tag in request.POST['tags'].split(','):
                post.tags.add(tag)
            post.save()
            return redirect('accounts:detail',id=post.id)
    return render(request,'accounts/create.html',{'form':form})


@login_required
def update(request,id):
    post = Post.objects.get(id=id)
    form = PostForm(instance=post)
    tags = ''
    for tag in post.tags.all():
        tags+=str(tag)+','
    # print(tags)
    # print(dir(form.fields['tags']))
    # form.fields['tags'].initial = tags
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = user
            post.save()
            for tag in request.POST['tags'].split(','):
                post.tags.add(tag)
            post.save()
            return redirect('accounts:detail',id=post.id)
    return render(request,'accounts/update.html',{'form':form,'tags':tags})

@login_required
def detail(request,id):
    post = Post.objects.get(id=id)
    return render(request,'accounts/details.html',{'post':post})

@login_required
def delete(request,id):
    post = Post.objects.get(id=id)
    if request.method == 'POST':
        post.delete()
        return redirect('accounts:index')

    return render(request,'accounts/delete.html',)


@login_required
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if form.is_valid():
            if password1==password2:
                form.save()
                return redirect('accounts:login')
            # else:
            #     raise ValidationError('Password doesn\'t match')
    return render(request,'accounts/register.html',{'form':form})


def loginview(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('accounts:index')
    return render(request,'accounts/login.html')
