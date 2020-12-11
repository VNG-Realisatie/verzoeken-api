## Notificaties
## Berichtkenmerken voor verzoeken API

Kanalen worden typisch per component gedefinieerd. Producers versturen berichten op bepaalde kanalen,
consumers ontvangen deze. Consumers abonneren zich via een notificatiecomponent (zoals <a href="https://notificaties-api.vng.cloud/api/v1/schema/" rel="nofollow">https://notificaties-api.vng.cloud/api/v1/schema/</a>) op berichten.

Hieronder staan de kanalen beschreven die door deze component gebruikt worden, met de kenmerken bij elk bericht.

De architectuur van de notificaties staat beschreven op <a href="https://github.com/VNG-Realisatie/notificaties-api" rel="nofollow">https://github.com/VNG-Realisatie/notificaties-api</a>.


### verzoeken

**Kanaal**
`verzoeken`

**Main resource**

`verzoek`



**Kenmerken**

* `bronorganisatie`: Het RSIN van de Niet-natuurlijk persoon zijnde de organisatie die de klantinteractie heeft gecreeerd. Dit moet een geldig RSIN zijn van 9 nummers en voldoen aan <a href="https://nl.wikipedia.org/wiki/Burgerservicenummer#11-proef" rel="nofollow">https://nl.wikipedia.org/wiki/Burgerservicenummer#11-proef</a>

**Resources en acties**


* <code>verzoek</code>: create, update, destroy

* <code>verzoekinformatieobject</code>: create, destroy

* <code>verzoekcontactmoment</code>: create, destroy

* <code>verzoekproduct</code>: create, destroy

* <code>klantverzoek</code>: create, destroy


