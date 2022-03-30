from django.urls import reverse
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import pre_save,post_save
from taggit.managers import TaggableManager
from random import randint

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class DraftManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='draft')


###################################################


class Post(models.Model):
    STATUS_CHOICE = (
        ('draft','Draft'),
        ('published','Published')
    )
    CATEGORY_CHOICES = (
        ('uzb',"O\'zbekiston"),
        ('world','Jahon'),
        ('economy','Iqtisodiyot'),
        ('sport','Sport'),
        ('science','Fan-texnika'),
        ('shou','Shou-biznes')

        )
    picture = models.CharField(max_length=2000)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,unique=True,null=False,blank=False)
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
    body = models.TextField()
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICE,default='draft')
    tags = TaggableManager()
    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title
    
    



    def get_absolute_url(self):
        return reverse('blog:post_detail',args=(self.slug,))



    def get_update_url(self):
        return reverse('accounts:update',args=(self.id,))
    

    def get_delete_url(self):
        return reverse('accounts:delete',args=(self.id,))


    objects = models.Manager()
    published = PublishedManager()
    drafts = DraftManager()





def slugify_instance_title(instance,sender,*args,**kwargs):
    slug = slugify(instance.title)
    if not sender.objects.filter(slug=slug).exists():
        instance.slug = slug
    else:
        while(sender.objects.filter(slug=slug).exists()):
            slug = slugify(instance.title)+'-'+str(randint(0,1000))
    instance.slug = slug


pre_save.connect(slugify_instance_title,Post)
    

##################################################################################
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=40)
    body = models.TextField()
    email = models.EmailField()
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
    class Meta:
        ordering = ('created',)