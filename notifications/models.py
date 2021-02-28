from django.db import models

from users.models import Member


# TODO:
# Consider merging notifications of the same type. How do we do this???
# COULD MERGE BY URL

class NotifType:
    NEWSLETTER = 1
    MESSAGE = 2
    RPG_JOIN = 3
    RPG_LEAVE = 4
    RPG_KICK = 5
    RPG_ADDED = 6
    FORUM_REPLY = 7
    OTHER = 8
    RPG_CREATE = 9
    LOAN_REQUESTS = 10


class SubType:
    NONE = 0
    WEB = 1
    SUMMARY = 2
    FULL = 3


class NotificationSubscriptions(models.Model):
    notification_types = [
        (NotifType.NEWSLETTER, 'Newsletter'),
        (NotifType.MESSAGE, 'PMs'),
        (NotifType.LOAN_REQUESTS, 'Loan Request Updates'),
        (NotifType.RPG_JOIN, 'RPG Gains Member'),
        (NotifType.RPG_LEAVE, 'RPG Looses Member'),
        (NotifType.RPG_KICK, 'Kicked from RPG'),
        (NotifType.RPG_ADDED, 'Added to RPG'),
        (NotifType.FORUM_REPLY, 'Forum Replies'),
        (NotifType.RPG_CREATE, 'New RPG Available'),
        (NotifType.OTHER, 'Other Notification')
    ]
    subscription_types = [
        (SubType.NONE, 'None'),
        (SubType.WEB, 'Online Only'),
        (SubType.SUMMARY, 'Summary Email'),
        (SubType.FULL, 'Full Email'),
    ]

    reduced_subscription_types = subscription_types[:3]
    member = models.OneToOneField(Member, on_delete=models.CASCADE)

    newsletter = models.IntegerField(verbose_name='Newsletters', choices=subscription_types, default=SubType.WEB)
    message = models.IntegerField(verbose_name='Receive Direct Messages', choices=reduced_subscription_types,
                                  default=SubType.WEB)
    loan_request = models.IntegerField(verbose_name='A Loan Request Gets Updated', choices=reduced_subscription_types,
                                  default=SubType.WEB)
    rpg_join = models.IntegerField(verbose_name='Someone Joins Your Event', choices=reduced_subscription_types,
                                   default=SubType.WEB)
    rpg_leave = models.IntegerField(verbose_name='Someone Leaves Your Event', choices=reduced_subscription_types,
                                    default=SubType.WEB)
    rpg_kick = models.IntegerField(verbose_name='Removal from an Event', choices=reduced_subscription_types,
                                   default=SubType.WEB)
    rpg_add = models.IntegerField(verbose_name='Addition to an Event', choices=reduced_subscription_types,
                                  default=SubType.WEB)
    forum_reply = models.IntegerField(verbose_name='Reply to a Forum Post You Participated in',
                                      choices=reduced_subscription_types,
                                      default=SubType.WEB)
    rpg_new = models.IntegerField(verbose_name='A New Event is Created', choices=reduced_subscription_types,
                                  default=SubType.NONE)
    other = models.IntegerField(verbose_name='Miscellaneous', choices=reduced_subscription_types, default=SubType.NONE)

    def get_category_subscription(self, category):
        # Map setting value to its ID value
        mapping = {
            NotifType.NEWSLETTER: self.newsletter,
            NotifType.MESSAGE: self.message,
            NotifType.LOAN_REQUESTS: self.loan_request,
            NotifType.RPG_JOIN: self.rpg_join,
            NotifType.RPG_LEAVE: self.rpg_leave,
            NotifType.RPG_KICK: self.rpg_kick,
            NotifType.RPG_ADDED: self.rpg_add,
            NotifType.FORUM_REPLY: self.forum_reply,
            NotifType.RPG_CREATE: self.rpg_new,
            NotifType.OTHER: self.other
        }

        return mapping.get(category, SubType.NONE)

    def __str__(self):
        return str(self.member.equiv_user.username)

    class Meta:
        verbose_name_plural = "Notifications Subscriptions"
        verbose_name = "Notifications Subscription"


class Notification(models.Model):
    notification_types = NotificationSubscriptions.notification_types

    member = models.ForeignKey(Member, related_name='notifications_owned', on_delete=models.CASCADE)
    notif_type = models.IntegerField(choices=notification_types, default=NotifType.OTHER)
    url = models.CharField(max_length=512)
    content = models.TextField(max_length=8192)
    # A value used to group notifications. Usually a relevant primary key (forum thread key, rpg key, etc.):
    merge_key = models.IntegerField(blank=True, null=True)
    is_unread = models.BooleanField(default=True)
    is_emailed = models.BooleanField(default=False)
    time = models.DateTimeField()

    def notify_icon(self):
        default_icon = 'fas fa-circle'
        icons = {
            NotifType.NEWSLETTER: 'fas fa-newspaper',
            NotifType.MESSAGE: 'fas fa-comment-dots',
            NotifType.LOAN_REQUESTS: 'fas fa-exchange-alt',
            NotifType.RPG_JOIN: 'fas fa-sign-in-alt',
            NotifType.RPG_LEAVE: 'fas fa-sign-out-alt',
            NotifType.RPG_KICK: 'fas fa-times',
            NotifType.RPG_ADDED: 'fas fa-magic',
            NotifType.FORUM_REPLY: 'fas fa-quote-right',
            NotifType.RPG_CREATE: 'fas fa-hat-wizard',
            NotifType.OTHER: default_icon
        }
        if self.notif_type in icons:
            return icons[self.notif_type]
        else:
            return default_icon


