import factory.fuzzy

from ..constants import IndicatieMachtiging, KlantRol, ObjectTypes, VerzoekStatus


class VerzoekFactory(factory.django.DjangoModelFactory):
    bronorganisatie = factory.Faker("ssn", locale="nl_NL")
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


class VerzoekInformatieObjectFactory(factory.django.DjangoModelFactory):
    verzoek = factory.SubFactory(VerzoekFactory)
    informatieobject = factory.Faker("url")

    class Meta:
        model = "datamodel.VerzoekInformatieObject"


class KlantVerzoekFactory(factory.django.DjangoModelFactory):
    verzoek = factory.SubFactory(VerzoekFactory)
    klant = factory.Faker("url")
    rol = factory.fuzzy.FuzzyChoice(KlantRol.values)
    indicatie_machtiging = factory.fuzzy.FuzzyChoice(IndicatieMachtiging.values)

    class Meta:
        model = "datamodel.KlantVerzoek"
