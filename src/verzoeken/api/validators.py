from collections import OrderedDict

from django.conf import settings
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _

from rest_framework import exceptions, serializers
from rest_framework.validators import UniqueTogetherValidator
from vng_api_common.models import APICredential
from vng_api_common.validators import ResourceValidator
from zds_client import ClientError

from verzoeken.datamodel.models import ObjectVerzoek

from .auth import get_auth
from .utils import get_absolute_url


class ObjectVerzoekDestroyValidator:
    message = _(
        "The canonical remote relation still exists, this relation cannot be deleted."
    )
    code = "remote-relation-exists"
    resource_name = "verzoek"

    def __call__(self, objectklantinteractie: ObjectVerzoek):
        object_url = objectklantinteractie.object
        klantinteractie_uuid = getattr(objectklantinteractie, self.resource_name).uuid
        klantinteractie_url = get_absolute_url(
            f"{self.resource_name}-detail", uuid=klantinteractie_uuid
        )

        Client = import_string(settings.ZDS_CLIENT_CLASS)
        client = Client.from_url(object_url)
        client.auth = APICredential.get_auth(object_url)

        resource = f"{objectklantinteractie.object_type}{self.resource_name}"

        try:
            relations = client.list(
                resource,
                query_params={
                    objectklantinteractie.object_type: object_url,
                    f"{self.resource_name}": klantinteractie_url,
                },
            )
        except ClientError as exc:
            raise serializers.ValidationError(
                exc.args[0], code="relation-lookup-error"
            ) from exc

        if len(relations) >= 1:
            raise serializers.ValidationError(self.message, code=self.code)


class ObjectVerzoekCreateValidator:
    """
    Validate that the VERZOEK is already linked to the OBJECT in the remote component.
    """

    message = _("The verzoek has no relations to {object}")
    code = "inconsistent-relation"
    resource_name = "verzoek"

    def __call__(self, attrs: OrderedDict):
        object_url = attrs["object"]
        object_type = attrs["object_type"]
        klantinteractie_url = get_absolute_url(
            f"{self.resource_name}-detail", uuid=attrs[self.resource_name].uuid
        )

        # dynamic so that it can be mocked in tests easily
        Client = import_string(settings.ZDS_CLIENT_CLASS)
        client = Client.from_url(object_url)
        client.auth = APICredential.get_auth(object_url)

        resource = f"{object_type}{self.resource_name}"
        oas_schema = settings.ZRC_API_SPEC

        try:
            ResourceValidator(
                object_type.capitalize(),
                oas_schema,
                get_auth=get_auth,
                headers={"Accept-Crs": "EPSG:4326"},
            )(object_url)
        except exceptions.ValidationError as exc:
            raise serializers.ValidationError(
                {"object": exc.detail}, code=ResourceValidator.code
            )

        try:
            relations = client.list(
                resource,
                query_params={
                    object_type: object_url,
                    f"{self.resource_name}": klantinteractie_url,
                },
            )

        except ClientError as exc:
            raise serializers.ValidationError(
                exc.args[0], code="relation-validation-error"
            ) from exc

        if len(relations) == 0:
            raise serializers.ValidationError(
                self.message.format(object=object_type), code=self.code
            )


class KlantProductUniqueTogetherValidator(UniqueTogetherValidator):
    def enforce_required_fields(self, attrs):
        # These attributes are optional, so this should not be enforced
        return

    def __call__(self, attrs):
        # To ensure that the validation does not fail in case the attributes
        # are missing (since they are not required)
        if ("product" in self.fields and "product" not in attrs) or (
            "product_code" in self.fields and "product_code" not in attrs
        ):
            return
        super().__call__(attrs)
