from rest_framework import viewsets
from .models import Post
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        q = (self.request.query_params.get("q") or "").strip()
        author = (self.request.query_params.get("author") or "").strip()
        is_published = (self.request.query_params.get("is_published") or "").strip().lower()

        if q:
            qs = qs.filter(title__icontains=q)
        if author:
            qs = qs.filter(author__icontains=author)
        if is_published in {"true", "false"}:
            qs = qs.filter(is_published=(is_published == "true"))
        return qs
