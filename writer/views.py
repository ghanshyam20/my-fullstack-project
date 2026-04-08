from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from  .forms import ArticleForm
from django.http import HttpResponse

# this is for writer logic

#  i have aded deorators so that nobody will access without login cred
@login_required(login_url='my-login')
def writer_dasboard(request):
    return render(request, 'writer/writer-dashboard.html')




@login_required(login_url='my-login') # add deorators so that nobody will access without login cred
def create_article(request):
    form=ArticleForm()

    if request.method=='POST':
        form=ArticleForm(request.POST)

        if form.is_valid():
            article=form.save(commit=False)
            article.user=request.user

            article.save()
            return HttpResponse('Article created!')
        

    context={'CreateArticleForm':form}


    return render(request, 'writer/create-article.html', context)



        

    






