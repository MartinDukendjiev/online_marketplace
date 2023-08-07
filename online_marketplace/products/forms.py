from django import forms
from django.forms import inlineformset_factory

from .models import Product, Category, ProductImage


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'phone_number', 'location', 'category', 'condition']


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'phone_number', 'location', 'category', 'condition']


class ProductSearchForm(forms.Form):
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Search...'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)


class ProductImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image', required=False, widget=forms.ClearableFileInput(attrs={'clearable': False}))

    class Meta:
        model = ProductImage
        fields = '__all__'


ProductImageFormSet = inlineformset_factory(Product, ProductImage, form=ProductImageForm, extra=4)
