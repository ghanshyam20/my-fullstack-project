from django.urls import path 
from .import views



urlpatterns=[
    path('client-dashboard/',views.client_dashboard,name="client-dashboard"),
    
    path('article/<int:id>/', views.article_detail, name='article-detail'),
    path('toggle-like/<int:article_id>/', views.toggle_like, name='toggle-like'),
    path('comment/<int:article_id>/', views.add_comment, name='add-comment'),
    path('toggle-bookmark/<int:article_id>/', views.toggle_bookmark, name='toggle-bookmark'),
    path('report/<int:article_id>/', views.report_article, name='report-article'),
    path('delete-comment/<int:comment_id>/', views.delete_comment, name='delete-comment'),
    path('edit-comment/<int:comment_id>/', views.edit_comment, name='edit-comment'),
    path('subscription/', views.subscription_page, name='subscription-page'),
    path('create-order/', views.create_paypal_order, name='create-order'),
    path('payment-success/', views.payment_success, name='payment-success'),
    path('payment-cancel/', views.payment_cancel, name='payment-cancel'),
    path('protected-image/<int:image_id>/', views.protected_image, name='protected-image'),
    path('bookmarks/', views.bookmarked_articles, name='bookmarked-articles')
   
]