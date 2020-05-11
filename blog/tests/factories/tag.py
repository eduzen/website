import factory


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "blog.Tag"
        django_get_or_create = ("slug",)
