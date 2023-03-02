from django import forms
from django.core.exceptions import ValidationError
from .models import User, OtpCode, Address
from django.contrib.auth.forms import ReadOnlyPasswordHashField, PasswordChangeForm


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name')

    def clean_pssword2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('passwords dont match')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text="you can change password using <a href=\"../password/\">this "
                                                   "form</a>.")

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name', 'password', 'last_login')


class UserRegistrationForm(forms.Form):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class:': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class:': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=11)

    # password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('this email is already exist')
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        user = User.objects.filter(phone_number=phone).exists()
        if user:
            raise ValidationError('this phone number is already exist')
        OtpCode.objects.filter(phone_number=phone).delete()
        return phone

    # def clean(self):
    #     cd = super().clean()
    #     p1 = cd.get('password1')
    #     p2 = cd.get('password2')
    #     if p1 and p2 and p1 != p2:
    #         raise ValidationError('password must match')


class UserLoginForm(forms.Form):
    phone = forms.CharField(widget=forms.TextInput(attrs={'class:': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'phone_number', 'full_name', 'avatar']

        widgets = {
            'email': forms.TextInput(attrs={'class:': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class:': 'form-control'}),
            'user_name': forms.TextInput(attrs={'class:': 'form-control'}),
            'avatar' : forms.FileInput(attrs={'class': 'form-control-file'})
        }


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['city_name', 'street_name', 'plock_no']

        widgets = {
            'city_name': forms.TextInput(attrs={'class:': 'form-control'}),
            'street_name': forms.TextInput(attrs={'class:': 'form-control'}),
            'plock_no': forms.TextInput(attrs={'class:': 'form-control'}),
        }
