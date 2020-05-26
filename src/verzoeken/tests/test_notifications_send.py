from unittest.mock import patch

from django.test import override_settings

from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import JWTAuthMixin, get_operation_url

from verzoeken.datamodel.constants import VerzoekStatus
from verzoeken.datamodel.tests.factories import VerzoekProductFactory

KLANT = "http://some.klanten.nl/api/v1/klanten/951e4660-3835-4643-8f9c-e523e364a30f"


@freeze_time("2018-09-07T00:00:00Z")
@override_settings(NOTIFICATIONS_DISABLED=False)
class SendNotifTestCase(JWTAuthMixin, APITestCase):

    heeft_alle_autorisaties = True

    @patch("zds_client.Client.from_url")
    def test_send_notif_create_verzoek(self, mock_client):
        """
        Check if notifications will be send when Verzoek is created
        """
        client = mock_client.return_value
        url = get_operation_url("verzoek_create")
        data = {
            "bronorganisatie": "423182687",
            "klant": KLANT,
            "status": VerzoekStatus.ontvangen,
            "tekst": "some text",
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

        data = response.json()
        client.create.assert_called_once_with(
            "notificaties",
            {
                "kanaal": "verzoeken",
                "hoofdObject": data["url"],
                "resource": "verzoek",
                "resourceUrl": data["url"],
                "actie": "create",
                "aanmaakdatum": "2018-09-07T00:00:00Z",
                "kenmerken": {"bronorganisatie": "423182687"},
            },
        )

    @patch("zds_client.Client.from_url")
    def test_send_notif_delete_verzoekproduct(self, mock_client):
        """
        Check if notifications will be send when VerzoekProduct is deleted
        """
        client = mock_client.return_value
        verzoek_product = VerzoekProductFactory.create(
            verzoek__bronorganisatie=423182687
        )
        verzoek_product_url = get_operation_url(
            "verzoekproduct_delete", uuid=verzoek_product.uuid
        )
        verzoek_url = get_operation_url(
            "verzoek_read", uuid=verzoek_product.verzoek.uuid
        )

        response = self.client.delete(verzoek_product_url)

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT, response.data
        )

        client.create.assert_called_once_with(
            "notificaties",
            {
                "kanaal": "verzoeken",
                "hoofdObject": f"http://testserver{verzoek_url}",
                "resource": "verzoekproduct",
                "resourceUrl": f"http://testserver{verzoek_product_url}",
                "actie": "destroy",
                "aanmaakdatum": "2018-09-07T00:00:00Z",
                "kenmerken": {"bronorganisatie": "423182687"},
            },
        )
