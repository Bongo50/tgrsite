from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from rpgs.models import Rpg
from .models import Member


class MemberInline(admin.StackedInline):
    model = Member
    can_delete = False
    verbose_name_plural = 'member'


class RpgInline(admin.TabularInline):
    model = Rpg
    extra = 0


class UserAdmin(BaseUserAdmin):
    inlines = (MemberInline,)


class MemberAdmin(admin.ModelAdmin):
    # inlines = (RpgInline,)
    pass


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Member, MemberAdmin)
