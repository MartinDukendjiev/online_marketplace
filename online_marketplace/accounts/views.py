from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView, PasswordChangeDoneView
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from online_marketplace.accounts.forms import RegisterUserForm, CommentForm, RatingForm
from online_marketplace.accounts.models import Comment, Rating
from online_marketplace.products.models import Product

UserModel = get_user_model()


class UserMatchMixin:
    def check_user_match(self, user_object):
        if self.request.user != user_object:
            raise Http404("You are not allowed to perform this action.")


class OnlyAnonymousMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')

        return super().dispatch(request, *args, **kwargs)


class UserRegisterView(OnlyAnonymousMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)
        return result

    def form_invalid(self, form):
        return super().form_invalid(form)


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        next_url = self.request.POST.get('next', None)
        if next_url:
            return next_url
        return reverse_lazy('index')


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

        if 'delete_comment' in request.POST:
            self.delete_comment(request)

        self.handle_comment(request)
        self.handle_rating(request)

        return self.render_to_response(self.get_context_data())

    def delete_comment(self, request):
        comment_id = request.POST.get('comment_id')
        comment = Comment.objects.filter(pk=comment_id, user=request.user).first()
        if comment:
            comment.delete()
            messages.success(request, 'Your comment has been deleted.')

    def handle_comment(self, request):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.seller_profile = self.object
            comment.save()
            messages.success(request, 'Your comment has been added.')

    def handle_rating(self, request):
        user_rating = Rating.objects.filter(receiver=self.object, reviewer=request.user).first()
        if not user_rating:
            rating_form = RatingForm(request.POST)
            if rating_form.is_valid():
                rating = rating_form.save(commit=False)
                rating.reviewer = request.user
                rating.receiver = self.object
                rating.save()
                messages.success(request, 'Your rating has been added.')


class ProfileEditView(LoginRequiredMixin, UserMatchMixin, UpdateView):
    model = UserModel
    template_name = 'accounts/profile-edit-page.html'
    fields = ['first_name', 'last_name', 'email', 'avatar']

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        self.check_user_match(obj)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object
        return context

    def get_success_url(self):
        return reverse('profile details', kwargs={'pk': self.object.pk})


class ProfilePasswordChangeView(LoginRequiredMixin, UserMatchMixin, PasswordChangeView):
    template_name = 'accounts/change_password.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        self.check_user_match(obj)
        return obj

    def get_success_url(self):
        return reverse_lazy('password change done', kwargs={'pk': self.request.user.pk})


class ProfilePasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'


class ProfileDeleteView(LoginRequiredMixin, UserMatchMixin, DeleteView):
    model = UserModel
    template_name = 'accounts/profile-delete-page.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_object()
        return context

    def get_success_url(self):
        return reverse('login user')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        self.check_user_match(obj)
        return obj
