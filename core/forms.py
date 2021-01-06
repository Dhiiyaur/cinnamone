from django import forms


PAYMENT_METHOD =  (

    ('Credit Card', 'Credit Card'),
    ('Debit Card', 'Debit Card')
)

class CheckoutFrom(forms.Form):

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'First name',
        'class' : "form-control"
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Last name',
        'class' : "form-control"
    }))
    # email =forms.CharField(widget=forms.TextInput(attrs={
    #     'placeholder' : 'Email',
    #     'class' : "form-control"
    # }))
    address  = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Address',
        'class' : "form-control"
    }))
    phone = forms.IntegerField(widget=forms.TextInput(attrs={
        'placeholder' : 'Phone Number',
        'class' : "form-control"
    }))
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_METHOD)