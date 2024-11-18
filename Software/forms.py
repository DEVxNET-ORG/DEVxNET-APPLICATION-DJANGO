from django import forms
from .models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data['password']  
        user.set_password(password)  
        if commit:
            user.save()
        return user



