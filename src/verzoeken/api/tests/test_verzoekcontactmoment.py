from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import JWTAuthMixin, reverse

from verzoeken.datamodel.models import VerzoekContactMoment
from verzoeken.datamodel.tests.factories import (
    VerzoekContactMomentFactory,
    VerzoekFactory,
)

CONTACTMOMENT = "http://some.contactmomenten.nl/api/v1/contactmomenten/12345"


class VerzoekContactMomentTests(JWTAuthMixin, APITestCase):
    heeft_alle_autorisaties = True

    def test_list_verzoekcontactmoment(self):
        list_url = reverse(VerzoekContactMoment)
        VerzoekContactMomentFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_list_filter_verzoekcontactmoment(self):
        list_url = reverse(VerzoekContactMoment)
        vc1 = VerzoekContactMomentFactory.create()
        vc2 = VerzoekContactMomentFactory.create()

        response = self.client.get(
            list_url,
            {"verzoek": f"http://testserver.com{reverse(vc1.verzoek)}"},
            HTTP_HOST="testserver.com",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 1)

        response = self.client.get(
            list_url, {"contactmoment": vc2.contactmoment}, HTTP_HOST="testserver.com",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 1)

    def test_read_verzoekcontactmoment(self):
        verzoekcontactmoment = VerzoekContactMomentFactory.create()
        verzoek_url = reverse(verzoekcontactmoment.verzoek)
        detail_url = reverse(verzoekcontactmoment)
        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(
            data,
            {
                "url": f"http://testserver{detail_url}",
                "verzoek": f"http://testserver{verzoek_url}",
                "contactmoment": verzoekcontactmoment.contactmoment,
            },
        )

    def test_create_verzoekcontactmoment(self):
        verzoek = VerzoekFactory.create()
        verzoek_url = reverse(verzoek)
        list_url = reverse(VerzoekContactMoment)
        data = {"verzoek": verzoek_url, "contactmoment": CONTACTMOMENT}

        response = self.client.post(list_url, data)

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, response.content
        )

        verzoekcontactmoment = VerzoekContactMoment.objects.get()

        self.assertEqual(verzoekcontactmoment.verzoek, verzoek)
        self.assertEqual(verzoekcontactmoment.contactmoment, CONTACTMOMENT)

    def test_destroy_verzoekcontactmoment(self):
        verzoekcontactmoment = VerzoekContactMomentFactory.create()
        detail_url = reverse(verzoekcontactmoment)

        response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(VerzoekContactMoment.objects.count(), 0)

    def test_pagination_default(self):
        VerzoekContactMomentFactory.create_batch(2)
        url = reverse(VerzoekContactMoment)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 2)
        self.assertIsNone(response_data["previous"])
        self.assertIsNone(response_data["next"])

    def test_pagination_page_param(self):
        VerzoekContactMomentFactory.create_batch(2)
        url = reverse(VerzoekContactMoment)

        response = self.client.get(url, {"page": 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 2)
        self.assertIsNone(response_data["previous"])
        self.assertIsNone(response_data["next"])
