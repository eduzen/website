from django.apps import AppConfig
from django.contrib.postgres.search import SearchVector
from django.db import connections
from django.db.models import Model
from django.db.models.signals import post_save


def update_search_vector(sender: type[Model], instance: Model, **kwargs: object) -> None:
    """Keep the PostgreSQL search vector in sync after model saves."""
    using = kwargs.get("using")
    db_alias = using if isinstance(using, str) else "default"
    if connections[db_alias].vendor != "postgresql":
        return

    sender._default_manager.using(db_alias).filter(pk=instance.pk).update(
        search_vector=(
            SearchVector("title", weight="A") + SearchVector("summary", weight="B") + SearchVector("text", weight="C")
        )
    )


class BlogConfig(AppConfig):
    name = "blog"

    def ready(self) -> None:
        post_save.connect(
            update_search_vector,
            sender=self.get_model("Post"),
            dispatch_uid="blog.post.update_search_vector",
            weak=False,
        )
