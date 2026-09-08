from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password', 'class' : 'form-control',}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Confirm Password'}))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name',  'email', 'phone_number', 'password']
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        
        # if password and confirm_password:
        #     if password != confirm_password:
        #         self.add_error('confirm_password', "Passwords do not match!")
        # return cleaned_data

        if password != confirm_password:
            raise forms.ValidationError("Password does not match!")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if Account.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    


    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["first_name", "last_name", "phone_number", "profile_picture"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "profile_picture": forms.FileInput(attrs={"class": "form-control-file"}),
        }