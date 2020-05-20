import factory.fuzzy

from ..constants import ObjectTypes, VerzoekStatus


class VerzoekFactory(factory.django.DjangoModelFactory):
    bronorganisatie = factory.Faker("ssn", locale="nl_NL")
    klant = factory.Faker("url")
    tekst = factory.Faker("word")
    status = factory.fuzzy.FuzzyChoice(VerzoekStatus.values)

    class Meta:
        model = "datamodel.Verzoek"


class ObjectVerzoekFactory(factory.django.DjangoModelFactory):
    verzoek = factory.SubFactory(VerzoekFactory)
    object_type = factory.fuzzy.FuzzyChoice(ObjectTypes.values)
    object = factory.Faker("url")

    class Meta:
        model = "datamodel.ObjectVerzoek"


class VerzoekProductFactory(factory.django.DjangoModelFactory):
    verzoek = factory.SubFactory(VerzoekFactory)
    product = factory.Faker("url")

    class Meta:
        model = "datamodel.VerzoekProduct"


class VerzoekContactMomentFactory(factory.django.DjangoModelFactory):
    verzoek = factory.SubFactory(VerzoekFactory)
    contactmoment = factory.Faker("url")

    class Meta:
        model = "datamodel.VerzoekContactMoment"
