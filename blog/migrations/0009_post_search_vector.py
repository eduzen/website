# Generated manually — adds SearchVectorField + GIN index for fast full-text search.
# Both the GIN index creation and the back-fill are PostgreSQL-only and are
# skipped silently on SQLite (used in the test suite).

from django.apps.registry import Apps
from django.contrib.postgres.search import SearchVector, SearchVectorField
from django.db import migrations
from django.db.backends.base.schema import BaseDatabaseSchemaEditor


def add_gin_index(apps: Apps, schema_editor: BaseDatabaseSchemaEditor) -> None:
    """Create the GIN index only on PostgreSQL — SQLite has no such index type."""
    if schema_editor.connection.vendor != "postgresql":
        return
    schema_editor.execute("CREATE INDEX IF NOT EXISTS post_search_vector_gin_idx ON blog_post USING gin(search_vector)")


def drop_gin_index(apps: Apps, schema_editor: BaseDatabaseSchemaEditor) -> None:
    if schema_editor.connection.vendor != "postgresql":
        return
    schema_editor.execute("DROP INDEX IF EXISTS post_search_vector_gin_idx")


def populate_search_vector(apps: Apps, schema_editor: BaseDatabaseSchemaEditor) -> None:
    """Back-fill search_vector for all existing posts in a single UPDATE.

    Skipped on non-PostgreSQL backends (e.g. SQLite in the test suite) because
    ``to_tsvector`` is a PostgreSQL-only function.
    """
    if schema_editor.connection.vendor != "postgresql":
        return

    Post = apps.get_model("blog", "Post")
    Post.objects.update(
        search_vector=(
            SearchVector("title", weight="A") + SearchVector("summary", weight="B") + SearchVector("text", weight="C")
        )
    )


def noop(apps: Apps, schema_editor: BaseDatabaseSchemaEditor) -> None:
    del apps, schema_editor


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0008_post_post_published_date_idx_and_more"),
    ]

    operations = [
        # 1. Add the nullable column — works on every backend.
        migrations.AddField(
            model_name="post",
            name="search_vector",
            field=SearchVectorField(blank=True, null=True),
        ),
        # 2. Create GIN index — PostgreSQL only; skipped on SQLite.
        migrations.RunPython(add_gin_index, reverse_code=drop_gin_index),
        # 3. Back-fill existing rows — PostgreSQL only; skipped on SQLite.
        migrations.RunPython(populate_search_vector, reverse_code=noop),
    ]
