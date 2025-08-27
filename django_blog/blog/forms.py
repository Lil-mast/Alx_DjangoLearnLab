# blog/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Post, Comment, Tag
from django.utils.text import slugify

class TagWidget(forms.TextInput):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.update({
            'class': 'form-control tag-input',
            'placeholder': 'Enter tags separated by commas (e.g., python, django, web)',
            'data-role': 'tagsinput'
        })

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)
    
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']

class PostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        widget=TagWidget(),
        help_text="Separate tags with commas. Tags will be converted to lowercase."
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your post content here...',
                'rows': 10
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Pre-populate tags field with existing tags
            self.fields['tags'].initial = ', '.join([tag.name for tag in self.instance.tags.all()])
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        return title
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 50:
            raise forms.ValidationError("Content must be at least 50 characters long.")
        return content
    
    def clean_tags(self):
        tags_input = self.cleaned_data.get('tags', '')
        if not tags_input:
            return []
        
        # Split and clean tags
        tag_list = []
        for tag in tags_input.split(','):
            tag_name = tag.strip()
            if tag_name:  # Only add non-empty tags
                tag_list.append(tag_name.lower())
        
        # Validate tag length
        for tag in tag_list:
            if len(tag) > 50:
                raise forms.ValidationError(f"Tag '{tag}' is too long. Maximum length is 50 characters.")
            if len(tag) < 2:
                raise forms.ValidationError(f"Tag '{tag}' is too short. Minimum length is 2 characters.")
        
        return tag_list
    
    def save(self, commit=True):
        post = super().save(commit=False)
        if commit:
            post.save()
            self.save_tags(post)
        return post
    
    def save_tags(self, post):
        """Helper method to save tags for the post"""
        tag_names = self.cleaned_data['tags']
        
        # Clear existing tags
        post.tags.clear()
        
        # Add new tags
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(
                name=tag_name,
                defaults={'slug': slugify(tag_name)}
            )
            post.tags.add(tag)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your comment here...',
                'rows': 4,
                'maxlength': 1000
            })
        }
        labels = {
            'content': 'Your Comment'
        }
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content.strip()) < 10:
            raise forms.ValidationError("Comment must be at least 10 characters long.")
        if len(content.strip()) > 1000:
            raise forms.ValidationError("Comment cannot exceed 1000 characters.")
        return content

class CommentUpdateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'maxlength': 1000
            })
        }