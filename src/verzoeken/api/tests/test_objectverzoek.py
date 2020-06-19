import uuid
from unittest.mock import patch

from django.test import override_settings

from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import JWTAuthMixin, get_validation_errors, reverse
from zds_client.tests.mocks import mock_client

from verzoeken.datamodel.constants import ObjectTypes
from verzoeken.datamodel.models import ObjectVerzoek
from verzoeken.datamodel.tests.factories import ObjectVerzoekFactory, VerzoekFactory

ZAAK = "http://example.com/api/v1/zaken/1"


class ObjectVerzoekTests(JWTAuthMixin, APITestCase):
    heeft_alle_autorisaties = True

    def test_list_objectverzoeken(self):
        list_url = reverse(ObjectVerzoek)
        ObjectVerzoekFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_objectverzoek(self):
        verzoek = VerzoekFactory.create()
        verzoek_url = reverse(verzoek)
        objectverzoek = ObjectVerzoekFactory.create(verzoek=verzoek)
        detail_url = reverse(objectverzoek)

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(
            data,
            {
                "url": f"http://testserver{detail_url}",
                "verzoek": f"http://testserver{verzoek_url}",
                "objectType": objectverzoek.object_type,
                "object": objectverzoek.object,
            },
        )

    @override_settings(LINK_FETCHER="vng_api_common.mocks.link_fetcher_200",)
    @patch(
        "zds_client.client.get_operation_url", return_value="/api/v1/zaakverzoeken",
    )
    @patch("zds_client.tests.mocks.MockClient.fetch_schema", return_value={})
    @patch("vng_api_common.validators.obj_has_shape", return_value=True)
    def test_create_objectverzoek(self, *mocks):
        verzoek = VerzoekFactory.create()
        verzoek_url = reverse(verzoek)
        list_url = reverse(ObjectVerzoek)
        data = {
            "verzoek": verzoek_url,
            "objectType": ObjectTypes.zaak,
            "object": ZAAK,
        }
        responses = {
            "http://example.com/api/v1/zaakverzoeken": [
                {
                    "url": f"https://example.com/api/v1/zaakverzoeken/{uuid.uuid4()}",
                    "verzoek": f"http://testserver/api/v1/verzoeken/{uuid.uuid4()}",
                    "zaak": ZAAK,
                }
            ]
        }
        with mock_client(responses):
            response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

        objectverzoek = ObjectVerzoek.objects.get()

        self.assertEqual(objectverzoek.verzoek, verzoek)
        self.assertEqual(objectverzoek.object_type, ObjectTypes.zaak)
        self.assertEqual(objectverzoek.object, ZAAK)

    @override_settings(LINK_FETCHER="vng_api_common.mocks.link_fetcher_200",)
    @patch(
        "zds_client.client.get_operation_url", return_value="/api/v1/zaakverzoeken",
    )
    @patch("zds_client.tests.mocks.MockClient.fetch_schema", return_value={})
    @patch("vng_api_common.validators.obj_has_shape", return_value=True)
    def test_create_objectverzoek_fail_no_remote_relation(self, *mocks):
        verzoek = VerzoekFactory.create()
        verzoek_url = reverse(verzoek)
        list_url = reverse(ObjectVerzoek)
        data = {
            "verzoek": verzoek_url,
            "objectType": ObjectTypes.zaak,
            "object": ZAAK,
        }
        responses = {"http://example.com/api/v1/zaakverzoeken": []}
        with mock_client(responses):
            response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")

        self.assertEqual(error["code"], "inconsistent-relation")

    @patch(
        "zds_client.client.get_operation_url", return_value="/api/v1/zaakverzoeken",
    )
    @patch("zds_client.tests.mocks.MockClient.fetch_schema", return_value={})
    def test_destroy_objectverzoek(self, *mocks):
        objectverzoek = ObjectVerzoekFactory.create(
            object=ZAAK, object_type=ObjectTypes.zaak
        )
        detail_url = reverse(objectverzoek)
        responses = {"http://example.com/api/v1/zaakverzoeken": []}

        with mock_client(responses):
            response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ObjectVerzoek.objects.count(), 0)

    @patch(
        "zds_client.client.get_operation_url", return_value="/api/v1/zaakverzoeken",
    )
    @patch("zds_client.tests.mocks.MockClient.fetch_schema", return_value={})
    def test_destroy_fail_existing_relation(self, *mocks):
        objectverzoek = ObjectVerzoekFactory.create(
            object=ZAAK, object_type=ObjectTypes.zaak
        )
        detail_url = reverse(objectverzoek)
        responses = {
            "http://example.com/api/v1/zaakverzoeken": [
                {
                    "url": f"https://example.com/api/v1/zaakverzoeken/{uuid.uuid4()}",
                    "verzoek": f"http://testserver/api/v1/verzoeken/{uuid.uuid4()}",
                    "zaak": ZAAK,
                }
            ]
        }

        with mock_client(responses):
            response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")

        self.assertEqual(error["code"], "remote-relation-exists")


class ObjectVerzoekFilterTests(JWTAuthMixin, APITestCase):
    heeft_alle_autorisaties = True
    list_url = reverse(ObjectVerzoek)

    def test_filter_verzoek(self):
        oio = ObjectVerzoekFactory.create()
        verzoek_url = reverse(oio.verzoek)

        response = self.client.get(
            self.list_url,
            {"verzoek": f"http://testserver.com{verzoek_url}"},
            HTTP_HOST="testserver.com",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(
            response.data["results"][0]["verzoek"],
            f"http://testserver.com{verzoek_url}",
        ),

    def test_filter_object(self):
        oio = ObjectVerzoekFactory.create()

        response = self.client.get(self.list_url, {"object": oio.object})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["object"], oio.object)

    def test_pagination_default(self):
        ObjectVerzoekFactory.create_batch(2)
        url = reverse(ObjectVerzoek)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 2)
        self.assertIsNone(response_data["previous"])
        self.assertIsNone(response_data["next"])

    def test_pagination_page_param(self):
        ObjectVerzoekFactory.create_batch(2)
        url = reverse(ObjectVerzoek)

        response = self.client.get(url, {"page": 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 2)
        self.assertIsNone(response_data["previous"])
        self.assertIsNone(response_data["next"])
