#beeco_app/notifications/models/models.py

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=20, choices=[('like', 'Like'), ('comment', 'Comment')])
    text = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)