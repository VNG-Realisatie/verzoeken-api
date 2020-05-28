from datetime import datetime

from django.utils.timezone import make_aware

from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import JWTAuthMixin, reverse

from verzoeken.datamodel.constants import VerzoekStatus
from verzoeken.datamodel.models import Verzoek
from verzoeken.datamodel.tests.factories import VerzoekFactory

KLANT = "http://some.klanten.nl/api/v1/klanten/12345"


class VerzoekTests(JWTAuthMixin, APITestCase):
    heeft_alle_autorisaties = True

    def test_list_verzoeken(self):
        list_url = reverse(Verzoek)
        VerzoekFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data), 2)

    def test_read_verzoek(self):
        verzoek = VerzoekFactory.create(
            klant=KLANT, registratiedatum=make_aware(datetime(2019, 1, 1)),
        )
        detail_url = reverse(verzoek)

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(
            data,
            {
                "url": f"http://testserver{detail_url}",
                "bronorganisatie": verzoek.bronorganisatie,
                "externeIdentificatie": verzoek.externe_identificatie,
                "identificatie": "VERZOEK-2019-0000000001",
                "klant": KLANT,
                "registratiedatum": "2019-01-01T00:00:00Z",
                "status": verzoek.status,
                "tekst": verzoek.tekst,
                "voorkeurskanaal": verzoek.voorkeurskanaal,
            },
        )

    def test_create_verzoek(self):
        list_url = reverse(Verzoek)
        data = {
            "bronorganisatie": "423182687",
            "klant": KLANT,
            "status": VerzoekStatus.ontvangen,
            "tekst": "some text",
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        verzoek = Verzoek.objects.get()

        self.assertEqual(verzoek.klant, KLANT)
        self.assertEqual(verzoek.tekst, "some text")
        self.assertGreater(len(verzoek.identificatie), 0)

    def test_update_verzoek(self):
        verzoek = VerzoekFactory.create()
        detail_url = reverse(verzoek)

        response = self.client.patch(detail_url, {"klant": KLANT})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        verzoek.refresh_from_db()

        self.assertEqual(verzoek.klant, KLANT)

    def test_destroy_verzoek(self):
        verzoek = VerzoekFactory.create()
        detail_url = reverse(verzoek)

        response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Verzoek.objects.count(), 0)
