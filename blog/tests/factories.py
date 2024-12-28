import factory
from django.utils import timezone
from django.utils.text import slugify


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "auth.User"
        django_get_or_create = ("username",)

    username = factory.Sequence(lambda n: f"eduzen{n}")
    first_name = factory.Faker("first_name")
    first_name = factory.Faker("first_name")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@eduzen.ar")
    password = factory.django.Password("pw")


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "blog.Tag"
        django_get_or_create = ("word",)
        skip_postgeneration_save = True

    word = factory.Faker("word")
    slug = factory.LazyAttribute(lambda obj: slugify(obj.word))


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "blog.Post"
        django_get_or_create = ("slug",)
        skip_postgeneration_save = True

    author = factory.SubFactory(UserFactory)
    title = factory.Faker("sentence", nb_words=4)
    summary = factory.Faker("sentence")
    text = factory.Faker("paragraph", nb_sentences=50)
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))
    published_date = factory.LazyFunction(timezone.now)

    @factory.post_generation
    def tags(self, create, tags, **kwargs):
        if not create:
            return

        if not tags:
            return
        for tag in tags:
            self.tags.add(tag)
