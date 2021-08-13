from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from core.utils import auto_save_current_user
# Create your models here.

User = get_user_model()


class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title

# Posts Model
class Post(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)  # null == None, blank = ''
    image = models.ImageField(upload_to='post_images')   # BASE_DIR -> media -> post_images
    user = models.ForeignKey(User, on_delete=models.PROTECT, editable=False,related_name='posts')    # user_id
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField(blank=True, null=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        auto_save_current_user(self)
        super(Post, self).save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse('post_detail_view', kwargs={
            'id': self.id
        })

    def get_update_url(self):
        return reverse('post-update', kwargs={
            'pk': self.pk
        })

    def get_delete_url(self):
        return reverse('post_delete_view', kwargs={
            'pk': self.pk
        })


    @property
    def likes_count(self):
        count = self.like.count()
        return count

    @property
    def comments_count(self):
        count = self.comment_set.count()
        return count

    @property
    def view_count(self):
        return PostView.objects.filter(post=self).count()

# Comments Model
class Comment(models.Model):
    text = models.CharField(max_length=240)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    commented_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


# Likes Model
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='like')
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    liked_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.post.id)



# Followers Model
class Follow(models.Model):
    user = models.ForeignKey(User, related_name='follow_follower', on_delete=models.CASCADE, editable=False)
    followed = models.ForeignKey(User, related_name='follow_followed', on_delete=models.CASCADE)
    followed_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.user} --> {self.followed}"


class SavedPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    saved_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.post.pk)
