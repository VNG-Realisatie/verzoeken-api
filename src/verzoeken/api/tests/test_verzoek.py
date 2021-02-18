from datetime import datetime

from django.utils.timezone import make_aware

from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import JWTAuthMixin, get_validation_errors, reverse

from verzoeken.datamodel.constants import VerzoekStatus
from verzoeken.datamodel.models import Verzoek
from verzoeken.datamodel.tests.factories import VerzoekFactory


class VerzoekTests(JWTAuthMixin, APITestCase):
    heeft_alle_autorisaties = True

    def test_list_verzoeken(self):
        list_url = reverse(Verzoek)
        VerzoekFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data["results"]), 2)

    def test_read_verzoek(self):
        in_te_trekken_verzoek, aangevulde_verzoek = VerzoekFactory.create_batch(2)
        verzoek = VerzoekFactory.create(
            registratiedatum=make_aware(datetime(2019, 1, 1)),
            in_te_trekken_verzoek=in_te_trekken_verzoek,
            aangevulde_verzoek=aangevulde_verzoek,
        )
        intrekkende_verzoek = VerzoekFactory.create(in_te_trekken_verzoek=verzoek)
        aanvullende_verzoek = VerzoekFactory.create(aangevulde_verzoek=verzoek)
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
                "registratiedatum": "2019-01-01T00:00:00Z",
                "status": verzoek.status,
                "tekst": verzoek.tekst,
                "voorkeurskanaal": verzoek.voorkeurskanaal,
                "inTeTrekkenVerzoek": f"http://testserver{reverse(in_te_trekken_verzoek)}",
                "intrekkendeVerzoek": f"http://testserver{reverse(intrekkende_verzoek)}",
                "aangevuldeVerzoek": f"http://testserver{reverse(aangevulde_verzoek)}",
                "aanvullendeVerzoek": f"http://testserver{reverse(aanvullende_verzoek)}",
            },
        )

    def test_create_verzoek(self):
        in_te_trekken_verzoek, aangevulde_verzoek = VerzoekFactory.create_batch(2)
        list_url = reverse(Verzoek)
        data = {
            "bronorganisatie": "423182687",
            "status": VerzoekStatus.ontvangen,
            "tekst": "some text",
            "inTeTrekkenVerzoek": reverse(in_te_trekken_verzoek),
            "aangevuldeVerzoek": reverse(aangevulde_verzoek),
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        verzoek = Verzoek.objects.get(bronorganisatie="423182687")

        self.assertEqual(verzoek.tekst, "some text")
        self.assertGreater(len(verzoek.identificatie), 0)
        self.assertEqual(verzoek.in_te_trekken_verzoek, in_te_trekken_verzoek)
        self.assertEqual(verzoek.aangevulde_verzoek, aangevulde_verzoek)

    def test_update_verzoek(self):
        verzoek = VerzoekFactory.create()
        detail_url = reverse(verzoek)

        response = self.client.patch(detail_url, {"tekst": "new"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        verzoek.refresh_from_db()

        self.assertEqual(verzoek.tekst, "new")

    def test_destroy_verzoek(self):
        verzoek = VerzoekFactory.create()
        detail_url = reverse(verzoek)

        response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Verzoek.objects.count(), 0)

    def test_pagination_default(self):
        VerzoekFactory.create_batch(2)
        url = reverse(Verzoek)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 2)
        self.assertIsNone(response_data["previous"])
        self.assertIsNone(response_data["next"])

    def test_pagination_page_param(self):
        VerzoekFactory.create_batch(2)
        url = reverse(Verzoek)

        response = self.client.get(url, {"page": 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 2)
        self.assertIsNone(response_data["previous"])
        self.assertIsNone(response_data["next"])

    def test_update_verzoek_unique_bronorganisatie_and_identificatie(self):
        VerzoekFactory.create(bronorganisatie="000000000", identificatie="unique")

        # Create verzoek with same identificatie, but different bronorganisatie
        verzoek = VerzoekFactory.create(identificatie="unique")
        detail_url = reverse(verzoek)

        response = self.client.patch(detail_url, {"bronorganisatie": "000000000"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "identificatie")
        self.assertEqual(error["code"], "identificatie-niet-uniek")


class VerzoekFilterTests(JWTAuthMixin, APITestCase):
    heeft_alle_autorisaties = True
    maxDiff = None

    def test_filter_identificatie(self):
        VerzoekFactory.create(identificatie="000000000")
        VerzoekFactory.create(identificatie="123456782")
        url = reverse(Verzoek)

        response = self.client.get(url, {"identificatie": "000000000"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 1)

        result = response_data["results"][0]
        self.assertEqual(result["identificatie"], "000000000")

    def test_filter_bronorganisatie(self):
        VerzoekFactory.create(bronorganisatie="000000000")
        VerzoekFactory.create(bronorganisatie="123456782")
        url = reverse(Verzoek)

        response = self.client.get(url, {"bronorganisatie": "000000000"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 1)

        result = response_data["results"][0]
        self.assertEqual(result["bronorganisatie"], "000000000")

    def test_filter_externe_identificatie(self):
        VerzoekFactory.create(externe_identificatie="000000000")
        VerzoekFactory.create(externe_identificatie="123456782")
        url = reverse(Verzoek)

        response = self.client.get(url, {"externe_identificatie": "000000000"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 1)

        result = response_data["results"][0]
        self.assertEqual(result["externeIdentificatie"], "000000000")

    def test_filter_registratiedatum(self):
        VerzoekFactory.create(registratiedatum=make_aware(datetime(2019, 1, 1)))
        VerzoekFactory.create(registratiedatum=make_aware(datetime(2020, 1, 1)))
        url = reverse(Verzoek)

        response = self.client.get(url, {"registratiedatum": "2020-01-01T00:00:00Z"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 1)

        result = response_data["results"][0]
        self.assertEqual(result["registratiedatum"], "2020-01-01T00:00:00Z")

    def test_filter_registratiedatum__gt(self):
        VerzoekFactory.create(registratiedatum=make_aware(datetime(2019, 1, 1)))
        VerzoekFactory.create(registratiedatum=make_aware(datetime(2020, 1, 1)))
        url = reverse(Verzoek)

        response = self.client.get(
            url, {"registratiedatum__gt": "2019-01-01T00:00:00Z"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 1)

        result = response_data["results"][0]
        self.assertEqual(result["registratiedatum"], "2020-01-01T00:00:00Z")

    def test_filter_registratiedatum__gte(self):
        VerzoekFactory.create(registratiedatum=make_aware(datetime(2019, 1, 1)))
        VerzoekFactory.create(registratiedatum=make_aware(datetime(2020, 1, 1)))
        url = reverse(Verzoek)

        response = self.client.get(
            url, {"registratiedatum__gte": "2020-01-01T00:00:00Z"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 1)

        result = response_data["results"][0]
        self.assertEqual(result["registratiedatum"], "2020-01-01T00:00:00Z")

    def test_filter_registratiedatum__lt(self):
        VerzoekFactory.create(registratiedatum=make_aware(datetime(2019, 1, 1)))
        VerzoekFactory.create(registratiedatum=make_aware(datetime(2020, 1, 1)))
        url = reverse(Verzoek)

        response = self.client.get(
            url, {"registratiedatum__lt": "2020-01-01T00:00:00Z"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 1)

        result = response_data["results"][0]
        self.assertEqual(result["registratiedatum"], "2019-01-01T00:00:00Z")

    def test_filter_registratiedatum__lte(self):
        VerzoekFactory.create(registratiedatum=make_aware(datetime(2019, 1, 1)))
        VerzoekFactory.create(registratiedatum=make_aware(datetime(2020, 1, 1)))
        url = reverse(Verzoek)

        response = self.client.get(
            url, {"registratiedatum__lte": "2019-01-01T00:00:00Z"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 1)

        result = response_data["results"][0]
        self.assertEqual(result["registratiedatum"], "2019-01-01T00:00:00Z")

    def test_filter_voorkeurskanaal(self):
        VerzoekFactory.create(voorkeurskanaal="kanaal1")
        VerzoekFactory.create(voorkeurskanaal="kanaal2")
        url = reverse(Verzoek)

        response = self.client.get(url, {"voorkeurskanaal": "kanaal2"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 1)

        result = response_data["results"][0]
        self.assertEqual(result["voorkeurskanaal"], "kanaal2")

    def test_filter_tekst(self):
        VerzoekFactory.create(tekst="sometext1")
        VerzoekFactory.create(tekst="sometext2")
        url = reverse(Verzoek)

        response = self.client.get(url, {"tekst": "sometext2"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 1)

        result = response_data["results"][0]
        self.assertEqual(result["tekst"], "sometext2")

    def test_filter_status(self):
        VerzoekFactory.create(status=VerzoekStatus.afgehandeld)
        VerzoekFactory.create(status=VerzoekStatus.afgewezen)
        url = reverse(Verzoek)

        response = self.client.get(url, {"status": VerzoekStatus.afgewezen})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 1)

        result = response_data["results"][0]
        self.assertEqual(result["status"], VerzoekStatus.afgewezen)

    def test_filter_in_te_trekken_verzoek(self):
        verzoek1, verzoek2 = VerzoekFactory.create_batch(2)
        VerzoekFactory.create(in_te_trekken_verzoek=verzoek1)
        verzoek3 = VerzoekFactory.create(in_te_trekken_verzoek=verzoek2)
        url = reverse(Verzoek)

        response = self.client.get(
            url,
            {"in_te_trekken_verzoek": f"http://testserver.com{reverse(verzoek2)}"},
            HTTP_HOST="testserver.com",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 1)

        result = response_data["results"][0]
        self.assertEqual(result["url"], f"http://testserver.com{reverse(verzoek3)}")
        self.assertEqual(
            result["inTeTrekkenVerzoek"], f"http://testserver.com{reverse(verzoek2)}"
        )

    def test_filter_intrekkende_verzoek(self):
        verzoek1, verzoek2 = VerzoekFactory.create_batch(2)
        VerzoekFactory.create(in_te_trekken_verzoek=verzoek1)
        verzoek3 = VerzoekFactory.create(in_te_trekken_verzoek=verzoek2)
        url = reverse(Verzoek)

        response = self.client.get(
            url,
            {"intrekkende_verzoek": f"http://testserver.com{reverse(verzoek3)}"},
            HTTP_HOST="testserver.com",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 1)

        result = response_data["results"][0]
        self.assertEqual(result["url"], f"http://testserver.com{reverse(verzoek2)}")
        self.assertEqual(
            result["intrekkendeVerzoek"], f"http://testserver.com{reverse(verzoek3)}"
        )

    def test_filter_aangevulde_verzoek(self):
        verzoek1, verzoek2 = VerzoekFactory.create_batch(2)
        VerzoekFactory.create(aangevulde_verzoek=verzoek1)
        verzoek3 = VerzoekFactory.create(aangevulde_verzoek=verzoek2)
        url = reverse(Verzoek)

        response = self.client.get(
            url,
            {"aangevulde_verzoek": f"http://testserver.com{reverse(verzoek2)}"},
            HTTP_HOST="testserver.com",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 1)

        result = response_data["results"][0]
        self.assertEqual(result["url"], f"http://testserver.com{reverse(verzoek3)}")
        self.assertEqual(
            result["aangevuldeVerzoek"], f"http://testserver.com{reverse(verzoek2)}"
        )

    def test_filter_aanvullende_verzoek(self):
        verzoek1, verzoek2 = VerzoekFactory.create_batch(2)
        VerzoekFactory.create(aangevulde_verzoek=verzoek1)
        verzoek3 = VerzoekFactory.create(aangevulde_verzoek=verzoek2)
        url = reverse(Verzoek)

        response = self.client.get(
            url,
            {"aanvullende_verzoek": f"http://testserver.com{reverse(verzoek3)}"},
            HTTP_HOST="testserver.com",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data["count"], 1)

        result = response_data["results"][0]
        self.assertEqual(result["url"], f"http://testserver.com{reverse(verzoek2)}")
        self.assertEqual(
            result["aanvullendeVerzoek"], f"http://testserver.com{reverse(verzoek3)}"
        )
