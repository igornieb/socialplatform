from django import forms
from core.models import Comment, Account
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'style': 'height:100px',
            })

    class Meta:
        model = Comment
        fields = ['comment']


class AccountForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Account
        fields = ('name', 'profile_picture', 'bio')


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        fields = ('username', 'email', 'password1', 'password2')
        model = User

    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'username',
                                                             'class': 'form-control mb-4',
                                                             }))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-control mb-4',
                                                           }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'class': 'form-control mb-4',
                                                                  }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'class': 'form-control mb-4',
                                                                  }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Confirm Password"


class SearchForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['user']
