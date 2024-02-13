from django.db import models

from accounts.models import CustomUser

class CustomPostManager(models.Manager):
    def for_user(self, user):
        if user.is_authenticated:
            return self.all()
        else:
            return self.filter(is_authenticated_only=False)
        

class Post(models.Model):
    title = models.CharField(max_length=400)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    is_authenticated_only = models.BooleanField(default=False)

    objects = CustomPostManager()

    def upvote(self):
        self.upvotes += 1
        self.save()

    def downvote(self):
        self.downvotes += 1
        self.save()

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

    def upvote(self):
        self.upvotes += 1
        self.save()

    def downvote(self):
        self.downvotes += 1
        self.save()

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"


