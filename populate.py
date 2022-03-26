import os
import random
import django
from django.utils.text import slugify
from faker import Faker
#
os.environ.setdefault('DJANGO_SETTINGS_MODULE','newsapp.settings')


django.setup()

from django.contrib.auth.models import User
from blog.models import Post

user=User.objects.get(username='admin')

fakegen = Faker()

categories = ['uzb','world','economy','sport','science','shou']
def populate(N=7):
    for i in range(N):
        title = fakegen.text(max_nb_chars=100)
        body = fakegen.text(max_nb_chars=2000)
        category = random.choice(categories)
        picture = fakegen.image_url()
        slug = slugify(title)
        post = Post.objects.create(
            title=title,
            slug=slug,
            author=user,
            body=body,
            status='published',
            category=category,
            picture = picture,
            )
        post.save()


def add_tags():
    tags = []
    for _ in range(15):
        tags.append(fakegen.word())

    posts = Post.published.all()
    #print(posts)
    for post in posts:
        curr_tags = ()
        count_tags = random.randint(2,5)
        for _ in range(count_tags):
            tag = random.choice(tags)
            post.tags.add(tag)
            post.save()
            # curr_tags=curr_tags+(tag,)
        # post.tags.add(curr_tags)
    
if __name__=='__main__':
    print('Populating....')
    populate(100) 
    add_tags()
    print('Populating end')