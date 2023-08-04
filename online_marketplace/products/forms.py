from django import forms
from .models import Product, Category, ProductImage


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'phone_number', 'location', 'category', 'condition']


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'location', 'category']


class ProductSearchForm(forms.Form):
    search = forms.CharField(required=False, widget=forms.TextInput())
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)


class ProductImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')

    class Meta:
        model = ProductImage
        fields = ('image',)
