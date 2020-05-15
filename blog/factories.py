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
        django_get_or_create = ("slug",)


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "blog.Post"
        django_get_or_create = ("slug",)

    author = factory.SubFactory(UserFactory)
    title = factory.Faker("sentence", nb_words=4)
    pompadour = factory.Faker("sentence")
    text = factory.Faker("text")
    slug = factory.LazyAttribute(lambda obj: obj.title.replace(" ", "-").replace(".", ""))
    published_date = factory.Faker("date_time", tzinfo=timezone.get_current_timezone())
