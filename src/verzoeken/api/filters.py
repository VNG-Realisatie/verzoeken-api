from django_filters import filters
from vng_api_common.filtersets import FilterSet
from vng_api_common.utils import get_help_text

from verzoeken.datamodel.models import (
    ObjectVerzoek,
    VerzoekContactMoment,
    VerzoekInformatieObject,
    VerzoekProduct,
)


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
