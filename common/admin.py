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
)


admin.site.register(
    [
        GetIpAddress,
        Category,
        Article,
        Book,
        Movie,
        Voice,
        Title,
        Biography,
        QuoteImage,
        ShortSound,
        OnlineCourse,
        InPersonCourse,
    ]
)
