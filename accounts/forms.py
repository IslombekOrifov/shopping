from django import forms
from django.forms import ValidationError
from .models import CustomUser, Profile


class UserLogForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegisterForm(forms.ModelForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'terms')

    def clean_terms(self):
        if not self.cleaned_data['terms']:
            raise ValidationError(
                {'terms': "Shartlarga rozi bo'lmasangiz, sizga saytdan foydalanish mumkin emas!"}
            )
        return self.cleaned_data['terms']
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['new_password1'] != cd['new_password2']:
            raise ValidationError("Parollar mos emas")
        return cd['new_password2']
    

class UserUpdateForm(forms.ModelForm):
     class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'currency')

class PassUpdateForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password1 = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['new_password1'] != cd['new_password2']:
            raise ValidationError("Parollar mos emas")
        return cd['new_password2']


class PassResetForm(forms.Form):
    new_password1 = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['new_password1'] != cd['new_password2']:
            raise ValidationError("Parollar mos emas")
        return cd['new_password2']


# class ProfileRegisterForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ('terms',)


class ProfileUpdateForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(), required=False)
    class Meta:
        model = Profile
        fields = ('image', 'date_of_birth', 'phone')



