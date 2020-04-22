from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from desk.models import Post
from desk.forms import NewPostForm, SignUpForm, SignInForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.utils import timezone


def index(request):
    posts = Post.objects.all().order_by('-pub_date')
    return render(request, 'desk/post_list.html', {'posts': posts})


@login_required
def new_post(request):

    if request.method == 'POST':
        form = NewPostForm(request.POST)

        if form.is_valid():
            post = Post(
                author=request.user,
                subject=form.cleaned_data['subject'],
                text=form.cleaned_data['text'],
                pub_date=timezone.now())
            post.save()
            return HttpResponseRedirect(reverse('desk:index'))

    form = NewPostForm()
    return render(request, 'desk/new_post.html', {'form': form})


def sign_up(request):
    form = SignUpForm()

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            content = form.cleaned_data
            user = authenticate(
                username=content['username'],
                password=content['password1']
            )

            login(request, user)

            return HttpResponseRedirect(reverse('desk:index'))

    return (render(request, 'desk/sign_up.html', {'form': form}))


def sign_in(request):
    form = SignInForm()

    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():

            content = form.cleaned_data
            user = authenticate(
                username=content['username'],
                password=content['password']
            )

            if not user:
                form.error_message = 'Invalid username or password'

                return render(
                    request,
                    'desk/sign_in.html',
                    {'form': form},
                    status=403
                )

            login(request, user)

            if len(request.GET['next']) != 0:
                redirect_path = request.GET['next']
            else:
                redirect_path = reverse('desk:index')

            return HttpResponseRedirect(redirect_path)

    return render(request, 'desk/sign_in.html', {'form': form})


def sign_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('desk:index'))


@login_required
def change_pass(request):
    user = request.user
    form = PasswordChangeForm(user)

    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            content = form.cleaned_data
            user.set_password(content['new_password1'])
            user.save()

            login(request, user)

            return HttpResponseRedirect(reverse('desk:index'))
    return render(request, 'desk/change_pass.html', {'form': form})


@login_required
def account(request):
    user = request.user
    return render(request, 'desk/account.html', {'user': user})
