from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.forms import modelformset_factory, inlineformset_factory

from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from online_marketplace.products.models import Product, Category, ProductImage  # SubCategory
from online_marketplace.products.forms import ProductForm, ProductUpdateForm, ProductSearchForm, ProductImageForm

ProductImageFormSet = inlineformset_factory(Product, ProductImage, form=ProductImageForm, extra=4)


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-upload_date')
        search_query = self.request.GET.get('search', '')
        category_query = self.request.GET.get('category', '')
        # subcategory_query = self.request.GET.get('subcategory', '')

        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

        if category_query and category_query.isdigit():
            queryset = queryset.filter(category__id=category_query)

        # if subcategory_query and subcategory_query.isdigit():
        #     queryset = queryset.filter(subcategory__id=subcategory_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = ProductSearchForm(self.request.GET)
        context['categories'] = Category.objects.all()
        # context['subcategories'] = SubCategory.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'


# class ProductCreateView(LoginRequiredMixin, CreateView):
#     model = Product
#     form_class = ProductForm
#     template_name = 'products/product_create.html'
#     success_url = reverse_lazy('product list')
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['categories'] = Category.objects.all()
#         # context['subcategories'] = SubCategory.objects.all()
#         return context

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_create.html'
    success_url = reverse_lazy('product list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        ImageFormSet = modelformset_factory(ProductImage, form=ProductImageForm, extra=4)
        context['formset'] = ImageFormSet(queryset=ProductImage.objects.none())

        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)

        ImageFormSet = modelformset_factory(ProductImage, form=ProductImageForm, extra=4)
        formset = ImageFormSet(self.request.POST, self.request.FILES, queryset=ProductImage.objects.none())

        if formset.is_valid():
            for image_form in formset:
                image = image_form.cleaned_data.get('image')
                if image:
                    ProductImage.objects.create(image=image, product=self.object)

        return response


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductUpdateForm
    template_name = 'products/product_update.html'

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        if request.user.is_staff or request.user == product.user:
            return super().dispatch(request, *args, **kwargs)

        return HttpResponseForbidden("You do not have permission to edit this product.")

    def get_success_url(self):
        return reverse('product details', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ProductImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            # Използваме queryset, за да редактираме съществуващите изображения
            context['formset'] = ProductImageFormSet(queryset=self.object.images.all())
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()  # Записваме промените във формата
            formset.instance = self.object
            formset.save()  # Записваме промените във формсета
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        return self.render_to_response(self.get_context_data(form=form))


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('product list')

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        if request.user.is_staff or request.user == product.user:
            return super().dispatch(request, *args, **kwargs)

        return HttpResponseForbidden("You do not have permission to edit this product.")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise Http404()
        return obj
