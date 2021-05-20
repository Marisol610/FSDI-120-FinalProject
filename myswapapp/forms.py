
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, SetPasswordForm, PasswordChangeForm, PasswordResetForm
from django.utils.translation import gettext, gettext_lazy as _
from myswapapp.models import Order, Profile, Product, OrderProduct, Address, Basket






class LoginForm(forms.Form):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class': 'form-control'}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}))




PAYMENT_CHOICES = {
    ('P', 'PAYPAL')
    
}

class PaymentForm(forms.Form):
    #street_address = forms.CharField(forms.TextInput(attrs={'placeholder': 1234 Maint St}))
    street_address = forms.CharField(required=False)
    state = forms.CharField()
    zipcode = forms.CharField()
    same_as_shipping_address = forms.BooleanField(widget=forms.CheckboxInput())
    save_info = forms.BooleanField(widget=forms.CheckboxInput())
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(choices=PAYMENT_CHOICES))
    paypal_account = forms.CharField()


class UserForm(forms.Form):
	class Meta:
		model = User
		fields = '__all__'
		exclude = ['user']


class ProfilePageForm(forms.Form):
    class Meta:
        model = Profile
        fields = ['user','location','image']
        widgets = {'location':forms.TextInput(attrs={'class': 'form-control'})

        }


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class OrderForm(forms.Form):
    class Meta:
        model = Order
        fields = '__all__'
    


    
class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label="Confirm Password (again)", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'email': 'Email'}
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control'})}
    


class MyPasswordResetForm(PasswordResetForm):
    email =forms.EmailField(label=_("Email"), max_length=254, widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'from-control'}))



class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=("Old Password"),
    strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus':True, 'class':'form-control'}))

    new_password1 = forms.CharField(label=("New Password"),
    strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control'}))
   
    new_password2 = forms.CharField(label=("Confirm New Password"),strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}))


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=("New Password"),
    strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control'}))
   
    new_password2 = forms.CharField(label=("Confirm New Password"),strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}))
