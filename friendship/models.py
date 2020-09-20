from __future__ import unicode_literals
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from chat.models import Chat
from friendship.exceptions import AlreadyExistsError
from friendship.signals import (
    friendship_request_created, friendship_request_rejected,
    friendship_request_canceled, friendship_request_viewed,
    friendship_request_accepted, friendship_removed, block_created,
    block_removed
)

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class FriendshipRequest(models.Model):
    """ Model to represent friendship requests """
    from_user = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='friendship_requests_sent'
    )
    to_user = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='friendship_requests_received'
    )

    message = models.TextField(_('Message'), blank=True)

    created = models.DateTimeField(default=timezone.now)
    rejected = models.DateTimeField(blank=True, null=True)
    viewed = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = _('Friendship Request')
        verbose_name_plural = _('Friendship Requests')
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return "%s" % self.from_user_id

    def accept(self):
        """ Accept this friendship request """
        relation1 = Friend.objects.create(
            from_user=self.from_user,
            to_user=self.to_user
        )

        relation2 = Friend.objects.create(
            from_user=self.to_user,
            to_user=self.from_user
        )

        friendship_request_accepted.send(
            sender=self,
            from_user=self.from_user,
            to_user=self.to_user
        )
        create_chat = Chat.objects.create(name='')
        create_chat.user_list.add(self.from_user_id, self.to_user_id)

        FriendshipRequest.objects.filter(
            from_user=self.to_user,
            to_user=self.from_user
        ).delete()

        FriendshipRequest.objects.filter(
            from_user=self.from_user,
            to_user=self.to_user
        ).delete()
        return True

    def reject(self):
        """ reject this friendship request """
        self.rejected = timezone.now()
        self.save()
        FriendshipRequest.objects.filter(
            from_user=self.from_user,
            to_user=self.to_user
        ).delete()
        friendship_request_rejected.send(sender=self)

    def cancel(self):
        """ cancel this friendship request """
        self.delete()
        friendship_request_canceled.send(sender=self)
        return True

    def mark_viewed(self):
        self.viewed = timezone.now()
        friendship_request_viewed.send(sender=self)
        self.save()
        return True


class FriendshipManager(models.Manager):
    """ Friendship manager """

    def friends(self, user):
        qs = Friend.objects.select_related(
            'from_user', 'to_user'
        ).filter(to_user=user).all().order_by("?")
        friends = [u.from_user for u in qs]
        return friends

    def requests_received(self, user):
        qs = FriendshipRequest.objects.select_related(
            'from_user', 'to_user'
        ).filter(to_user=user).all().order_by("created")
        requests = list(qs)
        return requests

    def sent_requests(self, user):
        qs = FriendshipRequest.objects.select_related(
            'from_user', 'to_user'
        ).filter(from_user=user, rejected__isnull=True).all()
        requests = list(qs)
        return requests

    def unread_requests(self, user):
        qs = FriendshipRequest.objects.select_related(
            'from_user', 'to_user'
        ).filter(to_user=user, viewed__isnull=True).all()
        unread_requests = list(qs)
        return unread_requests

    def unread_request_count(self, user):
        count = FriendshipRequest.objects.select_related(
            'from_user', 'to_user'
        ).filter(to_user=user, viewed__isnull=True).count()
        return count

    def read_requests(self, user):
        qs = FriendshipRequest.objects.select_related(
            'from_user', 'to_user'
        ).filter(to_user=user, viewed__isnull=False).all()
        read_requests = list(qs)
        return read_requests

    def rejected_requests(self, user):
        qs = FriendshipRequest.objects.select_related(
            'from_user', 'to_user'
        ).filter(to_user=user, rejected__isnull=False).all()
        rejected_requests = list(qs)
        return rejected_requests

    def unrejected_requests(self, user):
        qs = FriendshipRequest.objects.select_related(
            'from_user', 'to_user'
        ).filter(to_user=user, rejected__isnull=True).all()
        unrejected_requests = list(qs)
        return unrejected_requests

    def unrejected_request_count(self, user):
        count = FriendshipRequest.objects.select_related(
            'from_user', 'to_user'
        ).filter(to_user=user, rejected__isnull=True).count()
        return count

    def add_friend(self, from_user, to_user, message=None):
        """ Create a friendship request """
        if from_user == to_user:
            raise ValidationError("Users cannot be friends with themselves")

        if self.can_request_send(from_user, to_user):
            raise AlreadyExistsError("Friendship already requested")

        if message is None:
            message = ''

        request, created = FriendshipRequest.objects.get_or_create(
            from_user=from_user,
            to_user=to_user,
        )

        if created is False:
            raise AlreadyExistsError("Friendship already requested")

        if message:
            request.message = message
            request.save()
        friendship_request_created.send(sender=request)

        return request

    def can_request_send(self, from_user, to_user):
        """ Checks if a request was sent """
        if from_user == to_user or FriendshipRequest.objects.filter(
                from_user=from_user, to_user=to_user,
        ) \
                .exists() is False:
            return False
        else:
            return True

    def remove_friend(self, from_user, to_user):
        """ Destroy a friendship relationship """
        try:
            qs = Friend.objects.filter(
                Q(to_user=to_user, from_user=from_user) |
                Q(to_user=from_user, from_user=to_user)
            ).distinct().all()

            if qs:
                friendship_removed.send(
                    sender=qs[0],
                    from_user=from_user,
                    to_user=to_user
                )
                # Chat.objects.filter(user_list=(from_user.id, to_user.id)).delete()
                qs.delete()
                return True
            else:
                return False
        except Friend.DoesNotExist:
            return False
        # Chat.objects.filter(user_list=(from_user, to_user)).delete()


class Friend(models.Model):
    """ Model to represent Friendships """
    to_user = models.ForeignKey(
        AUTH_USER_MODEL, models.CASCADE, related_name='friends'
    )
    from_user = models.ForeignKey(
        AUTH_USER_MODEL, models.CASCADE, related_name='_unused_friend_relation'
    )
    created = models.DateTimeField(default=timezone.now)

    objects = FriendshipManager()

    class Meta:
        verbose_name = _('Friend')
        verbose_name_plural = _('Friends')
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return "User #%s is friends with #%s" % (
            self.to_user_id, self.from_user_id
        )

    def save(self, *args, **kwargs):
        # Ensure users can't be friends with themselves
        if self.to_user == self.from_user:
            raise ValidationError("Users cannot be friends with themselves.")
        super(Friend, self).save(*args, **kwargs)


class BlockManager(models.Manager):
    def blocked(self, user):
        qs = Block.objects.filter(blocked=user).all()
        blocked = [u.blocked for u in qs]
        return blocked

    def blocking(self, user):
        qs = Block.objects.filter(blocker=user).all()
        blocking = [u.blocked for u in qs]
        return blocking

    def add_block(self, blocker, blocked):
        if blocker == blocked:
            raise ValidationError("Users cannot block themselves")
        relation, created = Block.objects.get_or_create(
            blocker=blocker, blocked=blocked
        )

        if created is False:
            raise AlreadyExistsError(
                "User '%s' already blocks '%s'" % (blocker, blocked)
            )
        block_created.send(sender=self, blocker=blocker)
        block_created.send(sender=self, blocked=blocked)
        block_created.send(sender=self, blocking=relation)
        return relation

    def remove_block(self, blocker, blocked):
        """ Remove 'blocker' blocks 'blocked' relationship """
        rel = Block.objects.get(blocker=blocker, blocked=blocked)
        block_removed.send(sender=rel, blocker=rel.blocker)
        block_removed.send(sender=rel, blocked=rel.blocked)
        block_removed.send(sender=rel, blocking=rel)
        rel.delete()
        return True


class Block(models.Model):
    blocker = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blocking'
    )
    blocked = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blockees'
    )
    created = models.DateTimeField(default=timezone.now)
    objects = BlockManager()

    class Meta:
        verbose_name = _('Blocker Relationship')
        verbose_name_plural = _('Blocked Relationships')
        unique_together = ('blocker', 'blocked')

    def __str__(self):
        return "User #%s blocks #%s" % (self.blocker_id, self.blocked_id)

    def save(self, *args, **kwargs):
        # Ensure users can't be friends with themselves
        if self.blocker == self.blocked:
            raise ValidationError("Users cannot block themselves.")
        super(Block, self).save(*args, **kwargs)
