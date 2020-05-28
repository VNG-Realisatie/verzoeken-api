import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from vng_api_common.fields import RSINField
from vng_api_common.models import APIMixin
from vng_api_common.utils import (
    generate_unique_identification,
    request_object_attribute,
)
from vng_api_common.validators import alphanumeric_excluding_diacritic

from .constants import IndicatieMachtiging, KlantRol, ObjectTypes, VerzoekStatus


class Verzoek(APIMixin, models.Model):
    """
    Verzoek is een speciaal contactmoment.
    """

    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4, help_text="Unieke resource identifier (UUID4)"
    )
    bronorganisatie = RSINField(
        help_text="Het RSIN van de Niet-natuurlijk persoon zijnde de "
        "organisatie die de klantinteractie heeft gecreeerd. Dit moet een "
        "geldig RSIN zijn van 9 nummers en voldoen aan "
        "https://nl.wikipedia.org/wiki/Burgerservicenummer#11-proef"
    )
    registratiedatum = models.DateTimeField(
        default=timezone.now,
        help_text=_("De datum en het tijdstip waarop het VERZOEK is geregistreerd."),
    )
    tekst = models.TextField(
        blank=True,
        help_text=_(
            "Een toelichting die inhoudelijk het VERZOEK van de KLANT beschrijft."
        ),
    )
    voorkeurskanaal = models.CharField(
        max_length=50,
        blank=True,
        help_text=_(
            "Het communicatiekanaal dat voor opvolging van het VERZOEK de voorkeur heeft van de KLANT."
        ),
    )
    identificatie = models.CharField(
        max_length=40,
        blank=True,
        help_text="De unieke identificatie van het VERZOEK binnen de "
        "organisatie die verantwoordelijk is voor de behandeling van "
        "het VERZOEK.",
        validators=[alphanumeric_excluding_diacritic],
    )
    externe_identificatie = models.CharField(
        max_length=40,
        blank=True,
        help_text="De identificatie van het VERZOEK buiten de eigen organisatie.",
        validators=[alphanumeric_excluding_diacritic],
    )
    status = models.CharField(
        max_length=20,
        choices=VerzoekStatus,
        help_text="De waarden van de typering van de voortgang van afhandeling van een VERZOEK.",
    )
    in_te_trekken_verzoek = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="intrekkende_verzoek",
        help_text="URL-referentie naar het (eerdere) VERZOEK dat door dit VERZOEK wordt verzocht ingetrokken te worden.",
    )
    aangevulde_verzoek = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="aanvullende_verzoek",
        help_text="URL-referentie naar het (eerdere) VERZOEK dat door dit VERZOEK wordt aangevuld.",
    )

    class Meta:
        unique_together = ("bronorganisatie", "identificatie")
        verbose_name = "verzoek"
        verbose_name_plural = "verzoeken"

    def save(self, *args, **kwargs):
        if not self.identificatie:
            self.identificatie = generate_unique_identification(
                self, "registratiedatum"
            )

        super().save(*args, **kwargs)

    def unique_representation(self):
        return f"{self.bronorganisatie} - {self.identificatie}"


class ObjectVerzoek(APIMixin, models.Model):
    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4, help_text="Unieke resource identifier (UUID4)"
    )
    object = models.URLField(
        max_length=1000,
        help_text="URL-referentie naar het gerelateerde OBJECT (in een andere API).",
    )
    object_type = models.CharField(
        "objecttype",
        max_length=100,
        choices=ObjectTypes.choices,
        help_text="Het type van het gerelateerde OBJECT.",
    )
    verzoek = models.ForeignKey(
        "datamodel.Verzoek",
        on_delete=models.CASCADE,
        help_text="URL-referentie naar het VERZOEK.",
    )

    class Meta:
        verbose_name = "object-verzoek"
        verbose_name_plural = "object-verzoeken"
        unique_together = ("verzoek", "object")


class VerzoekProduct(APIMixin, models.Model):
    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4, help_text="Unieke resource identifier (UUID4)"
    )
    verzoek = models.ForeignKey(
        "datamodel.Verzoek",
        on_delete=models.CASCADE,
        help_text="URL-referentie naar het VERZOEK.",
    )
    product = models.URLField(
        blank=True,
        max_length=1000,
        help_text="URL-referentie naar het PRODUCT (in de Producten en Diensten API).",
    )
    product_code = models.CharField(
        max_length=20, blank=True, help_text="De unieke code van het PRODUCT."
    )

    def clean(self):
        if not self.product and not self.product_code:
            raise ValidationError(
                _("product or productIdentificatie must be provided"),
                code="invalid-product",
            )

    def unique_representation(self):
        product_id = (
            self.product.rstrip("/").split("/")[-1]
            if self.product
            else self.product_code
        )
        return f"({self.verzoek.unique_representation()}) - {product_id}"


class VerzoekInformatieObject(models.Model):
    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4, help_text="Unieke resource identifier (UUID4)"
    )
    verzoek = models.ForeignKey(
        "datamodel.Verzoek",
        on_delete=models.CASCADE,
        help_text="URL-referentie naar het VERZOEK.",
    )
    informatieobject = models.URLField(
        "informatieobject",
        help_text="URL-referentie naar het INFORMATIEOBJECT (in de Documenten "
        "API) waarin (een deel van) het verzoek beschreven is of "
        "aanvullende informatie biedt bij het VERZOEK.",
        max_length=1000,
    )

    class Meta:
        verbose_name = "verzoekinformatieobject"
        verbose_name_plural = "verzoekinformatieobjecten"
        unique_together = (("verzoek", "informatieobject"),)

    def __str__(self):
        return str(self.uuid)

    def unique_representation(self):
        if not hasattr(self, "_unique_representation"):
            io_id = request_object_attribute(
                self.informatieobject, "identificatie", "enkelvoudiginformatieobject"
            )
            self._unique_representation = (
                f"({self.verzoek.unique_representation()}) - {io_id}"
            )
        return self._unique_representation


class VerzoekContactMoment(models.Model):
    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4, help_text="Unieke resource identifier (UUID4)"
    )
    verzoek = models.ForeignKey(
        "datamodel.Verzoek",
        on_delete=models.CASCADE,
        help_text="URL-referentie naar het VERZOEK.",
    )
    contactmoment = models.URLField(
        max_length=1000,
        help_text=_("URL-referentie naar een CONTACTMOMENT (in Contactmoment API)"),
    )

    class Meta:
        verbose_name = "verzoekcontactmoment"
        verbose_name_plural = "verzoekcontactmomenten"
        unique_together = ("verzoek", "contactmoment")

    def __str__(self):
        return str(self.uuid)

    def unique_representation(self):
        contactmoment_id = self.contactmoment.rstrip("/").split("/")[-1]
        return f"({self.verzoek.unique_representation()}) - {contactmoment_id}"


class KlantVerzoek(models.Model):
    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4, help_text="Unieke resource identifier (UUID4)"
    )
    verzoek = models.ForeignKey(
        "datamodel.Verzoek",
        on_delete=models.CASCADE,
        help_text="URL-referentie naar het VERZOEK.",
    )
    klant = models.URLField(
        max_length=1000, help_text=_("URL-referentie naar een KLANT (in Klanten API)"),
    )
    rol = models.CharField(
        max_length=100,
        blank=True,
        choices=KlantRol.choices,
        help_text="Rol van de KLANT bij het VERZOEK.",
    )
    indicatie_machtiging = models.CharField(
        max_length=100,
        blank=True,
        choices=IndicatieMachtiging.choices,
        help_text="Indicatie machtiging",
    )

    class Meta:
        verbose_name = "klantverzoek"
        verbose_name_plural = "klantverzoeken"
        unique_together = ("verzoek", "klant")

    def unique_representation(self):
        klant_id = self.klant.rstrip("/").split("/")[-1]
        return f"({self.verzoek.unique_representation()}) - {klant_id}"
