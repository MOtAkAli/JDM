from django.shortcuts import render
from django.utils import timezone
from django.views.generic.list import ListView

from articles.models import Article

class ArticleListView(ListView):

    model = Article
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

def index(request):
    return render(request, 'home/index.html')


def rent(request):
    return render(request, 'home/cars.html')

