import requests_mock
from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import JWTAuthMixin, get_validation_errors, reverse

from verzoeken.datamodel.models import KlantVerzoek
from verzoeken.datamodel.tests.factories import KlantVerzoekFactory, VerzoekFactory

KLANT = "http://some.klanten.nl/api/v1/klanten/12345"


class KlantVerzoekTests(JWTAuthMixin, APITestCase):
    heeft_alle_autorisaties = True

    def test_list_klantverzoek(self):
        list_url = reverse(KlantVerzoek)
        KlantVerzoekFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_list_filter_klantverzoek(self):
        list_url = reverse(KlantVerzoek)
        vc1 = KlantVerzoekFactory.create()
        vc2 = KlantVerzoekFactory.create()

        response = self.client.get(
            list_url,
            {"verzoek": f"http://testserver.com{reverse(vc1.verzoek)}"},
            HTTP_HOST="testserver.com",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 1)

        response = self.client.get(
            list_url,
            {"klant": vc2.klant},
            HTTP_HOST="testserver.com",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 1)

    def test_read_klantverzoek(self):
        klantverzoek = KlantVerzoekFactory.create()
        verzoek_url = reverse(klantverzoek.verzoek)
        detail_url = reverse(klantverzoek)
        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(
            data,
            {
                "url": f"http://testserver{detail_url}",
                "verzoek": f"http://testserver{verzoek_url}",
                "klant": klantverzoek.klant,
                "rol": klantverzoek.rol,
                "indicatieMachtiging": klantverzoek.indicatie_machtiging,
            },
        )

    def test_create_klantverzoek(self):
        verzoek = VerzoekFactory.create()
        verzoek_url = reverse(verzoek)
        list_url = reverse(KlantVerzoek)
        data = {"verzoek": verzoek_url, "klant": KLANT}

        with requests_mock.Mocker() as m:
            m.get(KLANT, json={})
            response = self.client.post(list_url, data)

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, response.content
        )

        klantverzoek = KlantVerzoek.objects.get()

        self.assertEqual(klantverzoek.verzoek, verzoek)
        self.assertEqual(klantverzoek.klant, KLANT)

    def test_create_klantverzoek_with_invalid_klant_url(self):
        verzoek = VerzoekFactory.create()
        verzoek_url = reverse(verzoek)
        list_url = reverse(KlantVerzoek)
        data = {"verzoek": verzoek_url, "klant": KLANT}

        with requests_mock.Mocker() as m:
            m.get(KLANT, status_code=404)
            response = self.client.post(list_url, data)

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.content
        )

        self.assertEqual(KlantVerzoek.objects.count(), 0)

        error = get_validation_errors(response, "klant")
        self.assertEqual(error["code"], "bad-url")

    def test_destroy_klantverzoek(self):
        klantverzoek = KlantVerzoekFactory.create()
        detail_url = reverse(klantverzoek)

        response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(KlantVerzoek.objects.count(), 0)

    def test_pagination_default(self):
        KlantVerzoekFactory.create_batch(2)
        url = reverse(KlantVerzoek)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 2)
        self.assertIsNone(response_data["previous"])
        self.assertIsNone(response_data["next"])

    def test_pagination_page_param(self):
        KlantVerzoekFactory.create_batch(2)
        url = reverse(KlantVerzoek)

        response = self.client.get(url, {"page": 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 2)
        self.assertIsNone(response_data["previous"])
        self.assertIsNone(response_data["next"])
