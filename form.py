from django import forms

from OnlineLibrary.library.models import Profile, Book


class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'First Name'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Last Name'
                }
            ),
            'image_url': forms.URLInput(
                attrs={
                    'placeholder': 'URL'
                }
            ),
        }


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'


class DeleteProfileForm(forms.ModelForm):
    def save(self, commit=True):
        if commit:
            self.instance.delete()
            return self.instance

    class Meta:
        model = Profile
        fields = '__all__'

        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'readonly': 'readonly',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'readonly': 'readonly',
                }
            ),
            'image_url': forms.URLInput(
                attrs={
                    'readonly': 'readonly',
                }
            ),
        }


class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': 'Title',
                },
            ),
            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Description',
                },
            ),
            'image': forms.URLInput(
                attrs={
                    'placeholder': 'Image',
                },
            ),
            'type': forms.TextInput(
                attrs={
                    'placeholder': 'Type',
                },
            ),
            'user': forms.HiddenInput(),
            # hardcore to profile
        }


class DeleteBookForm(forms.ModelForm):
    def save(self, commit=True):
        if commit:
            self.instance.delete()
            return self.instance

    class Meta:
        model = Book
        fields = '__all__'
        # exclude = ('user_id',)

        widgets = {
            'user_id': forms.HiddenInput(),
        }


class EditBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = (
            'title',
            'description',
            'image',
            'type',
        )
