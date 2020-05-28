from django.test import TestCase, override_settings

from zds_client.tests.mocks import mock_client

from verzoeken.tests.mixins import VerzoekInformatieObjectSyncMixin

from .factories import (
    VerzoekContactMomentFactory,
    VerzoekFactory,
    VerzoekInformatieObjectFactory,
    VerzoekProductFactory,
)


class UniqueRepresentationTests(VerzoekInformatieObjectSyncMixin, TestCase):
    def test_verzoek(self):
        verzoek = VerzoekFactory.create(
            bronorganisatie="154760924", identificatie="12345"
        )

        self.assertEqual(verzoek.unique_representation(), "154760924 - 12345")

    def test_verzoekproduct(self):
        verzoek_product = VerzoekProductFactory.create(
            verzoek__bronorganisatie="154760924",
            verzoek__identificatie="12345",
            product="http://some.products.nl/products/111",
        )

        self.assertEqual(
            verzoek_product.unique_representation(), "(154760924 - 12345) - 111"
        )

    @override_settings(ZDS_CLIENT_CLASS="vng_api_common.mocks.MockClient")
    def test_verzoekinformatieobject(self):
        vio = VerzoekInformatieObjectFactory.create(
            verzoek__bronorganisatie="154760924", verzoek__identificatie="12345",
        )
        responses = {
            vio.informatieobject: {
                "url": vio.informatieobject,
                "identificatie": "12345",
            }
        }
        with mock_client(responses):
            unique_representation = vio.unique_representation()

        self.assertEqual(unique_representation, "(154760924 - 12345) - 12345")

    def test_verzoekcontactmoment(self):
        verzoek_contactmoment = VerzoekContactMomentFactory.create(
            verzoek__bronorganisatie="154760924",
            verzoek__identificatie="12345",
            contactmoment="http://some.contactmomenten.nl/api/v1/contactmomenten/222",
        )

        self.assertEqual(
            verzoek_contactmoment.unique_representation(), "(154760924 - 12345) - 222"
        )
