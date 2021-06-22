# Resources

Dit document beschrijft de (RGBZ-)objecttypen die als resources ontsloten
worden met de beschikbare attributen.


## KlantVerzoek

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/klantverzoek)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| url | URL-referentie naar dit object. Dit is de unieke identificatie en locatie van dit object. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| klant | URL-referentie naar een KLANT (in Klanten API) | string | ja | C​R​U​D |
| verzoek | URL-referentie naar het VERZOEK. | string | ja | C​R​U​D |
| rol | Rol van de KLANT bij het VERZOEK.

Uitleg bij mogelijke waarden:

* `belanghebbende` - Belanghebbende
* `initiator` - Initiator
* `mede_initiator` - Mede-initiator | string | nee | C​R​U​D |
| indicatieMachtiging | Indicatie machtiging

Uitleg bij mogelijke waarden:

* `gemachtigde` - (Gemachtigde) De KLANT is door een andere KLANT gemachtigd om in het VERZOEK namens hem of haar te handelen.
* `machtiginggever` - (Machtiginggever) De KLANT heeft een andere KLANT gemachtigd om in het VERZOEK namens hem of haar te handelen. | string | nee | C​R​U​D |

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
| registratiedatum | De datum en het tijdstip waarop het VERZOEK is geregistreerd. | string | nee | C​R​U​D |
| voorkeurskanaal | Het communicatiekanaal dat voor opvolging van het VERZOEK de voorkeur heeft van de KLANT. | string | nee | C​R​U​D |
| tekst | Een toelichting die inhoudelijk het VERZOEK van de KLANT beschrijft. | string | nee | C​R​U​D |
| status | De waarden van de typering van de voortgang van afhandeling van een VERZOEK.

Uitleg bij mogelijke waarden:

* `ontvangen` - (Ontvangen) Het verzoek is ingediend en door de organisatie ontvangen.
* `in_behandeling` - (In behandeling) Het is verzoek is in behandeling.
* `afgehandeld` - (Afgehandeld) Het verzoek zelf is afgehandeld. Eventuele vervolg acties, zoals zaken die voortkomen uit het verzoek, hebben een eigen status.
* `afgewezen` - (Afgewezen) Het verzoek is afgewezen zonder vervolg acties.
* `ingetrokken` - (Ingetrokken) De indiener heeft het verzoek ingetrokken. | string | ja | C​R​U​D |
| inTeTrekkenVerzoek | URL-referentie naar het (eerdere) VERZOEK dat door dit VERZOEK wordt verzocht ingetrokken te worden. | string | nee | C​R​U​D |
| intrekkendeVerzoek | URL-referentie naar het (latere) VERZOEK waarin verzocht wordt dit VERZOEK in te trekken. Dit veld is alleen leesbaar en wordt automatisch gezet wanneer er een ander VERZOEK wordt aangemaakt dat dit VERZOEK intrekt. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| aangevuldeVerzoek | URL-referentie naar het (eerdere) VERZOEK dat door dit VERZOEK wordt aangevuld. | string | nee | C​R​U​D |
| aanvullendeVerzoek | URL-referentie naar het (latere) VERZOEK waarin dit VERZOEK wordt aangevuld. Dit veld is alleen leesbaar en wordt automatisch gezet indien een ander VERZOEK wordt aangemaakt dat dit VERZOEK aanvult. | string | nee | ~~C~~​R​~~U~~​~~D~~ |

## AuditTrail

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/audittrail)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| uuid | Unieke identificatie van de audit regel. | string | nee | C​R​U​D |
| bron | De naam van het component waar de wijziging in is gedaan.

Uitleg bij mogelijke waarden:

* `ac` - Autorisaties API
* `nrc` - Notificaties API
* `zrc` - Zaken API
* `ztc` - Catalogi API
* `drc` - Documenten API
* `brc` - Besluiten API
* `cmc` - Contactmomenten API
* `kc` - Klanten API | string | ja | C​R​U​D |
| applicatieId | Unieke identificatie van de applicatie, binnen de organisatie. | string | nee | C​R​U​D |
| applicatieWeergave | Vriendelijke naam van de applicatie. | string | nee | C​R​U​D |
| gebruikersId | Unieke identificatie van de gebruiker die binnen de organisatie herleid kan worden naar een persoon. | string | nee | C​R​U​D |
| gebruikersWeergave | Vriendelijke naam van de gebruiker. | string | nee | C​R​U​D |
| actie | De uitgevoerde handeling.

De bekende waardes voor dit veld zijn hieronder aangegeven,                         maar andere waardes zijn ook toegestaan

Uitleg bij mogelijke waarden:

* `create` - Object aangemaakt
* `list` - Lijst van objecten opgehaald
* `retrieve` - Object opgehaald
* `destroy` - Object verwijderd
* `update` - Object bijgewerkt
* `partial_update` - Object deels bijgewerkt | string | ja | C​R​U​D |
| actieWeergave | Vriendelijke naam van de actie. | string | nee | C​R​U​D |
| resultaat | HTTP status code van de API response van de uitgevoerde handeling. | integer | ja | C​R​U​D |
| hoofdObject | De URL naar het hoofdobject van een component. | string | ja | C​R​U​D |
| resource | Het type resource waarop de actie gebeurde. | string | ja | C​R​U​D |
| resourceUrl | De URL naar het object. | string | ja | C​R​U​D |
| toelichting | Toelichting waarom de handeling is uitgevoerd. | string | nee | C​R​U​D |
| resourceWeergave | Vriendelijke identificatie van het object. | string | ja | C​R​U​D |
| aanmaakdatum | De datum waarop de handeling is gedaan. | string | nee | ~~C~~​R​~~U~~​~~D~~ |

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
