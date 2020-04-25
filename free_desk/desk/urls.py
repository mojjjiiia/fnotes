from django.urls import path
from desk import views
from django.contrib.auth.decorators import login_required

app_name = 'desk'

urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index'),
    path('new_post/', login_required(views.NewPostView.as_view()), name='new_post'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_out/', views.sign_out, name='sign_out'),
    path('change_pass/', views.change_pass, name='change_pass'),
    path('account/', login_required(views.AccountView.as_view()), name='account')
]
