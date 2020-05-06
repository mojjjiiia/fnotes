from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from desk.models import Post
from desk.forms import NewPostForm, SignUpForm, SignInForm, CustomPasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.views.generic import ListView, FormView


class IndexView(ListView):
    paginate_by = 12
    model = Post
    ordering = '-pub_date'

# def index(request):
#    posts = Post.objects.all().order_by('-pub_date')
#    return render(request, 'desk/post_list.html', {'posts': posts})


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

# @login_required
# def new_post(request):
#
#    if request.method == 'POST':
#        form = NewPostForm(request.POST)
#
#        if form.is_valid():
#            post = Post(
#                author=request.user,
#                subject=form.cleaned_data['subject'],
#                text=form.cleaned_data['text'],
#                pub_date=timezone.now())
#            post.save()
#            return HttpResponseRedirect(reverse('desk:index'))
#
#    form = NewPostForm()
#    return render(request, 'desk/new_post.html', {'form': form})


class SignUpView(FormView):
    form_class = SignUpForm
    success_url = reverse_lazy('desk:index')
    template_name = 'desk/sign_up.html'

    def form_valid(self, form):
        form.save()

        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1']
        )

        login(self.request, user)

        return super().form_valid(form)


# def sign_up(request):
#    form = SignUpForm()

#    if request.method == 'POST':
#        form = SignUpForm(request.POST)
#        if form.is_valid():
#            form.save()

#            content = form.cleaned_data
#            user = authenticate(
#                username=content['username'],
#                password=content['password1']
#            )

#            login(request, user)

#            return HttpResponseRedirect(reverse('desk:index'))

#    return (render(request, 'desk/sign_up.html', {'form': form}))


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
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )

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


# def sign_in(request):
#    form = SignInForm()

#    if request.method == 'POST':
#        form = SignInForm(request.POST)
#        if form.is_valid():

#            content = form.cleaned_data
#            user = authenticate(
#                username=content['username'],
#                password=content['password']
#            )

#            if not user:
#                form.error_message = 'Invalid username or password'

#                return render(
#                    request,
#                    'desk/sign_in.html',
#                    {'form': form},
#                    status=403
#                )

#            login(request, user)

#            if len(request.GET['next']) != 0:
#                redirect_path = request.GET['next']
#            else:
#                redirect_path = reverse('desk:index')

#            return HttpResponseRedirect(redirect_path)

#    return render(request, 'desk/sign_in.html', {'form': form})


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


# @login_required
# def change_pass(request):
#    user = request.user
#    form = CustomPasswordChangeForm(user)

#    if request.method == 'POST':
#        form = CustomPasswordChangeForm(user, request.POST)
#        if form.is_valid():
#            content = form.cleaned_data
#            user.set_password(content['new_password1'])
#            user.save()

#            login(request, user)

#            return HttpResponseRedirect(reverse('desk:index'))

#    return render(request, 'desk/change_pass.html', {'form': form})


#class AccountView(DetailView):
#    template_name = 'desk/account.html'
#
#    def get_object(self):
#        return self.request.user

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

#@login_required
#def account(request):
#    user = request.user
#    return render(request, 'desk/account.html', {'user': user})
