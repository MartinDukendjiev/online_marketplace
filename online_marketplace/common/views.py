from django.views.generic import TemplateView

from online_marketplace.products.models import Category, SubCategory


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_term = self.request.GET.get('search', '')
        categories = Category.objects.all()
        if search_term:
            categories = categories.filter(name__icontains=search_term)
        context['categories'] = categories
        context['subcategories'] = SubCategory.objects.all()
        return context
