from django import forms


class BookForm(forms.Form):
    title = forms.CharField(max_length=100)
    author = forms.CharField(max_length=100)
    publication_date = forms.DateField()
    isbn = forms.IntegerField()
    pages = forms.IntegerField()
    cover = forms.CharField(max_length=100)
    language = forms.CharField(max_length=3)
