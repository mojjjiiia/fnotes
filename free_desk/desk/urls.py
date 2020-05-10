from django.urls import path, re_path
from desk import views
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView

app_name = 'desk'

urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index'),
    path('new_post/', login_required(views.NewPostView.as_view()), name='new_post'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('sign_in/', views.SignInView.as_view(), name='sign_in'),
    path('sign_out/', views.sign_out, name='sign_out'),
    path('change_pass/', login_required(views.ChangePassView.as_view()), name='change_pass'),
    path('account/', login_required(views.AccountView.as_view()), name='account'),
    path('reset/', views.ResetView.as_view(), name='reset'),
    path('successfullreset/', TemplateView.as_view(template_name = 'desk/successfullreset.html'), name='successfullreset')
]
