from datetime import datetime

from django.utils.timezone import make_aware

from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import JWTAuthMixin, reverse

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
        self.assertEqual(len(data), 2)

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
