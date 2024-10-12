from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=255)
    description = models.TextField(
        null=True,
        blank=True,
        )

    def __str__(self) -> str:
        return self.category_name

class Comment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        )
    video = models.ForeignKey(
        'Video',
        on_delete=models.CASCADE,
        related_name='comments',
        )
    context = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.video.title}"

class Video(models.Model):
    uploader = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='videos',
        )
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    is_free = models.BooleanField(default=True)
    video_url = models.URLField(null=False, blank=False)
    categories = models.ManyToManyField(Category)
    upload_date = models.DateTimeField(auto_now_add=True)
    view_counts = models.IntegerField(default=0)
    like_counts = models.IntegerField(default=0)
    dislike_counts = models.IntegerField(default=0)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def has_access(self, user):
        if user.subscription.plan.plan_name == 'premium':
            return True
        elif user.subscription.plan.plan_name == 'free':
            return self.is_free_content
        return False


    def __str__(self) -> str:
        return self.title
