from django.utils.translation import ugettext_lazy as _

from django_filters import filters
from vng_api_common.filters import URLModelChoiceFilter
from vng_api_common.filtersets import FilterSet
from vng_api_common.utils import get_help_text

from verzoeken.datamodel.models import (
    KlantVerzoek,
    ObjectVerzoek,
    Verzoek,
    VerzoekContactMoment,
    VerzoekInformatieObject,
    VerzoekProduct,
)


class VerzoekFilter(FilterSet):
    class Meta:
        model = Verzoek
        fields = {
            "identificatie": ["exact"],
            "bronorganisatie": ["exact"],
            "externe_identificatie": ["exact"],
            "registratiedatum": ["exact", "gt", "gte", "lt", "lte"],
            "voorkeurskanaal": ["exact"],
            "tekst": ["exact"],
            "status": ["exact"],
            "in_te_trekken_verzoek": ["exact"],
            "intrekkende_verzoek": ["exact"],
            "aangevulde_verzoek": ["exact"],
            "aanvullende_verzoek": ["exact"],
        }

    @classmethod
    def filter_for_field(cls, f, name, lookup_expr):
        # Needed because `intrekkende_verzoek` and `aanvullende_verzoek`
        # are reverse OneToOne relations
        if f.name == "intrekkende_verzoek":
            filter = URLModelChoiceFilter()
            filter.field_name = "intrekkende_verzoek"
            filter.extra["help_text"] = _(
                "URL-referentie naar het (latere) VERZOEK waarin verzocht wordt "
                "dit VERZOEK in te trekken. Dit veld is alleen leesbaar en wordt "
                "automatisch gezet wanneer er een ander VERZOEK wordt aangemaakt "
                "dat dit VERZOEK intrekt."
            )
            filter.queryset = Verzoek.objects.all()
        elif f.name == "aanvullende_verzoek":
            filter = URLModelChoiceFilter()
            filter.field_name = "aanvullende_verzoek"
            filter.extra["help_text"] = _(
                "URL-referentie naar het (latere) VERZOEK waarin dit VERZOEK "
                "wordt aangevuld. Dit veld is alleen leesbaar en wordt automatisch "
                "gezet indien een ander VERZOEK wordt aangemaakt dat dit VERZOEK aanvult."
            )
            filter.queryset = Verzoek.objects.all()
        else:
            filter = super().filter_for_field(f, name, lookup_expr)
        return filter


class ObjectVerzoekFilter(FilterSet):
    class Meta:
        model = ObjectVerzoek
        fields = ("object", "verzoek")


class VerzoekInformatieObjectFilter(FilterSet):
    class Meta:
        model = VerzoekInformatieObject
        fields = ("verzoek", "informatieobject")


class VerzoekContactMomentFilter(FilterSet):
    class Meta:
        model = VerzoekContactMoment
        fields = ("verzoek", "contactmoment")


class VerzoekProductFilter(FilterSet):
    product_identificatie__code = filters.CharFilter(
        field_name="product_code",
        help_text=get_help_text("datamodel.VerzoekProduct", "product_code"),
    )

    class Meta:
        model = VerzoekProduct
        fields = ("verzoek", "product", "product_identificatie__code")


class KlantVerzoekFilter(FilterSet):
    class Meta:
        model = KlantVerzoek
        fields = ("verzoek", "klant")
