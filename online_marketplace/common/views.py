from django.shortcuts import render
from django.views.generic import TemplateView

from online_marketplace.products.models import Category # SubCategory


class IndexView(TemplateView):
    template_name = 'common/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_term = self.request.GET.get('search', '')
        categories = Category.objects.order_by('name')
        if search_term:
            categories = categories.filter(name__icontains=search_term)
        context['categories'] = categories
        # context['subcategories'] = SubCategory.objects.all()
        return context


def about_view(request):
    return render(request, 'common/about_page.html')