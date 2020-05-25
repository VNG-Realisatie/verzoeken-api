from copy import deepcopy
from unittest.mock import patch

from django.test import override_settings

from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.audittrails.models import AuditTrail
from vng_api_common.tests import JWTAuthMixin, reverse
from zds_client.tests.mocks import mock_client

from verzoeken.datamodel.constants import VerzoekStatus
from verzoeken.datamodel.models import Verzoek, VerzoekInformatieObject, VerzoekProduct

from .mixins import VerzoekInformatieObjectSyncMixin

KLANT = "http://some.klanten.nl/api/v1/klanten/951e4660-3835-4643-8f9c-e523e364a30f"
PRODUCT = (
    "http://some.producten.nl/api/v1/producten/c110d562-d983-4c0e-b5f8-bab1525edd31"
)
INFORMATIE_OBJECT = (
    "http://some.drc.nl/api/v1/informatieobjecten/ed01f0f6-6caf-4729-a68a-93d98dbaea0b"
)


class AuditTrailTests(VerzoekInformatieObjectSyncMixin, JWTAuthMixin, APITestCase):

    heeft_alle_autorisaties = True

    def _create_verzoek(self):
        list_url = reverse(Verzoek)
        data = {
            "bronorganisatie": "423182687",
            "klant": KLANT,
            "status": VerzoekStatus.ontvangen,
            "tekst": "some text",
        }

        response = self.client.post(list_url, data)
        return response.data

    def test_create_verzoek_audittrail(self):
        verzoek_response = self._create_verzoek()

        audittrails = AuditTrail.objects.filter(hoofd_object=verzoek_response["url"])
        self.assertEqual(audittrails.count(), 1)

        verzoek_create_audittrail = audittrails.get()
        self.assertEqual(verzoek_create_audittrail.bron, "Verzoeken")
        self.assertEqual(verzoek_create_audittrail.actie, "create")
        self.assertEqual(verzoek_create_audittrail.resultaat, 201)
        self.assertEqual(verzoek_create_audittrail.oud, None)
        self.assertEqual(verzoek_create_audittrail.nieuw, verzoek_response)

    def test_update_verzoek_audittrails(self):
        verzoek_data = self._create_verzoek()
        modified_data = deepcopy(verzoek_data)
        url = modified_data.pop("url")
        del modified_data["tekst"]
        modified_data["tekst"] = "new"

        response = self.client.put(url, modified_data)

        verzoek_response = response.data

        audittrails = AuditTrail.objects.filter(hoofd_object=verzoek_response["url"])
        self.assertEqual(audittrails.count(), 2)

        verzoek_update_audittrail = audittrails[1]
        self.assertEqual(verzoek_update_audittrail.bron, "Verzoeken")
        self.assertEqual(verzoek_update_audittrail.actie, "update")
        self.assertEqual(verzoek_update_audittrail.resultaat, 200)
        self.assertEqual(verzoek_update_audittrail.oud, verzoek_data)
        self.assertEqual(verzoek_update_audittrail.nieuw, verzoek_response)

    def test_partial_update_verzoek_audittrails(self):
        verzoek_data = self._create_verzoek()

        response = self.client.patch(verzoek_data["url"], {"tekst": "new"})
        verzoek_response = response.data

        audittrails = AuditTrail.objects.filter(hoofd_object=verzoek_response["url"])
        self.assertEqual(audittrails.count(), 2)

        verzoek_update_audittrail = audittrails[1]
        self.assertEqual(verzoek_update_audittrail.bron, "Verzoeken")
        self.assertEqual(verzoek_update_audittrail.actie, "partial_update")
        self.assertEqual(verzoek_update_audittrail.resultaat, 200)
        self.assertEqual(verzoek_update_audittrail.oud, verzoek_data)
        self.assertEqual(verzoek_update_audittrail.nieuw, verzoek_response)

    def test_delete_verzoek_cascade_audittrails(self):
        verzoek_data = self._create_verzoek()

        # Delete the Verzoek
        self.client.delete(verzoek_data["url"])

        audittrails = AuditTrail.objects.filter(hoofd_object=verzoek_data["url"])
        self.assertFalse(audittrails.exists())

    def test_create_and_delete_verzoek_product_audittrails(self):
        verzoek_response = self._create_verzoek()

        url = reverse(VerzoekProduct)
        verzoek_product_data = {"verzoek": verzoek_response["url"], "product": PRODUCT}

        response = self.client.post(url, verzoek_product_data)

        verzoek_product_response = response.data

        audittrails = AuditTrail.objects.filter(
            hoofd_object=verzoek_response["url"]
        ).order_by("pk")
        self.assertEqual(audittrails.count(), 2)

        # Verify that the audittrail for the VerzoekProduct creation contains the
        # correct information
        resultaat_create_audittrail = audittrails[1]
        self.assertEqual(resultaat_create_audittrail.bron, "Verzoeken")
        self.assertEqual(resultaat_create_audittrail.actie, "create")
        self.assertEqual(resultaat_create_audittrail.resultaat, 201)
        self.assertEqual(resultaat_create_audittrail.oud, None)
        self.assertEqual(resultaat_create_audittrail.nieuw, verzoek_product_response)

        response = self.client.delete(verzoek_product_response["url"])
        self.assertEqual(audittrails.count(), 3)

        # Verify that the audittrail for the VerzoekProduct deletion contains the
        # correct information
        resultaat_delete_audittrail = audittrails[2]
        self.assertEqual(resultaat_delete_audittrail.bron, "Verzoeken")
        self.assertEqual(resultaat_delete_audittrail.actie, "destroy")
        self.assertEqual(resultaat_delete_audittrail.resultaat, 204)
        self.assertEqual(resultaat_delete_audittrail.oud, verzoek_product_response)
        self.assertEqual(resultaat_delete_audittrail.nieuw, None)

    @override_settings(LINK_FETCHER="vng_api_common.mocks.link_fetcher_200")
    @patch("vng_api_common.validators.obj_has_shape", return_value=True)
    def test_create_verzoekinformatieobject_audittrail(self, *mocks):
        verzoek_response = self._create_verzoek()

        url = reverse(VerzoekInformatieObject)

        responses = {
            INFORMATIE_OBJECT: {"url": INFORMATIE_OBJECT, "identificatie": "12345"}
        }

        with mock_client(responses):
            response = self.client.post(
                url,
                {
                    "verzoek": verzoek_response["url"],
                    "informatieobject": INFORMATIE_OBJECT,
                },
            )

        verzoekinformatieobject_response = response.data

        audittrails = AuditTrail.objects.filter(hoofd_object=verzoek_response["url"])
        self.assertEqual(audittrails.count(), 2)

        # Verify that the audittrail for the VerzoekInformatieObject creation
        # contains the correct information
        bio_create_audittrail = audittrails[1]
        self.assertEqual(bio_create_audittrail.bron, "Verzoeken")
        self.assertEqual(bio_create_audittrail.actie, "create")
        self.assertEqual(bio_create_audittrail.resultaat, 201)
        self.assertEqual(bio_create_audittrail.oud, None)
        self.assertEqual(bio_create_audittrail.nieuw, verzoekinformatieobject_response)

    def test_read_audittrail(self):
        self._create_verzoek()

        verzoek = Verzoek.objects.get()
        audittrails = AuditTrail.objects.get()
        audittrails_url = reverse(audittrails, kwargs={"verzoek_uuid": verzoek.uuid})

        response_audittrails = self.client.get(audittrails_url)

        self.assertEqual(response_audittrails.status_code, status.HTTP_200_OK)
