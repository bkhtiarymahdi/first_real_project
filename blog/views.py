from typing import Any
from django.apps import apps
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q, Count
from django.core.paginator import Paginator, Page
from django.utils.text import slugify

import re
from itertools import chain
from taggit.models import Tag
from common.choices import persian_alphabet
from common.models import (
    Article,
    Book,
    Voice,
    Movie,
    Title,
    Category,
    Biography,
    QuoteImage,
    ShortSound,
    OnlineCourse,
    InPersonCourse,
    Pamphlets,
)


def category_view(request, slug):
    categories = get_object_or_404(
        Category.objects.filter(title__isnull=True, slug=slug)
    )
    return render(request, "blog/category.html", {"categories": categories})


def letter_alphabet(request):
    return render(request, "blog/alphabet.html", {"letters": persian_alphabet})


# search by alphabet
def filter_alphabet(request, letter):
    models = [
        ("book", Book),
        ("article", Article),
        ("biography", Biography),
        ("voice", Voice),
        ("movie", Movie),
        ("shortsound", ShortSound),
        ("pamphlets", Pamphlets),
        ("onlinecourse", OnlineCourse),
        ("inpersoncourse", InPersonCourse),
    ]

    filtered_results = {
        model_name: model.objects.filter(title__startswith=letter)
        for model_name, model in models
        if model.objects.filter(title__startswith=letter).exists()
    }

    return render(
        request,
        "blog/list_result_alphabet.html",
        {"results": filtered_results, "letter": letter},
    )


def view_tag(request, data):
    tag1 = Article.objects.filter(tag=data) + Book.objects.filter(tag=data)
    context = {"tags": tag1, "data": data}
    return render(request, "blog/tag_list.html", context)


class FinalNote(ListView):
    template_name = "blog/final_note.html"
    context_object_name = "final_note"
    paginate_by = 12

    def get_queryset(self):
        article = Article.objects.all().order_by("-create")
        book = Book.objects.all().order_by("-create")
        biography = Biography.objects.all().order_by("-create")
        combined = sorted(
            chain(article, book, biography),
            key=lambda x: x.create,
        )
        return combined


class HomeList(ListView):
    queryset = Article.objects.all()
    template_name = "blog/home.html"
    context_object_name = "articles"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        models = [Article, Book, Biography, Pamphlets, OnlineCourse, InPersonCourse]

        special_items = sorted(
            chain(*[model.objects.filter(special=True) for model in models]),
            key=lambda x: x.create,
            reverse=True,
        )[:5]

        context["special_items"] = special_items

        context["top_tags"] = Tag.objects.annotate(
            num_times_used=Count("taggit_taggeditem_items")
        ).order_by("-num_times_used")[:10]
        context["header_title"] = Title.objects.order_by("-create")[:1]
        context["all_note_article"] = Article.objects.order_by("-create")[:3]
        context["all_note_book"] = Book.objects.order_by("-create")[:3]

        last_notes = sorted(
            chain(
                Article.objects.order_by("-create")[:3],
                Book.objects.order_by("-create")[:3],
            ),
            key=lambda x: x.create,
            reverse=True,
        )
        context["last_note"] = last_notes

        return context


class SearchList(ListView):
    template_name = "blog/search_list.html"

    def get_queryset(self):
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_search = self.request.GET.get("query")

        models = [
            Book,
            Article,
            Biography,
            Voice,
            Movie,
            ShortSound,
            Pamphlets,
            OnlineCourse,
            InPersonCourse,
        ]

        search_results = []

        for model in models:
            results = model.objects.filter(Q(title__icontains=query_search))
            search_results.extend(results)

        context["search_results"] = search_results
        context["query_search"] = query_search
        return context


class ArticleList(ListView):
    queryset = Article.objects.all()
    template_name = "blog/article.html"
    context_object_name = "article_list"
    paginate_by = 6


class ContentDetailView(DetailView):
    template_name = "blog/detail.html"

    def get_object(self):
        type = self.kwargs.get("type")
        pk = self.kwargs.get("pk")

        if type == "article":
            return get_object_or_404(Article, pk=pk)
        elif type == "book":
            return get_object_or_404(Book, pk=pk)
        elif type == "biography":
            return get_object_or_404(Biography, pk=pk)
        else:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = self.kwargs.get("type")
        return context


class BookList(ListView):
    queryset = Book.objects.all()
    template_name = "blog/book.html"
    context_object_name = "books"
    paginate_by = 6


class BiographyList(ListView):
    queryset = Biography.objects.all()
    template_name = "blog/biography.html"
    context_object_name = "biographys"
    paginate_by = 6


class QuoteImageList(ListView):
    queryset = QuoteImage.objects.all()
    template_name = "blog/quoteimage.html"
    context_object_name = "quoteimages"
    paginate_by = 6


class VoiceList(ListView):
    queryset = Voice.objects.all()
    template_name = "blog/voice.html"
    context_object_name = "voices"
    paginate_by = 15


class ShortSoundList(ListView):
    queryset = ShortSound.objects.all()
    template_name = "blog/shortsound.html"
    context_object_name = "shortsounds"
    paginate_by = 15


class MovieList(ListView):
    queryset = Movie.objects.all()
    template_name = "blog/movie.html"
    context_object_name = "movies"
    paginate_by = 15


class OnlineCourseList(ListView):
    queryset = OnlineCourse.objects.all()
    template_name = "blog/online_course.html"
    context_object_name = "onlinecourse"
    paginate_by = 4


class InPersonCourseList(ListView):
    queryset = InPersonCourse.objects.all()
    template_name = "blog/in_person_course.html"
    context_object_name = "in_person_course"
    paginate_by = 4


class WrittenWorks(ListView):
    template_name = "blog/writtenworks.html"
    context_object_name = "writtenworks"
    paginate_by = 15

    def get_queryset(self):
        article = Article.objects.all().order_by("-create")
        books = Book.objects.all().order_by("-create")
        biographys = Biography.objects.all().order_by("-create")
        combined = sorted(
            chain(books, biographys, article), key=lambda x: x.create, reverse=True
        )
        return combined


def detail_view(request, type, pk):
    if type == "movie":
        obj = get_object_or_404(Movie, pk=pk)
    elif type == "voice":
        obj = get_object_or_404(Voice, pk=pk)
    elif type == "shortsound":
        obj = get_object_or_404(ShortSound, pk=pk)
    # else:
    #     return render(
    #         request, "404.html"
    #     )

    context = {
        "object": obj,
        "type": type,
    }
    return render(request, "blog/multimedia_detail.html", context)


class MultiMediaList(ListView):
    queryset = Movie.objects.all().order_by("-create")
    template_name = "blog/multimedia.html"
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie = Movie.objects.all().order_by("-create")
        voice = Voice.objects.all().order_by("-create")
        shortsound = ShortSound.objects.all().order_by("-create")
        combined = sorted(
            chain(movie, voice, shortsound),
            key=lambda x: x.create,
            reverse=True,
        )
        context["multimedias"] = combined
        return context


def tag_search(request):
    query = request.GET.get("tag")
    results = []

    if query:
        model_names = [
            "Book",
            "Article",
            "Biography",
            "Voice",
            "Movie",
            "ShortSound",
            "Pamphlets",
            "OnlineCourse",
            "InPersonCourse",
        ]

        for model_name in model_names:
            model = apps.get_model("common", model_name)
            filtered_objects = model.objects.filter(tag__name=query)
            if filtered_objects.exists():
                results.extend(filtered_objects)

    context = {
        "results": results,
        "query": query,
    }
    return render(request, "blog/tag_filter_results.html", context)
