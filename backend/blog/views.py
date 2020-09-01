from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from blog.models import BlogPost
from blog.serializers import BlogPostShortSerializer, BlogPostLongSerializer


class BlogPostViewSet(ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostLongSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'list':
            return BlogPostShortSerializer
        return self.serializer_class


