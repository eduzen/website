from django.http import HttpRequest
from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Snippet
from .serializers import SnippetSerializer


class SnippetModelViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()  # type: ignore
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request: HttpRequest, *args: int, **kwargs: str) -> Response:
        snippet = self.get_object()
        return Response(snippet.highlighted)
