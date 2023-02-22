import factory
from django.contrib.auth.models import User
from django.utils import timezone
from faker import Faker

from blog.models import Post, Tag

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "password")


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    word = factory.Sequence(lambda n: f"tag{n}")


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    author = factory.SubFactory(UserFactory)
    title = fake.sentence()
    pompadour = fake.text(max_nb_chars=800)
    slug = factory.Sequence(lambda n: f"post-{n}")
    created_date = factory.LazyFunction(timezone.now)
    published_date = factory.LazyFunction(lambda: fake.date_between(start_date="-1y", end_date="today"))
    text = fake.text()

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for tag in extracted:
                self.tags.add(tag)
        else:
            self.tags.add(TagFactory())

    @factory.post_generation
    def images(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for image in extracted:
                self.images.add(image)
