from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Q

from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from online_marketplace.products.models import Product, Category
from online_marketplace.products.forms import ProductForm, ProductSearchForm, ProductUpdateForm, \
    ProductImageFormSet


class ProductAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        if request.user.is_staff or request.user == product.user:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden("You do not have permission to edit this product.")


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        category_query = self.request.GET.get('category', '')
        sort_by = self.request.GET.get('sort_by', '-upload_date')

        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

        if category_query and category_query.isdigit():
            queryset = queryset.filter(category__id=category_query)

        if sort_by in ['name', 'price', 'upload_date']:
            order_direction = self.request.GET.get('order_direction', '')
            if order_direction == 'desc':
                sort_by = f"-{sort_by}"
            queryset = queryset.order_by(sort_by)
        else:
            queryset = queryset.order_by('-upload_date')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_form = ProductSearchForm(self.request.GET)
        context['search_form'] = search_form
        context['categories'] = Category.objects.all().order_by('name')
        context['query_params'] = self.request.GET.urlencode()

        category_id = search_form.data.get('category')
        if category_id and category_id.isdigit():
            try:
                context['category'] = Category.objects.get(id=category_id)
            except ObjectDoesNotExist:
                pass

        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_number = self.request.GET.get('page')
        context['page_obj'] = paginator.get_page(page_number)

        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        similar_products = Product.objects.filter(category=product.category).exclude(pk=product.pk).order_by('?')[:4]

        context['similar_products'] = similar_products

        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_create.html'
    success_url = reverse_lazy('product list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['formset'] = ProductImageFormSet(instance=None)
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        formset = ProductImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        if formset.is_valid():
            formset.save()

        return HttpResponseRedirect(self.get_success_url())


class ProductUpdateView(LoginRequiredMixin, ProductAccessMixin, UpdateView):
    model = Product
    form_class = ProductUpdateForm
    template_name = 'products/product_update.html'

    def get_success_url(self):
        return reverse('product details', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ProductImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['formset'] = ProductImageFormSet(instance=self.object)
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()

            for product_image in self.object.images.all():
                if not product_image.image:
                    product_image.delete()

            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        return self.render_to_response(self.get_context_data(form=form))


class ProductDeleteView(LoginRequiredMixin, ProductAccessMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('product list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user and not self.request.user.is_staff:
            raise Http404()
        return obj
