from django.urls import path
from django.views.generic import TemplateView
from .views import (
    HomeList,
    BookList,
    VoiceList,
    MovieList,
    ArticleList,
    SearchList,
    BiographyList,
    QuoteImageList,
    ShortSoundList,
    OnlineCourseList,
    ContentDetailView,
    FinalNote,
    WrittenWorks,
    MultiMediaList,
    detail_view,
    letter_alphabet,
    filter_alphabet,
    category_view,
    view_tag,
)


app_name = "blog"
urlpatterns = [
    path("", HomeList.as_view(), name="home"),
    path("letter/", letter_alphabet, name="letter"),
    path("books/", BookList.as_view(), name="books"),
    path("notes/", FinalNote.as_view(), name="notes"),
    path("voices/", VoiceList.as_view(), name="voices"),
    path("movies/", MovieList.as_view(), name="movies"),
    path("search/", SearchList.as_view(), name="search"),
    path("notes/<int:id>", FinalNote.as_view(), name="notes"),
    path("articles/", ArticleList.as_view(), name="articles"),
    path("view_tags/<int:data>/", view_tag, name="view_tags"),
    path("category/<slug:slug>/", category_view, name="category"),
    path("biography/", BiographyList.as_view(), name="biography"),
    # path("search/<int:page>", SearchList.as_view(), name="search"),
    path("multimedia/", MultiMediaList.as_view(), name="multimedia"),
    path("quoteimages/", QuoteImageList.as_view(), name="quoteimages"),
    path("shortsounds/", ShortSoundList.as_view(), name="shortsounds"),
    path("writtenworks/", WrittenWorks.as_view(), name="writtenworks"),
    path("<str:type>/<int:pk>/", detail_view, name="detail_multimedia"),
    path("onlinecourses/", OnlineCourseList.as_view(), name="onlinecourses"),
    path("filter_alphabet/<str:letter>/", filter_alphabet, name="filter_alphabet"),
    path(
        "<str:model_type>/<int:pk>/", ContentDetailView.as_view(), name="content_detail"
    ),
]


# other url Miscellaneous
urlpatterns += [
    path(
        "contact_information/",
        TemplateView.as_view(template_name="miscellaneous/contact_information.html"),
        name="contact_information",
    ),
    path(
        "about_us/",
        TemplateView.as_view(template_name="miscellaneous/about_us.html"),
        name="about_us",
    ),
    path(
        "work_with_us/",
        TemplateView.as_view(template_name="miscellaneous/work_with_us.html"),
        name="work_with_us",
    ),
]
