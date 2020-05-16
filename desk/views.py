from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from desk.models import Post
from desk.forms import NewPostForm, SignUpForm, SignInForm, CustomPasswordChangeForm, ResetForm
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.views.generic import ListView, FormView, RedirectView
from django.core.mail import send_mail
from free_desk import settings
from django.template import loader
from django.contrib.auth.models import User
import random
import string


class IndexView(ListView):
    paginate_by = 12
    model = Post
    ordering = '-pub_date'


class NewPostView(FormView):
    form_class = NewPostForm
    success_url = reverse_lazy('desk:index')
    template_name = 'desk/new_post.html'

    def form_valid(self, form):
        post = Post(
                    author=self.request.user,
                    subject=form.cleaned_data['subject'],
                    text=form.cleaned_data['text'],
                    pub_date=timezone.now()
                    )

        post.save()
        return super().form_valid(form)


class SignUpView(FormView):
    form_class = SignUpForm
    success_url = reverse_lazy('desk:index')
    template_name = 'desk/sign_up.html'

    def form_valid(self, form):
        context = ({'username': form.cleaned_data.get('username')})
        send_mail(
            'Registration on Free Desk.',
            loader.render_to_string('desk/emails/registrationmail.txt', context),
            settings.EMAIL_HOST_USER,
            [form.cleaned_data['email']],
            html_message=loader.render_to_string('desk/emails/registrationmail.html', context),
            fail_silently=True,
                   )

        form.save()

        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1']
        )

        login(self.request, user)

        return super().form_valid(form)


class SignInView(FormView):
    form_class = SignInForm
    template_name = 'desk/sign_in.html'

    def get_success_url(self):

        if len(self.request.GET['next']) != 0:
            success_url = self.request.GET['next']
        else:
            success_url = reverse_lazy('desk:index')

        return str(success_url)

    def form_valid(self, form):
        # Getting user objects with username__iexact,to avoid case sensitivity.
        # form_username is username printed in form by user.
        # So we can get user object from base with username in a different case
        # then requested by user. i.e alexey same as AlExEy
        try:
            form_username = form.cleaned_data['username']
            user = User.objects.get(username__iexact=form_username)
            user = authenticate(
                username=user.username,
                password=form.cleaned_data['password']
            )
        except User.DoesNotExist:
            user = None

        if not user:
            form.error_message = 'Invalid username or password'

            return render(
                self.request,
                'desk/sign_in.html',
                {'form': form},
                status=403
            )

        login(self.request, user)

        return super().form_valid(form)


def sign_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('desk:index'))


class ChangePassView(FormView):
    template_name = 'desk/change_pass.html'
    success_url = reverse_lazy('desk:index')

    def get_form(self):
        form = CustomPasswordChangeForm(self.request.user, self.request.POST)
        return form

    def form_valid(self, form):
        user = self.request.user
        user.set_password(form.cleaned_data['new_password1'])
        user.save()
        login(self.request, self.request.user)
        return super().form_valid(form)


class AccountView(ListView):
    model = Post
    template_name = 'desk/account.html'
    ordering = '-pub_date'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(author=self.request.user)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['user'] = self.request.user
        return context

    def post(self, request):
        post = get_object_or_404(Post, pk=request.POST['post_id'])
        post.delete()
        return HttpResponseRedirect(reverse('desk:account'))


class ResetView(FormView):
    form_class = ResetForm
    template_name = 'desk/reset.html'
    success_url = reverse_lazy('desk:successfullreset')

    def form_valid(self, form):
        new_pas = "".join(random.sample(string.ascii_letters + string.digits, 8))
        user_email = form.cleaned_data['email']
        user = User.objects.get(email=user_email)
        user.set_password(new_pas)

        context = {'password': new_pas, 'username': user.username}

        send_mail(
            'Password reset on Free Desk.',
            loader.render_to_string('desk/emails/resetmail.txt', context),
            settings.EMAIL_HOST_USER,
            [user.email],
            html_message=loader.render_to_string('desk/emails/resetmail.html', context),
            fail_silently=True,
                   )

        user.save()

        return super().form_valid(form)
