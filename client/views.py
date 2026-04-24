from django.shortcuts import get_object_or_404, render
from writer.models import Article
from django.contrib.auth.decorators import login_required

#for the client 

#decorators 

@login_required(login_url='my-login')
def client_dashboard(request):
    articles=Article.objects.all()
    return render (request, 'client/client-dashboard.html',{
        'articles':articles
    })





@login_required(login_url='my-login')
def article_detail(request, id):
    article = get_object_or_404(Article, id=id)

    return render(request, 'client/article_detail.html', {
        'article': article
    })






