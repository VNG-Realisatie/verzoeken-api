# Resources

Dit document beschrijft de (RGBZ-)objecttypen die als resources ontsloten
worden met de beschikbare attributen.


## ObjectVerzoek

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/objectverzoek)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| url | URL-referentie naar dit object. Dit is de unieke identificatie en locatie van dit object. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| verzoek | URL-referentie naar het VERZOEK. | string | ja | C​R​U​D |
| object | URL-referentie naar het gerelateerde OBJECT (in een andere API). | string | ja | C​R​U​D |
| objectType | Het type van het gerelateerde OBJECT.

Uitleg bij mogelijke waarden:

* `zaak` - Zaak | string | ja | C​R​U​D |

## VerzoekContactMoment

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/verzoekcontactmoment)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| url | URL-referentie naar dit object. Dit is de unieke identificatie en locatie van dit object. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| contactmoment | URL-referentie naar een CONTACTMOMENT (in Contactmoment API) | string | ja | C​R​U​D |
| verzoek | URL-referentie naar het VERZOEK. | string | ja | C​R​U​D |

## Verzoek

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/verzoek)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| url | URL-referentie naar dit object. Dit is de unieke identificatie en locatie van dit object. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| identificatie | De unieke identificatie van het VERZOEK binnen de organisatie die verantwoordelijk is voor de behandeling van het VERZOEK. | string | nee | C​R​U​D |
| bronorganisatie | Het RSIN van de Niet-natuurlijk persoon zijnde de organisatie die de klantinteractie heeft gecreeerd. Dit moet een geldig RSIN zijn van 9 nummers en voldoen aan https://nl.wikipedia.org/wiki/Burgerservicenummer#11-proef | string | ja | C​R​U​D |
| externeIdentificatie | De identificatie van het VERZOEK buiten de eigen organisatie. | string | nee | C​R​U​D |
| klant | URL-referentie naar een KLANT (in Klanten API) | string | nee | C​R​U​D |
| interactiedatum | De datum en het tijdstip waarop de klantinteractie heeft plaatsgevonden. | string | nee | C​R​U​D |
| voorkeurskanaal | Het communicatiekanaal dat voor opvolging van de klantinteractie de voorkeur heeft van de KLANT. | string | nee | C​R​U​D |
| tekst | Een toelichting die inhoudelijk de klantinteractie van de klant beschrijft. | string | nee | C​R​U​D |
| status | De waarden van de typering van de voortgang van afhandeling van een VERZOEK.

Uitleg bij mogelijke waarden:

* `ontvangen` - (Ontvangen) Het verzoek is ingediend en door de organisatie ontvangen.
* `in_behandeling` - (In behandeling) Het is verzoek is in behandeling.
* `afgehandeld` - (Afgehandeld) Het verzoek zelf is afgehandeld. Eventuele vervolg acties, zoals zaken die voortkomen uit het verzoek, hebben een eigen status.
* `afgewezen` - (Afgewezen) Het verzoek is afgewezen zonder vervolg acties.
* `ingetrokken` - (Ingetrokken) De indiener heeft het verzoek ingetrokken. | string | ja | C​R​U​D |

## VerzoekInformatieObject

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/verzoekinformatieobject)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| url | URL-referentie naar dit object. Dit is de unieke identificatie en locatie van dit object. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| informatieobject | URL-referentie naar het INFORMATIEOBJECT (in de Documenten API) waarin (een deel van) het verzoek beschreven is of aanvullende informatie biedt bij het VERZOEK. | string | ja | C​R​U​D |
| verzoek | URL-referentie naar het VERZOEK. | string | ja | C​R​U​D |

## VerzoekProduct

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/verzoekproduct)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| url | URL-referentie naar dit object. Dit is de unieke identificatie en locatie van dit object. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| verzoek | URL-referentie naar het VERZOEK. | string | ja | C​R​U​D |
| product | URL-referentie naar het PRODUCT (in de Producten en Diensten API). | string | nee | C​R​U​D |


* Create, Read, Update, Delete
