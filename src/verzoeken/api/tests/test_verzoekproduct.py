from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import JWTAuthMixin, get_validation_errors, reverse

from verzoeken.datamodel.models import VerzoekProduct
from verzoeken.datamodel.tests.factories import VerzoekFactory, VerzoekProductFactory


class VerzoekProductTests(JWTAuthMixin, APITestCase):
    heeft_alle_autorisaties = True

    def test_list_verzoekproduct(self):
        list_url = reverse(VerzoekProduct)
        VerzoekProductFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_list_filter_verzoekproduct(self):
        list_url = reverse(VerzoekProduct)
        vp1 = VerzoekProductFactory.create(product_code="test")
        vp2 = VerzoekProductFactory.create(product="https://www.example.com")

        response = self.client.get(
            list_url, {"productIdentificatie__code": vp1.product_code}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 1)

        response = self.client.get(list_url, {"product": vp2.product})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 1)

    def test_read_verzoekproduct_with_product_url(self):
        verzoekproduct = VerzoekProductFactory.create()
        detail_url = reverse(verzoekproduct)
        verzoek_url = reverse(verzoekproduct.verzoek)

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(
            data,
            {
                "url": f"http://testserver{detail_url}",
                "verzoek": f"http://testserver{verzoek_url}",
                "product": verzoekproduct.product,
                "productIdentificatie": {"code": ""},
            },
        )

    def test_read_verzoekproduct_with_product_id(self):
        verzoekproduct = VerzoekProductFactory.create(product_code="test", product="")
        detail_url = reverse(verzoekproduct)
        verzoek_url = reverse(verzoekproduct.verzoek)

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(
            data,
            {
                "url": f"http://testserver{detail_url}",
                "verzoek": f"http://testserver{verzoek_url}",
                "product": "",
                "productIdentificatie": {"code": "test"},
            },
        )

    def test_create_verzoekproduct_with_product_url(self):
        verzoek = VerzoekFactory.create()
        verzoek_url = reverse(verzoek)
        list_url = reverse(VerzoekProduct)
        data = {"verzoek": verzoek_url, "product": "https://example.com/"}

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        verzoekproduct = VerzoekProduct.objects.get()

        self.assertEqual(verzoekproduct.verzoek, verzoek)
        self.assertEqual(verzoekproduct.product, data["product"])

    def test_create_verzoekproduct_with_product_id(self):
        verzoek = VerzoekFactory.create()
        verzoek_url = reverse(verzoek)
        list_url = reverse(VerzoekProduct)
        data = {"verzoek": verzoek_url, "productIdentificatie": {"code": "test"}}

        response = self.client.post(list_url, data)

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, response.content
        )

        verzoekproduct = VerzoekProduct.objects.get()

        self.assertEqual(verzoekproduct.verzoek, verzoek)
        self.assertEqual(
            verzoekproduct.product_code, data["productIdentificatie"]["code"]
        )

    def test_create_verzoekproduct_without_product(self):
        verzoek = VerzoekFactory.create()
        verzoek_url = reverse(verzoek)
        list_url = reverse(VerzoekProduct)
        data = {"verzoek": verzoek_url}

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        validation_error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(validation_error["code"], "invalid-product")

    def test_destroy_verzoekproduct(self):
        verzoekproduct = VerzoekProductFactory.create()
        detail_url = reverse(verzoekproduct)

        response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(VerzoekProduct.objects.count(), 0)

    def test_pagination_default(self):
        VerzoekProductFactory.create_batch(2)
        url = reverse(VerzoekProduct)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 2)
        self.assertIsNone(response_data["previous"])
        self.assertIsNone(response_data["next"])

    def test_pagination_page_param(self):
        VerzoekProductFactory.create_batch(2)
        url = reverse(VerzoekProduct)

        response = self.client.get(url, {"page": 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 2)
        self.assertIsNone(response_data["previous"])
        self.assertIsNone(response_data["next"])
