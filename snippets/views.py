from rest_framework import viewsets
from rest_framework import permissions, renderers
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Snippet
from .serializers import SnippetSerializer


class SnippetModelViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)
