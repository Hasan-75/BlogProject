from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models
from django.db.models.signals import pre_save
# Create your models here.
from django.urls import reverse
from django.utils.text import slugify


def uploadLocation(instance, filename):
    return "%s+%s" %(instance.id, filename)

class Post(models.Model):
    user=models.ForeignKey(AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    slug=models.SlugField(unique=True)
    content=models.TextField()
    image=models.ImageField(upload_to=uploadLocation, null=True, blank=True, default=None, height_field='height_field', width_field='width_field')
    height_field=models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    timeStamp=models.DateTimeField(auto_now_add=True, auto_now=False)
    update=models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("detail-p", kwargs={'slug':self.slug})
    class Meta:
        ordering=['-timeStamp', '-update']

def createSlug(instance, new_slug=None):
    slug=slugify(instance.title)
    if new_slug is not None:
        slug=new_slug
    posts=Post.objects.filter(slug=slug).order_by('-id')
    exists=posts.exists()
    if exists:
        new_slug="%s-%s" %(slug, posts.first().id)
        return createSlug(instance, new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug=createSlug(instance)


pre_save.connect(pre_save_post_receiver, sender=Post)