import logging
from datetime import datetime

import requests
from django.db.models.functions import Lower
from django.shortcuts import render
from django.views import generic
from django_filters import rest_framework as filters
from rest_framework import viewsets, mixins

from .form import BookForm
from .models import Book
from .serializer import BookSerializer

logger = logging.getLogger(__name__)


def validate_date(date_str):
    try:
        if date_str != datetime.strptime(date_str, "%Y-%m-%d").strftime('%Y-%m-%d'):
            raise ValueError
        return True
    except ValueError:
        return False


class IndexView(generic.ListView):
    template_name = "books/index.html"
    context_object_name = 'books'

    def get(self, request):

        books = Book.objects.order_by(Lower('title'))
        context = {
            'books': books,
        }

        if request.GET.get('text_google_api'):
            parameter = request.GET.get('text_google_api')
            r = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={parameter}')
            temp_list = []
            for element in r.json()['items']:
                temp = {
                    'title': None,
                    'author': None,
                    'publication_date': None,
                    'isbn': None,
                    'pages': None,
                    'cover': None,
                    'language': None,
                }

                if 'title' in element['volumeInfo'].keys():
                    temp['title'] = element['volumeInfo']['title']

                if 'authors' in element['volumeInfo'].keys():
                    temp['author'] = ', '.join(element['volumeInfo']['authors'])

                if 'publishedDate' in element['volumeInfo'].keys():
                    if not validate_date(element['volumeInfo']['publishedDate']):
                        split_date = element['volumeInfo']['publishedDate'].split("-")
                        if len(split_date) == 1:
                            date_string = split_date[0] + "-01-01"
                        else:
                            date_string = split_date[0] + "-" + split_date[1] + "-01"
                        temp['publication_date'] = date_string
                    else:
                        temp['publication_date'] = element['volumeInfo']['publishedDate']

                if 'industryIdentifiers' in element['volumeInfo'].keys():
                    temp['isbn'] = element['volumeInfo']['industryIdentifiers'][0]['identifier']

                if 'pageCount' in element['volumeInfo'].keys():
                    temp['pages'] = element['volumeInfo']['pageCount']

                if 'imageLinks' in element['volumeInfo'].keys():
                    temp['cover'] = element['volumeInfo']['imageLinks']['thumbnail']

                if 'language' in element['volumeInfo'].keys():
                    temp['language'] = element['volumeInfo']['language']

                temp_list.append(temp)
                obj = Book(**temp)
                try:
                    obj.save()
                except Exception as err:
                    logger.error(f"error message: {err}")

            context = {
                'books': temp_list,
                'search': True,
            }
        elif request.GET.get('search_textbox') or request.GET.get('datestart') or request.GET.get('dateend'):
            parameter = request.GET.get('search_textbox')
            start = request.GET.get('datestart')
            end = request.GET.get('dateend')

            if start > end != "":
                return render(request, self.template_name, context)
            if request.GET.get('option') == "title":
                books = Book.objects.filter(publication_date__range=[start if start != "" else "0001-01-01",
                                                                     end if end != "" else datetime.now()],
                                            title__icontains=parameter)
            elif request.GET.get('option') == "author":
                books = Book.objects.filter(publication_date__range=[start if start != "" else "0001-01-01",
                                                                     end if end != "" else datetime.now()],
                                            author__icontains=parameter)
            elif request.GET.get('option') == "language":
                books = Book.objects.filter(publication_date__range=[start if start != "" else "0001-01-01",
                                                                     end if end != "" else datetime.now()],
                                            language__icontains=parameter)

            context = {
                'books': books,
            }

        return render(request, self.template_name, context)


class AddView(generic.TemplateView):
    model = Book
    template_name = 'books/add.html'

    def get(self, request):
        form = BookForm
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = BookForm(request.POST)
        if form.is_valid():
            book = Book(
                title=form.cleaned_data['title'],
                author=form.cleaned_data['author'],
                publication_date=form.cleaned_data['publication_date'],
                isbn=form.cleaned_data['isbn'],
                pages=form.cleaned_data['pages'],
                cover=form.cleaned_data['cover'],
                language=form.cleaned_data['language']
            )
            try:
                book.save()
            except Exception as err:
                return render(request, self.template_name, {'form': form, 'text': err})
            return render(request, self.template_name, {'form': form, 'text': 'Saved to database'})
        return render(request, self.template_name, {'form': form})


class EditView(generic.UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'books/edit.html'

    def post(self, request, pk):
        book = Book.objects.get(id=pk)
        form = BookForm(request.POST, instance=book)

        if form.is_valid():
            try:
                book.save()
            except Exception as err:
                return render(request, self.template_name, {'form': form, 'text': err})
            return render(request, self.template_name, {'form': form, 'text': 'Saved to db'})
        return render(request, self.template_name, {'form': form})


class BookFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    author = filters.CharFilter(field_name='author', lookup_expr='icontains')
    language = filters.CharFilter(field_name='language', lookup_expr='exact')
    publication_date = filters.DateFromToRangeFilter()

    class Meta:
        model = Book
        fields = ['title', 'author', 'language', 'publication_date']


class BookListView(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BookFilter
