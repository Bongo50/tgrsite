import hashlib
import secrets
import urllib.parse as urllib

from django.contrib.auth.models import User
from django.db import models
from django.core import validators
from django.db.models.query import Q


# extension to django's User class which has authentication details
# as well as some basic info such as name
class Member(models.Model):
    class BADGES:
        SUPERUSER = 1
        EXEC = 2
        EXEXEC = 3
        NONE = False

        _icons = {
            SUPERUSER: "fas fa-crown text-gold",
            EXEC: "fas fa-star text-gold",
            EXEXEC: "fas fa-award text-muted"
        }
        _desc = {
            SUPERUSER: "Admin",
            EXEC: "Exec",
            EXEXEC: "Ex-exec"
        }

        @classmethod
        def icon(cls, category):
            return cls._icons.get(category, False)

        @classmethod
        def desc(cls, category):
            return cls._desc.get(category, False)

    equiv_user = models.OneToOneField(User, on_delete=models.CASCADE)
    discord = models.CharField(max_length=100, blank=True)
    pronoun = models.CharField(max_length=50, blank=True, verbose_name="pronouns")
    bio = models.TextField(max_length=4096, blank=True)
    signature = models.TextField(max_length=1024, blank=True)
    official_photo_url = models.CharField(max_length=512, null=True, blank=True)
    dark = models.BooleanField(default=False, help_text="Enable Dark Mode(beta) on this account")

    def gravatar(self, size=128):
        h = hashlib.md5(
            self.equiv_user.email.encode('utf8').lower()
        ).hexdigest()
        q = urllib.urlencode({
            'd': 'identicon',
            's': str(size),
        })
        return 'https://www.gravatar.com/avatar/{}?{}'.format(h, q)

    @property
    def badge_type(self):
        if self.equiv_user.is_superuser:
            return self.BADGES.SUPERUSER
        elif self.is_exec():
            return self.BADGES.EXEC
        elif self.is_ex_exec():
            return self.BADGES.EXEXEC
        else:
            return self.BADGES.NONE

    @property
    def badge_title(self):
        return self.BADGES.desc(self.badge_type)

    @property
    def badge_icon(self):
        return self.BADGES.icon(self.badge_type)

    def __str__(self):
        return self.equiv_user.username

    @property
    def username(self):
        return self.equiv_user.username

    @property
    def firstname(self):
        return self.equiv_user.first_name

    @property
    def last_name(self):
        return self.equiv_user.last_name

    def notification_count(self):
        return self.notifications_owned.filter(is_unread=True).count()

    def is_exec(self):
        return self.exec_roles.count() > 0 or self.equiv_user.groups.filter(name='exec').exists()

    def is_ex_exec(self):
        return self.equiv_user.groups.filter(name='ex_exec').exists()

    @property
    def is_soc_member(self):
        if self.membership and self.membership.active:
            return True
        else:
            return False

    # Make .member idempotent i.e. user.member is valid even if user is actually a member
    @property
    def member(self):
        return self

    @staticmethod
    def users_with_perm(perm_name):
        return Member.objects.filter(
            Q(equiv_user__is_superuser=True) |
            Q(equiv_user__user_permissions__codename=perm_name) |
            Q(equiv_user__groups__permissions__codename=perm_name)).distinct()


class Membership(models.Model):
    uni_id = models.CharField(max_length=7, validators=[validators.RegexValidator(r'^[0-9]{7}$')])
    uni_email = models.EmailField()
    active = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    member = models.OneToOneField(Member, on_delete=models.CASCADE)


def generate_token():
    return secrets.token_urlsafe(64)


class VerificationRequest(models.Model):
    token = models.CharField(default=generate_token, max_length=100)
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE)