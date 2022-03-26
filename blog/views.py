from django.db.models import Count
from django.utils import timezone
import datetime
from django.shortcuts import render,get_object_or_404,get_list_or_404
from .models import Post
from django.contrib.postgres.search import SearchVector,SearchQuery,SearchRank
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from .forms import CommentForm,SearchForm
# Create your views here.

def index(request):
    uzb = get_list_or_404(Post,status='published',category='uzb')[:4]
    world = get_list_or_404(Post,status='published',category='world')[:4]
    economy = get_list_or_404(Post,status='published',category='economy')[:4]
    sport = get_list_or_404(Post,status='published',category='sport')[:4]
    science = get_list_or_404(Post,status='published',category='science')[:4]
    shou = get_list_or_404(Post,status='published',category='shou')[:4]
    latest = get_list_or_404(Post,status='published')[:20]

    lastweek = timezone.now() - datetime.timedelta(days=7)
    
    popular = Post.objects.filter(status='published',publish__gt=lastweek).annotate(num_comments=Count('comments')).order_by('num_comments')[:8]
    



    context = {
        'uzb':uzb,
        'world':world,
        'economy':economy,
        'sport':sport,
        'science':science,
        'shou':shou,
        'latest':latest,
        'popular':popular,
        
    }
    return render(request,'blog/index.html',context)



def post_detail(request,post):
    post = get_object_or_404(Post,slug=post,status='published')
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()

    else:
        comment_form = CommentForm()
    comments = post.comments.filter(active=True)

    similar_posts = post.tags.similar_objects()[:4]

    context = {
        'post': post,
        'new_comment':new_comment,
        'comments':comments,
        'comment_form':comment_form,
        'similar_posts':similar_posts,

    }

    return render(request,
                'blog/detail.html',context)
    


def post_list(request,category=''):
    if category:
        posts_list = get_list_or_404(Post,category=category,status='published')
    else:
        posts_list = get_list_or_404(Post,status='published')

    paginator = Paginator(posts_list,8)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request,
                'blog/post_list.html',
                {'posts': posts,})



def search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title',weight = 'A')+SearchVector('body',weight = 'B')
            search_query = SearchQuery(query)
            results = Post.published.annotate(
                rank = SearchRank(search_vector,search_query)).filter(rank__gt=0.3).order_by('-rank')
    
    
    context = {
        'query': query,
        'results': results,

    }

    return render(request,'blog/search.html',context)