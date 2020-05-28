from django.utils.translation import ugettext_lazy as _

from djchoices import ChoiceItem, DjangoChoices


class ObjectTypes(DjangoChoices):
    zaak = ChoiceItem("zaak", _("Zaak"))


class VerzoekStatus(DjangoChoices):
    ontvangen = ChoiceItem(
        "ontvangen",
        _("Ontvangen"),
        description=_("Het verzoek is ingediend en door de organisatie ontvangen."),
    )
    in_behandeling = ChoiceItem(
        "in_behandeling",
        _("In behandeling"),
        description=_("Het is verzoek is in behandeling."),
    )
    afgehandeld = ChoiceItem(
        "afgehandeld",
        _("Afgehandeld"),
        description=_(
            "Het verzoek zelf is afgehandeld. Eventuele vervolg acties, zoals "
            "zaken die voortkomen uit het verzoek, hebben een eigen status."
        ),
    )
    afgewezen = ChoiceItem(
        "afgewezen",
        _("Afgewezen"),
        description=_("Het verzoek is afgewezen zonder vervolg acties."),
    )
    ingetrokken = ChoiceItem(
        "ingetrokken",
        _("Ingetrokken"),
        description=_("De indiener heeft het verzoek ingetrokken."),
    )
