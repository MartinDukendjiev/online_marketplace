from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView
from django.shortcuts import get_object_or_404, redirect, render
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from online_marketplace.accounts.forms import RegisterUserForm, CommentForm
from online_marketplace.accounts.models import Comment

UserModel = get_user_model()


class UserRegisterView(CreateView):
    form_class = RegisterUserForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)
        return result

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', '')
        return context

    def get_success_url(self):
        return self.request.POST.get('next', self.success_url)


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'


class UserLogoutView(LoginRequiredMixin, LogoutView):
    pass


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserModel
    template_name = 'accounts/profile.html'
    context_object_name = 'profile'

    profile_image = static('images/person.png')

    def get_profile_image(self):
        if self.object.profile_picture is not None:
            return self.object.profile_picture
        return self.profile_image

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        comments = Comment.objects.filter(seller_profile=profile)
        context['comments'] = comments
        context['comment_form'] = CommentForm()
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = UserModel
    template_name = 'accounts/profile-edit-page.html'
    fields = ['first_name', 'last_name', 'email']


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = UserModel
    template_name = 'accounts/profile-delete-page.html'
    success_url = reverse_lazy('index')


def add_comment(request, pk):
    profile = get_object_or_404(UserModel, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.seller_profile = profile
            comment.save()
            messages.success(request, 'Your comment has been added.')
            return redirect('profile details', pk=pk)

    else:
        form = CommentForm()

    return render(request, 'accounts/profile.html', {'profile': profile, 'comment_form': form})