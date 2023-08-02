from django import forms
from .models import Product, Category, ProductImage  # SubCategory


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'phone_number', 'location', 'category', 'condition',
                  'image']


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'image', 'description', 'price', 'location', 'category']


class ProductSearchForm(forms.Form):
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Търси продукт'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False,
                                      empty_label="Изберете категория...")
    # subcategory = forms.ModelChoiceField(queryset=SubCategory.objects.all(), required=False, empty_label="Изберете подкатегория...")


class ProductImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')

    class Meta:
        model = ProductImage
        fields = ('image',)
