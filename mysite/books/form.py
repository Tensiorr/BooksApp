from django import forms

from .models import Book


class BookForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    author = forms.CharField(max_length=100)
    publication_date = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': "date"}))
    isbn = forms.CharField()
    pages = forms.IntegerField(required=False, min_value=1)
    cover = forms.CharField(max_length=100, required=False)
    language = forms.CharField(max_length=3, required=False)

    class Meta:
        model = Book
        fields = ('title', 'author', 'publication_date', 'isbn', 'pages', 'cover', 'language')

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
