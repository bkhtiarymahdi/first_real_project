from django.contrib import admin
from .models import (
    GetIpAddress,
    Category,
    Article,
    Movie,
    Voice,
    Title,
    Book,
    Biography,
    QuoteImage,
    ShortSound,
    OnlineCourse,
    InPersonCourse,
    Order,
    OrderItem,
    Transaction,
    User_Access,
    Pamphlets,
)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "create", "img_tag", "special")
    list_filter = ("create", "special")
    search_fields = ('title', 'description')
admin.site.register(Article, ArticleAdmin)


class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "create", "img_tag", "special")
    list_filter = ("create", "special")
    search_fields = ('title', 'description')
admin.site.register(Book, BookAdmin)


class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "create", "img_tag", "special")
    list_filter = ("create", "special")
    search_fields = ('title', 'description')
admin.site.register(Movie, MovieAdmin)

# class VoiceAdmin(admin.ModelAdmin):
#     list_display = ("title", "create", "special", "img_tag")
#     list_filter = ("create", "special")
#     search_fields = ('title', 'description')
# admin.site.register(Voice, VoiceAdmin)

# class ShortSoundAdmin(admin.ModelAdmin):
#     list_display = ("title", "create", "special", "img_tag")
#     list_filter = ("create", "special")
#     search_fields = ('title', 'description')
# admin.site.register(ShortSound, ShortSoundAdmin)

# class BiographyAdmin(admin.ModelAdmin):
#     list_display = ("title", "create", "special", "img_tag")
#     list_filter = ("create", "special")
#     search_fields = ('title', 'description')
# admin.site.register(Biography, BiographyAdmin)

# class PamphletsAdmin(admin.ModelAdmin):
#     list_display = ("title", "create", "special", "img_tag")
#     list_filter = ("create", "special")
#     search_fields = ('title', 'description')
# admin.site.register(Pamphlets, PamphletsAdmin)

# class InPersonCourseAdmin(admin.ModelAdmin):
#     list_display = ("title", "create", "special", "img_tag")
#     list_filter = ("create", "special")
#     search_fields = ('title', 'description')
# admin.site.register(InPersonCourse, InPersonCourseAdmin)

# class OnlineCourseAdmin(admin.ModelAdmin):
#     list_display = ("title", "create", "special", "img_tag")
#     list_filter = ("create", "special")
#     search_fields = ('title', 'description')
# admin.site.register(OnlineCourse, OnlineCourseAdmin)

# class QuoteImageAdmin(admin.ModelAdmin):
#     list_display = ("title", "create", "special", "img_tag")
#     list_filter = ("create", "special")
#     search_fields = ('title', 'description')
# admin.site.register(QuoteImage, QuoteImageAdmin)

# admin.site.register(
#     [
#         Title,
#         Voice,
#         Order,
#         Category,
#         OrderItem,
#         Biography,
#         Pamphlets,
#         QuoteImage,
#         ShortSound,
#         Transaction,
#         User_Access,
#         OnlineCourse,
#         GetIpAddress,
#         InPersonCourse,
#     ]
# )
