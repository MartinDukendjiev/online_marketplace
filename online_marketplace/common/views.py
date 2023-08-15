from django.shortcuts import render
from django.views.generic import TemplateView

from online_marketplace.products.models import Category


class IndexView(TemplateView):
    template_name = 'common/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_term = self.request.GET.get('search', '')
        categories = Category.objects.order_by('name')
        if search_term:
            categories = categories.filter(name__icontains=search_term)
        context['categories'] = categories
        return context


def about_view(request):
    return render(request, 'common/about_page.html')


def error_404(request, exception):
    return render(request, '404.html', status=404)


def error_500(request):
    return render(request, '500.html', status=500)
