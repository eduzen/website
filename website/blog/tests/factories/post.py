import factory

from blog.models import Post


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "auth.User"

    username = "eduzen"
    password = "eduzen"

    first_name = "Eduardo"
    last_name = "Enriquez"


class PostFactory(factory.Factory):
    class Meta:
        model = Post

    author = factory.SubFactory(UserFactory)
    title = factory.Faker('sentence', nb_words=4)
    pompadour = factory.Faker("sentence")
    text = factory.Faker("text")
