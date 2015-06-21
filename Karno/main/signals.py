from django.db.models.signals import post_save
from django.dispatch import receiver
from main.models import Comment, CommentNotification


@receiver(post_save, sender=Comment)
def create_notification(self, sender, **kwargs):
    """
    A function that creates a new notification once a new
    comment is added on a file I shared.
    :author Nourhan Fawzy:
    :param sender, keyword arguments:
    :return:
    """

    if kwargs.get('created', False):
        comment = kwargs.get('instance')
        file_uploaded = comment.file_uploaded

        comments = Comment.objects.filter(file_uploaded=file_uploaded)

        print "signal"

        # create a notification when others comment on file I commented on

        for c in comments:
            if c.user != self.request.user and c.user != file_uploaded.user:
                CommentNotification.objects.create(
                    comment=comment,
                    file_shared=file_uploaded,
                    user_notified=self.request.user).save()

        # create a notification when others comment on file I shared

        CommentNotification.objects.create(
                comment=comment, file_shared=comment.file_uploaded,
                user_notified=comment.file_uploaded.user).save()
