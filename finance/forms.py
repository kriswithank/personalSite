from .models import Category, Retailer, Transaction, TransactionMethod
from django import forms
from django.utils import timezone



class NewEntryForm(forms.Form):
    date = forms.DateField(
        label='Transaction Date',
        widget=forms.TextInput(attrs={
            'placeholder': 'YYYY-MM-DD',
            'value': str(timezone.now().date())
        })
    )

    payment_method = forms.ModelChoiceField(
        label='Payment method',
        queryset=TransactionMethod.objects.order_by('name'),
        widget=forms.Select(attrs={
            'class': 'ui search dropdown'
        })
    )

    total = forms.DecimalField(max_digits=11, decimal_places=2, label='Total (including tax)')

    tax = forms.DecimalField(max_digits=11, decimal_places=2, required=False)

    retailer = forms.ModelChoiceField(
        label='Retailer',
        queryset=Retailer.objects.order_by('name'),
        widget=forms.Select(attrs={
            'class': 'ui search dropdown'
        })
    )

    categories = forms.ModelMultipleChoiceField(
        label='Categories',
        required=False,
        queryset=Category.objects.order_by('name'),
        widget=forms.SelectMultiple(attrs={
            'class': 'ui search dropdown'
        })
    )

    description = forms.CharField(
        label='Description',
        widget=forms.Textarea(attrs={
            'rows': '2',
            'placeholder': 'Enter your description here...'
        })
    )


    def clean(self):
        cleaned_data = super(NewEntryForm, self).clean()
        total = cleaned_data.get('total')
        tax = cleaned_data.get('tax')

        if (total and tax) and (tax > total):
            self.add_error('tax', 'Tax cannot be greater than total.')


    def save_transaction(self, transaction_to_edit=None):
        """
        Saves the transaction if the form. If there is no transaction_to_edit, then
        a new transaction is created, if not the transaction to edit is altered
        and then saved.
        """
        if transaction_to_edit:
            obj = transaction_to_edit
        else:
            obj = Transaction()

        obj.date = self.cleaned_data['date']
        obj.transaction_method = self.cleaned_data['payment_method']
        obj.total = self.cleaned_data['total']
        obj.tax = self.cleaned_data['tax']
        obj.retailer = self.cleaned_data['retailer']
        obj.description = self.cleaned_data['description']
        obj.save()   # Necessary for many-to-many relationship of unsaved transactions.
        obj.categories = self.cleaned_data['categories']

        obj.save()


    def populate_form(self, transaction_id):
        """
        Populates the form to represent the transaction values.
        """
        pass
