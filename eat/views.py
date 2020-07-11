from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy

from django.db.models import Q

from eat.models import Recipe
from eat.forms import RecipeForm




#アクセス制限（レシピを作成した人のみアクセス可能にする（詳細、上書き、消去ページ）　URLでの直接アクセス防止
class OnlyUserRequiredMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):

        user = self.request.user
        obj = get_object_or_404(Recipe, id=self.kwargs['pk'])
        return user.id == obj.user.id or user.is_superuser

#レシピのリスト
class EatListView(LoginRequiredMixin, ListView):
    model = Recipe
    paginate_by = 5
    login_url = "/signup/login/"

#レシピの検索および並び替え
    def get_queryset(self):
        search = self.request.GET.get("search")
        order = self.request.GET.get("order")

        if self.request.user.is_authenticated:
            object_filter = Recipe.objects.filter(user=self.request.user)

            if search:
                object_filter = Recipe.objects.filter(
                    Q(user=self.request.user),
                    Q(recipe_name__contains=search)|
                    Q(ingredient__contains=search)|
                    Q(type__contains=search)
                    )
                if order == "new":
                    object_list = object_filter.order_by("-date")

                elif order == "old":
                    object_list = object_filter
                else:
                    object_list = object_filter.order_by("-date")
            elif order == "old":
                object_list = object_filter

            else:
                object_list = object_filter.order_by("-date")
            return object_list
        return reverse_lazy("signup:login")

#レシピの数のコンテキストの受け渡し
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe_count = Recipe.objects.filter(user=self.request.user).count()
        context["recipe_count"] = recipe_count
        return context

#選択消去機能
    def post(self, request):
        deletes = request.GET.get("deletes")

        if deletes == "deletes":
            recipe_pks = request.POST.getlist('delete')
            Recipe.objects.filter(pk__in=recipe_pks).delete()
        return redirect('eat:index')


class EatDetailView(LoginRequiredMixin, OnlyUserRequiredMixin, DetailView):
    model = Recipe
    login_url = "/signup/login/"


class EatCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "eat/recipe_create_form.html"
    success_url = reverse_lazy("eat:index")
    login_url = "/signup/login/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "保存しました")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "保存に失敗しました")
        return super().form_invalid(form)


class EatUpdateView(LoginRequiredMixin, OnlyUserRequiredMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "eat/recipe_update_form.html"
    login_url = "/signup/login/"

    def get_success_url(self):
        url = reverse_lazy("eat:detail", kwargs={"pk":self.kwargs["pk"]})
        return url

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "投稿を上書きしました")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "保存に失敗しました")
        return super().form_invalid(form)


class EatDeleteView(LoginRequiredMixin, OnlyUserRequiredMixin, DeleteView):
    model = Recipe
    template_name = "eat/recipe_delete.html"
    success_url = reverse_lazy("eat:index")
    login_url = "/signup/login/"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "消去しました")
        return super().delete(request, *args, **kwargs)
