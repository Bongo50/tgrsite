from django.contrib import admin

from .models import Thread, Response, Forum


class ThreadInline(admin.StackedInline):
    model = Thread
    extra = 0
    autocomplete_fields = ('author',)
    fields = ('title', 'body', 'pub_date', 'is_pinned', 'is_locked', 'author')


class ForumInline(admin.TabularInline):
    model = Forum
    extra = 0


class ResponseInline(admin.StackedInline):
    model = Response
    extra = 0


class ThreadAdmin(admin.ModelAdmin):
    inlines = [ResponseInline]
    list_display = ('title', 'body', 'get_author',)
    list_filter = ['pub_date', 'forum']
    autocomplete_fields = ('author',)


class ResponseAdmin(admin.ModelAdmin):
    model = Response
    list_display = ('body', 'get_author',)
    autocomplete_fields = ('author',)


class ForumAdmin(admin.ModelAdmin):
    model = Forum
    list_display = ('title', 'description', 'get_parent_tree',
                    'get_threads_count', 'get_subforums_str')
    inlines = [ForumInline, ThreadInline]


admin.site.register(Thread, ThreadAdmin)
admin.site.register(Response, ResponseAdmin)
admin.site.register(Forum, ForumAdmin)
