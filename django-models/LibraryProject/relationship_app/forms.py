from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year', 'libraries']
        widgets = {
            'publication_year': forms.NumberInput(attrs={'min': 1000, 'max': 2100}),
            'libraries': forms.CheckboxSelectMultiple(),
        }