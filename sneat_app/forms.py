from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate
from .models import Merchant, Transaction
from django.contrib.auth.models import User

class UnifiedLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your username or email',
                'autofocus': True
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your password'
            }
        )
    )
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                try:
                    user_obj = User.objects.get(email=username)
                    user = authenticate(username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass
            
            if user is None:
                raise forms.ValidationError('Invalid username/email or password.')
            elif not user.is_active:
                raise forms.ValidationError('Your account has been disabled.')
            else:
                self.user_cache = user
        
        return self.cleaned_data

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    is_staff = forms.BooleanField(required=False, label='Register as Merchant', help_text='Check this if you want to register as a merchant')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

class MerchantForm(forms.ModelForm):
    # User fields
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='Leave blank to keep current password (for editing)'
    )
    
    class Meta:
        model = Merchant
        fields = ['business_name', 'business_address', 'status']
        widgets = {
            'business_name': forms.TextInput(attrs={'class': 'form-control'}),
            'business_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Editing existing merchant - populate user fields
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['password'].required = False
        else:
            # Creating new merchant - password is required
            self.fields['password'].required = True
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if self.instance and self.instance.pk:
            # Editing - check if username changed and if it's unique
            if username != self.instance.user.username:
                if User.objects.filter(username=username).exists():
                    raise forms.ValidationError('A user with this username already exists.')
        else:
            # Creating - check if username is unique
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError('A user with this username already exists.')
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if self.instance and self.instance.pk:
            # Editing - check if email changed and if it's unique
            if email != self.instance.user.email:
                if User.objects.filter(email=email).exists():
                    raise forms.ValidationError('A user with this email already exists.')
        else:
            # Creating - check if email is unique
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('A user with this email already exists.')
        return email

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['merchant', 'amount', 'type', 'description']
        widgets = {
            'merchant': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Current Password'
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='New Password'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Confirm New Password'
    )
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError('New passwords do not match.')
        
        return cleaned_data
