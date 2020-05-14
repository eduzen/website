import factory

from blog.models import Post


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "auth.User"
        django_get_or_create = ("username",)

    username = "eduzen"
    first_name = "Eduardo"
    last_name = "Enriquez"
    password = factory.PostGenerationMethodCall("set_password", "eduzen!")


class PostFactory(factory.Factory):
    class Meta:
        model = Post

    author = factory.SubFactory(UserFactory)
    title = factory.Faker("sentence", nb_words=4)
    pompadour = factory.Faker("sentence")
    text = factory.Faker("text")
    slug = factory.LazyAttribute(lambda obj: obj.title.replace(" ", "-"))
