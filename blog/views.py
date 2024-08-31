from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.core.paginator import Paginator

from itertools import chain
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
    list_book = Book.objects.filter(name__startswith=letter)
    context = {"books": list_book, "letter": letter}
    return render(request, "blog/list_result_alphabet.html", context)


def view_tag(request, data):
    tag1 = Article.objects.filter(tag=data) + Book.objects.filter(tag=data)
    context = {"tags": tag1, "data": data}
    return render(request, "blog/tag_list.html", context)


class FinalNote(ListView):
    queryset = Book.objects.all().order_by("-create")
    template_name = "blog/final_note.html"
    context_object_name = "final_book"
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = Article.objects.all().order_by("-create")
        paginator = Paginator(article, 6)
        page_num = self.request.GET.get("page")
        second_part = paginator.get_page(page_num)
        context["final_article"] = second_part
        return context


# def final_note(request):
#     book = Book.objects.all().order_by("-create")
#     article = Article.objects.all().order_by("-create")

#     context = {"final_book": book, "final_article": article}

#     return render(request, "blog/final_note.html", context)


class HomeList(ListView):
    queryset = Article.objects.all()
    template_name = "blog/home.html"
    context_object_name = "articles"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_title"] = Title.objects.order_by("-create")[:1]
        context["all_note_article"] = Article.objects.all()[:3]
        context["all_note_book"] = Book.objects.all()[:3]
        context["special_article"] = Article.objects.filter(special=True).order_by(
            "-create"
        )[:5]
        context["special_books"] = Book.objects.filter(special=True).order_by(
            "-create"
        )[:5]
        context["last_note_article"] = Article.objects.order_by("-create")[:3]
        context["last_note_book"] = Book.objects.order_by("-create")[:3]

        return context


class SearchList(ListView):
    template_name = "blog/search_list.html"
    paginate_by = 6

    def get_queryset(self):
        query_search = self.request.GET.get("query")
        return Book.objects.filter(
            Q(description__icontains=query_search) | Q(name__icontains=query_search)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["querys"] = self.request.GET.get("query")
        return context


class ArticleList(ListView):
    queryset = Article.objects.all()
    template_name = "blog/article.html"
    context_object_name = "article_list"
    paginate_by = 6


class ContentDetailView(DetailView):
    template_name = "blog/detail.html"

    def get_object(self):
        model_type = self.kwargs.get("model_type")
        pk = self.kwargs.get("pk")

        if model_type == "article":
            return get_object_or_404(Article, pk=pk)
        elif model_type == "book":
            return get_object_or_404(Book, pk=pk)
        elif model_type == "biography":
            return get_object_or_404(Biography, pk=pk)
        else:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["model_type"] = self.kwargs.get("model_type")
        return context


# class TowModelsDetail(DetailView):
#     template_name = "blog/detail.html"
#     context_object_name = "articles"

#     def get_object(self):
#         global get_id
#         get_id = self.kwargs.get("id")
#         return get_object_or_404(Article, id=get_id)

# def get_context_data(self, **kwargs):
#     context = super().get_context_data(**kwargs)
#     context["books"] = get_object_or_404(Book, id=get_id)


class BookList(ListView):
    queryset = Book.objects.all()
    template_name = "blog/book.html"
    context_object_name = "books"
    paginate_by = 6


# class BookDetail(DetailView):
#     template_name = "blog/detail.html"
#     context_object_name = "details"

#     def get_object(self):
#         get_id = self.kwargs.get("id")
#         return get_object_or_404(Article, id=get_id)


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
    queryset = Article.objects.all().order_by("-create")
    template_name = "blog/writtenworks.html"
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = Article.objects.all().order_by("-create")
        books = Book.objects.all().order_by("-create")
        biographys = Biography.objects.all().order_by("-create")
        combined = sorted(
            chain(books, biographys, article), key=lambda x: x.create, reverse=True
        )
        context["writtenworks"] = combined
        return context


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
        quoteimage = QuoteImage.objects.all().order_by("-create")
        combined = sorted(
            chain(movie, voice, shortsound, quoteimage),
            key=lambda x: x.create,
            reverse=True,
        )
        context["multimedias"] = combined
        return context


# class Letter(ListView):

#     def get_queryset(self):
#         query = self.request.GET.get("letter")
#         for letter in persian_alphabet:
#             if query == letter:
#                 return Book.objects.filter(name__istartswith=letter)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["letters"] = self.request.GET.get("letter")
#         return context
