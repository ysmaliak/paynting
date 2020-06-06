from betterforms.multiform import MultiModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Masterpiece, MadeWith, Sort, Profile


class MasterpieceForm(forms.ModelForm):
    class Meta:
        model = Masterpiece
        fields = ['masterpiece_name', 'image', 'description']

    def save_user(self, commit=True):
        objects = super(MasterpieceForm, self).save(commit=False)

        if commit:
            uploaded_by = objects['uploaded_by']
            print(uploaded_by)
            uploaded_by.save()
            masterpiece = objects
            masterpiece.uploaded_by = uploaded_by
            masterpiece.save()


class MadeWithForm(forms.ModelForm):
    class Meta:
        model = MadeWith
        fields = ['hardware', 'software']


class MasterpieceUpdateForm(forms.ModelForm):
    class Meta:
        model = Masterpiece
        fields = ['masterpiece_name', 'image', 'description']


class MasterpieceUpdateMultiForm(MultiModelForm):
    form_classes = {
        'masterpiece': MasterpieceUpdateForm,
        'made_with': MadeWithForm,
    }


class MasterpieceCreationMultiForm(MultiModelForm):
    form_classes = {
        'masterpiece': MasterpieceForm,
        'made_with': MadeWithForm,
    }

    def save_user(self, user):
        objects = super(MasterpieceCreationMultiForm, self).save(commit=False)
        objects['masterpiece'].save_user(user)

    def save_made_with(self, made_with):
        objects = super(MasterpieceCreationMultiForm, self).save(commit=False)
        objects['masterpiece'].save_made_with(made_with)


SORT_TYPES = (
    ('az', 'A to Z'),
    ('za', 'Z to A'),
)


class SortForm(forms.ModelForm):
    sort_type = forms.ChoiceField(choices=SORT_TYPES, required=False)

    class Meta:
        model = Sort
        fields = ['sort_type']


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='Last Name')
    last_name = forms.CharField(max_length=100, help_text='Last Name')
    email = forms.EmailField(max_length=150, help_text='Email')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['signup_confirmation']
