import factory
from django.utils import timezone


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "auth.User"
        django_get_or_create = ("username",)

    username = "eduzen"
    first_name = "Eduardo"
    last_name = "Enriquez"
    password = factory.PostGenerationMethodCall("set_password", "eduzen!")


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "blog.Tag"
        django_get_or_create = ("word",)

    word = factory.Faker("word")
    slug = factory.LazyAttribute(lambda obj: obj.word.replace(" ", "-").replace(".", "")[:50])


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "blog.Post"
        django_get_or_create = ("slug",)

    author = factory.SubFactory(UserFactory)
    title = factory.Faker("sentence", nb_words=7)
    pompadour = factory.Faker("sentence")
    text = factory.Faker("paragraph", nb_sentences=50)
    slug = factory.LazyAttribute(lambda obj: obj.title.replace(" ", "-").replace(".", "")[:50])
    published_date = factory.Faker("date_time", tzinfo=timezone.get_current_timezone())

    @factory.post_generation
    def tags(self, create, tags, **kwargs):
        if not create:
            return

        if not tags:
            return
        for tag in tags:
            self.tags.add(tag)
