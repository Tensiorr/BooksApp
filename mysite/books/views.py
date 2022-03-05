from django.shortcuts import render
import requests
from django.views import generic
from django.db.models.functions import Lower
from .form import BookForm

from .models import Book


class IndexView(generic.ListView):
    template_name = "books/index.html"
    context_object_name = 'books'

    def get(self, request):

        if request.GET.get('text_google_api'):
            parameter = request.GET.get('text_google_api')
            r = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={parameter}')
            temp_list = []
            for element in r.json()['items']:
                temp = {}
                if 'title' in element['volumeInfo'].keys():
                    temp['title'] = element['volumeInfo']['title']
                else:
                    temp['title'] = None

                if 'authors' in element['volumeInfo'].keys():
                    name_string = ""
                    for name in element['volumeInfo']['authors']:
                        name_string += name + ", "
                    else:
                        name_string = name_string[:-2]
                    temp['author'] = name_string
                else:
                    temp['author'] = None

                if 'publishedDate' in element['volumeInfo'].keys():
                    split_date = element['volumeInfo']['publishedDate'].split("-")
                    if len(split_date) == 1:
                        date_string = split_date[0] + "-01-01"
                    elif len(split_date) == 2:
                        date_string = split_date[0] + "-" + split_date[1] + "-01"
                    else:
                        date_string = split_date[0] + "-" + split_date[1] + "-" + split_date[2]
                    temp['publication_date'] = date_string
                else:
                    temp['publication_date'] = None

                if 'industryIdentifiers' in element['volumeInfo'].keys():
                    temp['isbn'] = element['volumeInfo']['industryIdentifiers'][0]['identifier']
                else:
                    temp['isbn'] = None

                if 'pageCount' in element['volumeInfo'].keys():
                    temp['pages'] = element['volumeInfo']['pageCount']
                else:
                    temp['pages'] = None

                if 'imageLinks' in element['volumeInfo'].keys():
                    temp['cover'] = element['volumeInfo']['imageLinks']['thumbnail']
                else:
                    temp['cover'] = None

                if 'language' in element['volumeInfo'].keys():
                    temp['language'] = element['volumeInfo']['language']
                else:
                    temp['language'] = None

                temp_list.append(temp)
                obj = Book(**temp)
                try:
                    obj.save()
                except Exception as err:
                    print(f"error message: {err}")

            context = {
                'books': temp_list,
                'search': True,
            }
        elif request.GET.get('search_textbox'):
            parameter = request.GET.get('search_textbox')

            if request.GET.get('option') == "title":
                books = Book.objects.filter(title__icontains=parameter)
            elif request.GET.get('option') == "author":
                books = Book.objects.filter(author__icontains=parameter)
            elif request.GET.get('option') == "language":
                books = Book.objects.filter(language__icontains=parameter)
            else:
                books = {}

            context = {
                'books': books,
            }

        else:
            books = Book.objects.order_by(Lower('title'))
            context = {
                'books': books,
            }
        return render(request, self.template_name, context)


class AddView(generic.TemplateView):
    model = Book
    template_name = 'books/add.html'

    def get(self, request):
        form = BookForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = BookForm(request.POST)
        if form.is_valid():
            book = Book(title=form.cleaned_data['title'],
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
                print(f"error message: {err}")
        return render(request, self.template_name, {'form': form})


class EditView(generic.UpdateView):
    model = Book
    fields = ['title', 'author', 'publication_date', 'isbn', 'pages', 'cover', 'language']
    template_name = 'books/edit.html'

    def post(self, request, pk):
        form = BookForm()
        temp = Book.objects.get(id=pk)
        temp.title = request.POST['title']
        temp.author = request.POST['author']
        temp.publication_date = request.POST['publication_date']
        temp.isbn = request.POST['isbn']
        temp.pages = request.POST['pages']
        temp.cover = request.POST['cover']
        temp.language = request.POST['language']

        temp.save()
        return render(request, self.template_name, {'form': form, 'text': 'Save to db'})


class DetailView(generic.DetailView):
    model = Book
    template_name = 'books/detail.html'