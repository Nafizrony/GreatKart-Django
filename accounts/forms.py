from django import forms
from .models import Account

class AccountForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))
    class Meta:
        model = Account
        fields = ['first_name','last_name','email','phone_number','password']

    def clean(self):
        cleaned_data =  super(AccountForm,self).clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Password field does not match')

    
    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'placeholder':'First Name'})
        self.fields['last_name'].widget.attrs.update({'placeholder':'Last Name'})
        self.fields['email'].widget.attrs.update({'placeholder':'Email'})
        self.fields['phone_number'].widget.attrs.update({'placeholder':'Phone Number'})
        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})


        
    

    
    