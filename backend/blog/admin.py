from django.contrib import admin

from blog.models import Category, BlogPost, Illustration


admin.site.register(Category)
admin.site.register(BlogPost)
admin.site.register(Illustration)
