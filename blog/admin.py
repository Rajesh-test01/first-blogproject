from django.contrib import admin
from .models import Blog, Category , Contact , Comment
from django.utils.html import format_html
from .models import See_Our_Blogs

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'short_desc','owner','category', 'created_at', 'image_preview')
    list_filter = ('created_at','owner','category')
    search_fields = ('title', 'short_desc')
    readonly_fields = ('image_preview', 'created_at')

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="80" height="50" style="object-fit:cover;" />',
                obj.image.url
            )
        return "No Image"

    image_preview.short_description = 'Image'

    admin.site.register(Contact)

@admin.register(See_Our_Blogs)
class SeeOurBlogsAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')

admin.site.register(Category)

admin.site.register(Comment)    
