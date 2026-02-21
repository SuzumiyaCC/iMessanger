from django.views.generic import ListView
from .models import Post


class PostListView(ListView):
    template_name = "news.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        qs = Post.objects.filter(is_published=True)
        q = (self.request.GET.get("q") or "").strip()
        author = (self.request.GET.get("author") or "").strip()

        if q:
            qs = qs.filter(title__icontains=q)
        if author:
            qs = qs.filter(author__icontains=author)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = (self.request.GET.get("q") or "").strip()
        ctx["author"] = (self.request.GET.get("author") or "").strip()
        return ctx
