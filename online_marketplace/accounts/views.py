from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView, PasswordChangeDoneView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from online_marketplace.accounts.forms import RegisterUserForm, CommentForm, RatingForm, LoginUserForm
from online_marketplace.accounts.models import Comment, Rating
from online_marketplace.products.models import Product

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        user_comments = Comment.objects.filter(seller_profile=profile, user=self.request.user)
        user_rating = Rating.objects.filter(receiver=profile, reviewer=self.request.user).first()
        all_comments = Comment.objects.filter(seller_profile=profile)

        context['user_products'] = Product.objects.filter(user=profile)
        context['comment_form'] = CommentForm()
        context['user_comments'] = user_comments

        if user_rating:
            context['user_has_rated'] = True
        else:
            context['rating_form'] = RatingForm()
            context['user_has_rated'] = False

        context['comments'] = all_comments
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_rating = Rating.objects.filter(receiver=self.object, reviewer=request.user).first()

        if 'delete_comment' in request.POST:
            comment_id = request.POST.get('comment_id')
            comment = Comment.objects.filter(pk=comment_id, user=request.user).first()
            if comment:
                comment.delete()
                messages.success(request, 'Your comment has been deleted.')
                return self.render_to_response(self.get_context_data())

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.seller_profile = self.object
            comment.save()
            messages.success(request, 'Your comment has been added.')

        if not user_rating:
            rating_form = RatingForm(request.POST)
            if rating_form.is_valid():
                rating = rating_form.save(commit=False)
                rating.reviewer = request.user
                rating.receiver = self.object
                rating.save()
                messages.success(request, 'Your rating has been added.')

        return self.render_to_response(self.get_context_data())


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = UserModel
    template_name = 'accounts/profile-edit-page.html'
    fields = ['first_name', 'last_name', 'email']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_object()
        return context

    def get_success_url(self):
        return reverse('profile details', kwargs={'pk': self.object.pk})


class ProfilePasswordChangeView(PasswordChangeView):
    template_name = 'accounts/change_password.html'
    success_url = 'change-password/done/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user
        return context


class ProfilePasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = UserModel
    template_name = 'accounts/profile-delete-page.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_object()
        return context

    def get_success_url(self):
        return reverse('login user')


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


def add_rating(request, pk):
    profile = get_object_or_404(UserModel, pk=pk)

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.reviewer = request.user
            rating.receiver = profile
            rating.save()
            messages.success(request, 'Your rating has been added.')
            return redirect('profile details', pk=pk)

    else:
        form = RatingForm()

    return render(request, 'accounts/profile.html', {'profile': profile, 'rating_form': form})
