import logging

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.cache import caches
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.urls import reverse

from vng_api_common.models import APICredential
from zds_client import Client

from verzoeken.datamodel.models import VerzoekInformatieObject

logger = logging.getLogger(__name__)


class SyncError(Exception):
    pass


def sync_create_vio(relation: VerzoekInformatieObject):
    operation = "create"

    # build the URL of the Verzoek
    path = reverse(
        "verzoek-detail",
        kwargs={
            "version": settings.REST_FRAMEWORK["DEFAULT_VERSION"],
            "uuid": relation.verzoek.uuid,
        },
    )
    domain = Site.objects.get_current().domain
    protocol = "https" if settings.IS_HTTPS else "http"
    verzoek_url = f"{protocol}://{domain}{path}"

    logger.info("Verzoek: %s", verzoek_url)
    logger.info("Informatieobject: %s", relation.informatieobject)

    # Define the remote resource with which we need to interact
    resource = "objectinformatieobject"
    client = Client.from_url(relation.informatieobject)

    # TODO?
    client.auth = APICredential.get_auth(relation.informatieobject)

    try:
        operation_function = getattr(client, operation)
        operation_function(
            resource,
            {
                "object": verzoek_url,
                "informatieobject": relation.informatieobject,
                "objectType": "verzoek",
            },
        )
    except Exception as exc:
        logger.error(f"Could not {operation} remote relation", exc_info=1)
        raise SyncError(f"Could not {operation} remote relation") from exc


def sync_delete_vio(relation: VerzoekInformatieObject):
    operation = "delete"

    # build the URL of the Verzoek
    path = reverse(
        "verzoek-detail",
        kwargs={
            "version": settings.REST_FRAMEWORK["DEFAULT_VERSION"],
            "uuid": relation.verzoek.uuid,
        },
    )
    domain = Site.objects.get_current().domain
    protocol = "https" if settings.IS_HTTPS else "http"
    verzoek_url = f"{protocol}://{domain}{path}"

    logger.info("Verzoek: %s", verzoek_url)
    logger.info("Informatieobject: %s", relation.informatieobject)

    # Define the remote resource with which we need to interact
    resource = "objectinformatieobject"
    client = Client.from_url(relation.informatieobject)
    client.auth = APICredential.get_auth(relation.informatieobject)

    # Retrieve the url of the relation between the object and the
    response = client.list(resource, query_params={"object": verzoek_url})
    try:
        relation_url = response[0]["url"]
    except IndexError as exc:
        msg = "No relations found in DRC for this Verzoek"
        logger.error(msg, exc_info=1)
        raise IndexError(msg) from exc

    try:
        operation_function = getattr(client, operation)
        operation_function(resource, url=relation_url)
    except Exception as exc:
        logger.error(f"Could not {operation} remote relation", exc_info=1)
        raise SyncError(f"Could not {operation} remote relation") from exc


@receiver(
    [post_save, pre_delete],
    sender=VerzoekInformatieObject,
    dispatch_uid="sync.sync_informatieobject_relation",
)
def sync_informatieobject_relation(
    sender, instance: VerzoekInformatieObject = None, **kwargs
):
    cache_key = "vios_marked_for_delete"

    signal = kwargs["signal"]
    if signal is post_save and kwargs.get("created", False):
        sync_create_vio(instance)
    elif signal is pre_delete:
        # Add the uuid of the VerzoekInformatieObject to the list of vios that are
        # marked for delete, causing them not to show up when performing
        # GET requests on the verzoeken, allowing the validation in the DRC to pass
        cache = caches["drc_sync"]
        marked_vios = cache.get(cache_key)
        if marked_vios:
            cache.set(cache_key, marked_vios + [instance.uuid])
        else:
            cache.set(cache_key, [instance.uuid])

        try:
            sync_delete_vio(instance)
        finally:
            marked_vios = cache.get(cache_key)
            marked_vios.remove(instance.uuid)
            cache.set(cache_key, marked_vios)
