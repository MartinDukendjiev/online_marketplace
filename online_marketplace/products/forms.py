from django import forms
from .models import Product, Category, SubCategory


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'phone_number', 'location', 'category', 'subcategory', 'condition',
                  'image']


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'image', 'description', 'price', 'location', 'category', 'subcategory']

    def save(self, commit=True):
        product = self.instance
        product.name = self.cleaned_data['name']
        product.image = self.cleaned_data['image']
        product.description = self.cleaned_data['description']
        product.price = self.cleaned_data['price']
        product.location = self.cleaned_data['location']
        product.category = self.cleaned_data['category']
        product.subcategory = self.cleaned_data['subcategory']

        if commit:
            product.save()
        return product


class ProductSearchForm(forms.Form):
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Търси продукт'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, empty_label="Изберете категория...")
    subcategory = forms.ModelChoiceField(queryset=SubCategory.objects.all(), required=False, empty_label="Изберете подкатегория...")