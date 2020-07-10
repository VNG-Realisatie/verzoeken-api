import logging

from django.core.cache import caches

from rest_framework import mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.serializers import ValidationError
from rest_framework.settings import api_settings
from vng_api_common.audittrails.viewsets import (
    AuditTrailCreateMixin,
    AuditTrailDestroyMixin,
    AuditTrailViewSet,
    AuditTrailViewsetMixin,
)
from vng_api_common.notifications.viewsets import (
    NotificationCreateMixin,
    NotificationDestroyMixin,
    NotificationViewSetMixin,
)
from vng_api_common.permissions import AuthScopesRequired
from vng_api_common.viewsets import CheckQueryParamsMixin

from verzoeken.datamodel.models import (
    KlantVerzoek,
    ObjectVerzoek,
    Verzoek,
    VerzoekContactMoment,
    VerzoekInformatieObject,
    VerzoekProduct,
)

from .audits import AUDIT_VERZOEKEN
from .filters import (
    KlantVerzoekFilter,
    ObjectVerzoekFilter,
    VerzoekContactMomentFilter,
    VerzoekInformatieObjectFilter,
    VerzoekProductFilter,
)
from .kanalen import KANAAL_VERZOEKEN
from .scopes import (
    SCOPE_VERZOEKEN_AANMAKEN,
    SCOPE_VERZOEKEN_ALLES_LEZEN,
    SCOPE_VERZOEKEN_ALLES_VERWIJDEREN,
    SCOPE_VERZOEKEN_BIJWERKEN,
)
from .serializers import (
    KlantVerzoekSerializer,
    ObjectVerzoekSerializer,
    VerzoekContactMomentSerializer,
    VerzoekInformatieObjectSerializer,
    VerzoekProductSerializer,
    VerzoekSerializer,
)
from .validators import ObjectVerzoekDestroyValidator

logger = logging.getLogger(__name__)


class VerzoekViewSet(
    NotificationViewSetMixin, AuditTrailViewsetMixin, viewsets.ModelViewSet
):
    """
    Opvragen en bewerken van VERZOEKen.

    create:
    Maak een VERZOEK aan.

    Maak een VERZOEK aan.

    list:
    Alle VERZOEKen opvragen.

    Alle VERZOEKen opvragen.

    retrieve:
    Een specifiek VERZOEK opvragen.

    Een specifiek VERZOEK opvragen.

    update:
    Werk een VERZOEK in zijn geheel bij.

    Werk een VERZOEK in zijn geheel bij.

    partial_update:
    Werk een VERZOEK deels bij.

    Werk een VERZOEK deels bij.

    destroy:
    Verwijder een VERZOEK.

    Verwijder een VERZOEK.
    """

    queryset = Verzoek.objects.all()
    serializer_class = VerzoekSerializer
    lookup_field = "uuid"
    permission_classes = (AuthScopesRequired,)
    pagination_class = PageNumberPagination
    required_scopes = {
        "list": SCOPE_VERZOEKEN_ALLES_LEZEN,
        "retrieve": SCOPE_VERZOEKEN_ALLES_LEZEN,
        "create": SCOPE_VERZOEKEN_AANMAKEN,
        "update": SCOPE_VERZOEKEN_BIJWERKEN,
        "partial_update": SCOPE_VERZOEKEN_BIJWERKEN,
        "destroy": SCOPE_VERZOEKEN_ALLES_VERWIJDEREN,
    }
    notifications_kanaal = KANAAL_VERZOEKEN
    audit = AUDIT_VERZOEKEN


class ObjectVerzoekViewSet(
    CheckQueryParamsMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.ReadOnlyModelViewSet,
):
    """
    Opvragen en verwijderen van OBJECT-VERZOEK relaties.

    Het betreft een relatie tussen een willekeurig OBJECT, bijvoorbeeld een
    ZAAK in de Zaken API, en een VERZOEK.

    create:
    Maak een OBJECT-VERZOEK relatie aan.

    Maak een OBJECT-VERZOEK relatie aan.

    **LET OP: Dit endpoint hoor je als consumer niet zelf aan te spreken.**

    Andere API's, zoals de Zaken API, gebruiken dit
    endpoint bij het synchroniseren van relaties.

    list:
    Alle OBJECT-VERZOEK relaties opvragen.

    Alle OBJECT-VERZOEK relaties opvragen.

    retrieve:
    Een specifiek OBJECT-VERZOEK relatie opvragen.

    Een specifiek OBJECT-VERZOEK relatie opvragen.

    destroy:
    Verwijder een OBJECT-VERZOEK relatie.

    Verwijder een OBJECT-VERZOEK relatie.

    **LET OP: Dit endpoint hoor je als consumer niet zelf aan te spreken.**

    Andere API's, zoals de Zaken API, gebruiken dit
    endpoint bij het synchroniseren van relaties.
    """

    queryset = ObjectVerzoek.objects.all()
    serializer_class = ObjectVerzoekSerializer
    filterset_class = ObjectVerzoekFilter
    lookup_field = "uuid"
    permission_classes = (AuthScopesRequired,)
    pagination_class = PageNumberPagination
    required_scopes = {
        "list": SCOPE_VERZOEKEN_ALLES_LEZEN,
        "retrieve": SCOPE_VERZOEKEN_ALLES_LEZEN,
        "create": SCOPE_VERZOEKEN_AANMAKEN,
        "destroy": SCOPE_VERZOEKEN_ALLES_VERWIJDEREN,
    }

    def perform_destroy(self, instance):
        # destroy is only allowed if the remote relation does no longer exist, so check for that
        validator = ObjectVerzoekDestroyValidator()

        try:
            validator(instance)
        except ValidationError as exc:
            raise ValidationError(
                {api_settings.NON_FIELD_ERRORS_KEY: exc}, code=exc.detail[0].code
            )
        else:
            super().perform_destroy(instance)


class VerzoekInformatieObjectViewSet(
    NotificationCreateMixin,
    NotificationDestroyMixin,
    AuditTrailCreateMixin,
    AuditTrailDestroyMixin,
    CheckQueryParamsMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.ReadOnlyModelViewSet,
):
    """
    Opvragen en bewerken van VERZOEK-INFORMATIEOBJECT relaties.

    create:
    Maak een VERZOEK-INFORMATIEOBJECT relatie aan.

    Registreer een INFORMATIEOBJECT bij een VERZOEK. Er worden twee types van
    relaties met andere objecten gerealiseerd:

    **Er wordt gevalideerd op**
    - geldigheid `verzoek` URL
    - geldigheid `informatieobject` URL
    - de combinatie `informatieobject` en `verzoek` moet uniek zijn

    **Opmerkingen**
    - Bij het aanmaken wordt ook in de Documenten API de gespiegelde relatie
      aangemaakt, echter zonder de relatie-informatie.

    list:
    Alle VERZOEK-INFORMATIEOBJECT relaties opvragen.

    Deze lijst kan gefilterd wordt met query-string parameters.

    retrieve:
    Een specifieke VERZOEK-INFORMATIEOBJECT relatie opvragen.

    Een specifieke VERZOEK-INFORMATIEOBJECT relatie opvragen.

    update:
    Werk een VERZOEK-INFORMATIEOBJECT relatie in zijn geheel bij.

    Je mag enkel de gegevens van de relatie bewerken, en niet de relatie zelf
    aanpassen.

    **Er wordt gevalideerd op**
    - `informatieobject` URL en `verzoek` URL mogen niet veranderen

    partial_update:
    Werk een VERZOEK-INFORMATIEOBJECT relatie deels bij.

    Je mag enkel de gegevens van de relatie bewerken, en niet de relatie zelf
    aanpassen.

    **Er wordt gevalideerd op**
    - `informatieobject` URL en `verzoek` URL mogen niet veranderen

    destroy:
    Verwijder een VERZOEK-INFORMATIEOBJECT relatie.

    Verwijder een VERZOEK-INFORMATIEOBJECT relatie.
    """

    queryset = VerzoekInformatieObject.objects.all()
    serializer_class = VerzoekInformatieObjectSerializer
    filterset_class = VerzoekInformatieObjectFilter
    lookup_field = "uuid"
    permission_classes = (AuthScopesRequired,)
    pagination_class = PageNumberPagination
    required_scopes = {
        "list": SCOPE_VERZOEKEN_ALLES_LEZEN,
        "retrieve": SCOPE_VERZOEKEN_ALLES_LEZEN,
        "create": SCOPE_VERZOEKEN_AANMAKEN,
        "destroy": SCOPE_VERZOEKEN_ALLES_VERWIJDEREN,
        "update": SCOPE_VERZOEKEN_BIJWERKEN,
        "partial_update": SCOPE_VERZOEKEN_BIJWERKEN,
    }
    notifications_kanaal = KANAAL_VERZOEKEN
    audit = AUDIT_VERZOEKEN

    def get_queryset(self):
        qs = super().get_queryset()

        # Do not display VerzoekInformatieObjecten that are marked to be deleted
        cache = caches["drc_sync"]

        # TODO: Store cachekeys somewhere central.
        marked_vios = cache.get("vios_marked_for_delete")
        if marked_vios:
            return qs.exclude(uuid__in=marked_vios)
        return qs


class VerzoekContactMomentViewSet(
    NotificationCreateMixin,
    NotificationDestroyMixin,
    AuditTrailCreateMixin,
    AuditTrailDestroyMixin,
    CheckQueryParamsMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.ReadOnlyModelViewSet,
):
    """
    Opvragen en bewerken van VERZOEK-CONTACTMOMENT relaties.

    create:
    Maak een VERZOEK-CONTACTMOMENT relatie aan.

    Registreer een CONTACTMOMENT bij een VERZOEK. Er worden twee types van
    relaties met andere objecten gerealiseerd:

    **Er wordt gevalideerd op**
    - geldigheid `verzoek` URL
    - geldigheid `contactmoment` URL
    - de combinatie `contactmoment` en `verzoek` moet uniek zijn

    list:
    Alle VERZOEK-CONTACTMOMENT relaties opvragen.

    Deze lijst kan gefilterd wordt met query-string parameters.

    retrieve:
    Een specifieke VERZOEK-CONTACTMOMENT relatie opvragen.

    Een specifieke VERZOEK-CONTACTMOMENT relatie opvragen.

    update:
    Werk een VERZOEK-CONTACTMOMENT relatie in zijn geheel bij.

    Je mag enkel de gegevens van de relatie bewerken, en niet de relatie zelf
    aanpassen.

    **Er wordt gevalideerd op**
    - `contactmoment` URL en `verzoek` URL mogen niet veranderen

    partial_update:
    Werk een VERZOEK-CONTACTMOMENT relatie deels bij.

    Je mag enkel de gegevens van de relatie bewerken, en niet de relatie zelf
    aanpassen.

    **Er wordt gevalideerd op**
    - `contactmoment` URL en `verzoek` URL mogen niet veranderen

    destroy:
    Verwijder een VERZOEK-CONTACTMOMENT relatie.

    Verwijder een VERZOEK-CONTACTMOMENT relatie.
    """

    queryset = VerzoekContactMoment.objects.all()
    serializer_class = VerzoekContactMomentSerializer
    filterset_class = VerzoekContactMomentFilter
    lookup_field = "uuid"
    permission_classes = (AuthScopesRequired,)
    pagination_class = PageNumberPagination
    required_scopes = {
        "list": SCOPE_VERZOEKEN_ALLES_LEZEN,
        "retrieve": SCOPE_VERZOEKEN_ALLES_LEZEN,
        "create": SCOPE_VERZOEKEN_AANMAKEN,
        "destroy": SCOPE_VERZOEKEN_ALLES_VERWIJDEREN,
        "update": SCOPE_VERZOEKEN_BIJWERKEN,
        "partial_update": SCOPE_VERZOEKEN_BIJWERKEN,
    }
    notifications_kanaal = KANAAL_VERZOEKEN
    audit = AUDIT_VERZOEKEN


class VerzoekProductViewSet(
    NotificationCreateMixin,
    NotificationDestroyMixin,
    AuditTrailCreateMixin,
    AuditTrailDestroyMixin,
    CheckQueryParamsMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.ReadOnlyModelViewSet,
):
    """
    Opvragen en bewerken van VERZOEK-PRODUCT relaties.

    create:
    Maak een VERZOEK-PRODUCT relatie aan.

    Registreer een PRODUCT bij een VERZOEK. Er worden twee types van
    relaties met andere objecten gerealiseerd:

    **Er wordt gevalideerd op**
    - geldigheid `verzoek` URL
    - geldigheid `product` URL

    list:
    Alle VERZOEK-PRODUCT relaties opvragen.

    Deze lijst kan gefilterd wordt met query-string parameters.

    retrieve:
    Een specifieke VERZOEK-PRODUCT relatie opvragen.

    Een specifieke VERZOEK-PRODUCT relatie opvragen.

    destroy:
    Verwijder een VERZOEK-PRODUCT relatie.

    Verwijder een VERZOEK-PRODUCT relatie.
    """

    queryset = VerzoekProduct.objects.all()
    serializer_class = VerzoekProductSerializer
    filterset_class = VerzoekProductFilter
    lookup_field = "uuid"
    permission_classes = (AuthScopesRequired,)
    pagination_class = PageNumberPagination
    required_scopes = {
        "list": SCOPE_VERZOEKEN_ALLES_LEZEN,
        "retrieve": SCOPE_VERZOEKEN_ALLES_LEZEN,
        "create": SCOPE_VERZOEKEN_AANMAKEN,
        "destroy": SCOPE_VERZOEKEN_ALLES_VERWIJDEREN,
        "update": SCOPE_VERZOEKEN_BIJWERKEN,
        "partial_update": SCOPE_VERZOEKEN_BIJWERKEN,
    }
    notifications_kanaal = KANAAL_VERZOEKEN
    audit = AUDIT_VERZOEKEN


class KlantVerzoekViewSet(
    NotificationCreateMixin,
    NotificationDestroyMixin,
    AuditTrailCreateMixin,
    AuditTrailDestroyMixin,
    CheckQueryParamsMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.ReadOnlyModelViewSet,
):
    """
    Opvragen en bewerken van KLANT-VERZOEK relaties.

    create:
    Maak een KLANT-VERZOEK relatie aan.

    list:
    Alle KLANT-VERZOEK relaties opvragen.

    Deze lijst kan gefilterd wordt met query-string parameters.

    retrieve:
    Een specifieke KLANT-VERZOEK relatie opvragen.

    Een specifieke KLANT-VERZOEK relatie opvragen.

    destroy:
    Verwijder een KLANT-VERZOEK relatie.

    Verwijder een KLANT-VERZOEK relatie.
    """

    queryset = KlantVerzoek.objects.all()
    serializer_class = KlantVerzoekSerializer
    filterset_class = KlantVerzoekFilter
    lookup_field = "uuid"
    permission_classes = (AuthScopesRequired,)
    pagination_class = PageNumberPagination
    required_scopes = {
        "list": SCOPE_VERZOEKEN_ALLES_LEZEN,
        "retrieve": SCOPE_VERZOEKEN_ALLES_LEZEN,
        "create": SCOPE_VERZOEKEN_AANMAKEN,
        "destroy": SCOPE_VERZOEKEN_ALLES_VERWIJDEREN,
        "update": SCOPE_VERZOEKEN_BIJWERKEN,
        "partial_update": SCOPE_VERZOEKEN_BIJWERKEN,
    }
    notifications_kanaal = KANAAL_VERZOEKEN
    audit = AUDIT_VERZOEKEN


class VerzoekAuditTrailViewSet(AuditTrailViewSet):
    """
    Opvragen van de audit trail regels.

    list:
    Alle audit trail regels behorend bij het VERZOEK.

    Alle audit trail regels behorend bij het VERZOEK.

    retrieve:
    Een specifieke audit trail regel opvragen.

    Een specifieke audit trail regel opvragen.
    """

    main_resource_lookup_field = "verzoek_uuid"
