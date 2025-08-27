# blog/widgets.py
from django import forms

class EnhancedTagWidget(forms.TextInput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.update({
            'class': 'form-control enhanced-tag-input',
            'placeholder': 'Type tags and press Enter or comma...',
            'data-role': 'tagsinput',
            'autocomplete': 'off'
        })
    
    class Media:
        css = {
            'all': ('https://cdnjs.cloudflare.com/ajax/libs/bootstrap-tagsinput/0.8.0/bootstrap-tagsinput.css',)
        }
        js = (
            'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/bootstrap-tagsinput/0.8.0/bootstrap-tagsinput.min.js',
        )