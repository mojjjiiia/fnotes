from django.urls import path
from desk import views

app_name = 'desk'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('new_post/', views.new_post, name='new_post'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_out/', views.sign_out, name='sign_out'),
    path('change_pass/', views.change_pass, name='change_pass'),
    path('account/', views.account, name='account')
]
