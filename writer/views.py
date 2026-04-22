from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from  .forms import ArticleForm,UpdateUserForm
from django.http import HttpResponse

from .models import Article, ArticleImage

# this is for writer logic

#  i have aded deorators so that nobody will access without login cred
@login_required(login_url='my-login')
def writer_dasboard(request):
    return render(request, 'writer/writer-dashboard.html')




@login_required(login_url='my-login') # add deorators so that nobody will access without login cred
def create_article(request):
    form=ArticleForm()

    if request.method=='POST':
        form=ArticleForm(request.POST,request.FILES) # to handle file upload

        if form.is_valid():
            article=form.save(commit=False)
            article.user=request.user

            article.save()
            #for images
            files=request.FILES.getlist('images')
            for file in files:
                ArticleImage.objects.create(article=article,image=file)
            return redirect('my-articles')
        

    context={'CreateArticleForm':form}


    return render(request, 'writer/create-article.html', context)




@login_required(login_url='my-login')


def my_articles(request):

    current_user=request.user.id
    article=Article.objects.all().filter(user=current_user)

    context={'AllArticles':article}


    return render(request,'writer/my-articles.html',context)



@login_required(login_url='my-login')
def update_article(request,pk):


# to secure , relevant user associated with that article only allowed to update
    try:


        article=Article.objects.get(id=pk,user=request.user)

    except:
        return redirect('my-articles')

    form=ArticleForm(instance=article)

    if request.method=='POST':
        form=ArticleForm(request.POST,instance=article)


        if form.is_valid():
            form.save()

            return redirect('my-articles')

            
        

    context={'UpdateArticleForm':form}

    return render(request,'writer/update-article.html',context)





@login_required(login_url='my-login')
def delete_article(request,pk):

    try:

        article=Article.objects.get(id=pk,user=request.user)

    except:

        return redirect('my-articles')


    if request.method=='POST':

        article.delete()

        return redirect('my-articles')

    
    return render(request,'writer/delete-article.html' )



@login_required(login_url='my-login')
def account_management(request):
    form=UpdateUserForm(instance=request.user)


    if request.method=='POST':
        form=UpdateUserForm(request.POST,instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('writer-dashboard')
        

    context={'UpdateUserForm':form}
    return render(request,'writer/account-management.html',context)






        

    






