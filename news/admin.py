from django.contrib import admin
from news.models import News, Category
from django.utils.safestring import mark_safe

class NewsAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'category', 'created_at', 'updated_at',
                    'is_published', 'views', 'get_photo')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category')
    fields = ('title', 'category', 'content', 'photo', 'get_photo', 'views',
                    'is_published', 'created_at', 'updated_at')
    readonly_fields = ('get_photo', 'created_at', 'updated_at')
    save_on_top = True

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75" height="65">')
        else:
            return 'нет фото'

    get_photo.short_description = 'МИНИАТЮРА'


class CategoryAdmin(admin.ModelAdmin):

    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.site_title = 'АДМИНИСТРАТИВНЫЙ САЙТ'
admin.site.site_header = 'АДМИНИСТРАТИВНЫЙ САЙТ УПРАВЛЕНИЯ НОВОСТЯМИ'