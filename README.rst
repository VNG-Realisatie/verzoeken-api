=============
Verzoeken API
=============

:Version: master
:Source: https://github.com/VNG-Realisatie/verzoeken-api
:Keywords: zaken, zaakgericht werken, GEMMA

Introductie
===========

API voor opslag en ontsluiting van verzoeken en daarbij behorende metadata.

De API ondersteunt het opslaan en het naar andere applicaties ontsluiten van gegevens over verzoeken.

API specificaties
=================

|lint-oas| |generate-sdks| |generate-postman-collection|

==========  ==============  ====================================================================================================================================================================================================  =======================================================================================================================  =================================================================================================================================
Versie      Release datum   API specificatie                                                                                                                                                                                      Autorisaties                                                                                                             Notificaties
==========  ==============  ====================================================================================================================================================================================================  =======================================================================================================================  =================================================================================================================================
master      n.v.t.          `ReDoc <https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/VNG-Realisatie/verzoeken-api/master/src/openapi.yaml>`_,                                                               `Scopes <https://github.com/VNG-Realisatie/verzoeken-api/blob/master/src/autorisaties.md>`_                              `Berichtkenmerken <https://github.com/VNG-Realisatie/verzoeken-api/blob/master/src/notificaties.md>`_
                            `Swagger <https://petstore.swagger.io/?url=https://raw.githubusercontent.com/VNG-Realisatie/verzoeken-api/master/src/openapi.yaml>`_
==========  ==============  ====================================================================================================================================================================================================  =======================================================================================================================  =================================================================================================================================

Zie ook: `Alle versies en wijzigingen <https://github.com/VNG-Realisatie/verzoeken-api/blob/master/CHANGELOG.rst>`_

Ondersteuning
-------------

==========  ==============  ==========================  =================
Versie      Release datum   Einddatum ondersteuning     Documentatie
==========  ==============  ==========================  =================
==========  ==============  ==========================  =================

Referentie implementatie
========================

|build-status| |coverage| |docker| |black| |python-versions|

Referentieimplementatie van de Verzoeken API. Ook wel
verzoekregistratiecomponent (VRC) genoemd.

Ontwikkeld door `Maykin Media B.V. <https://www.maykinmedia.nl>`_ in opdracht
van VNG Realisatie.

Deze referentieimplementatie toont aan dat de API specificatie voor de
Zaken API implementeerbaar is, en vormt een voorbeeld voor andere
implementaties indien ergens twijfel bestaat.

Deze component heeft ook een `demo omgeving`_ waar leveranciers tegenaan kunnen
testen.

Links
=====

* Deze API is onderdeel van de `VNG standaard "API's voor Zaakgericht werken" <https://github.com/VNG-Realisatie/gemma-zaken>`_.
* Lees de `functionele specificatie <https://vng-realisatie.github.io/gemma-zaken/standaard/verzoeken/index>`_ bij de API specificatie.
* Bekijk de `demo omgeving`_ met de laatst gepubliceerde versie.
* Bekijk de `test omgeving <https://zaken-api.test.vng.cloud/>`_ met de laatste ontwikkel versie.
* Rapporteer `issues <https://github.com/VNG-Realisatie/gemma-zaken/issues>`_ bij vragen, fouten of wensen.
* Bekijk de `code <https://github.com/VNG-Realisatie/verzoeken-api/>`_ van de referentie implementatie.

.. _`demo omgeving`: https://zaken-api.vng.cloud/

Licentie
========

Copyright © VNG Realisatie 2018 - 2020

Licensed under the EUPL_

.. _EUPL: LICENCE.md

.. |build-status| image:: https://travis-ci.com/VNG-Realisatie/verzoeken-api.svg?branch=master
    :alt: Build status
    :target: https://travis-ci.com/VNG-Realisatie/verzoeken-api

.. |requirements| image:: https://requires.io/github/VNG-Realisatie/verzoeken-api/requirements.svg?branch=master
     :target: https://requires.io/github/VNG-Realisatie/verzoeken-api/requirements/?branch=master
     :alt: Requirements status

.. |coverage| image:: https://codecov.io/github/VNG-Realisatie/verzoeken-api/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage
    :target: https://codecov.io/gh/VNG-Realisatie/verzoeken-api

.. |docker| image:: https://img.shields.io/badge/docker-latest-blue.svg
    :alt: Docker image
    :target: https://hub.docker.com/r/vngr/verzoeken-api/

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :alt: Code style
    :target: https://github.com/psf/black

.. |python-versions| image:: https://img.shields.io/badge/python-3.7%2B-blue.svg
    :alt: Supported Python version
    :target: https://hub.docker.com/r/vngr/verzoeken-api/

.. |lint-oas| image:: https://github.com/VNG-Realisatie/verzoeken-api/workflows/lint-oas/badge.svg
    :alt: Lint OAS
    :target: https://github.com/VNG-Realisatie/verzoeken-api/actions?query=workflow%3Alint-oas

.. |generate-sdks| image:: https://github.com/VNG-Realisatie/verzoeken-api/workflows/generate-sdks/badge.svg
    :alt: Generate SDKs
    :target: https://github.com/VNG-Realisatie/verzoeken-api/actions?query=workflow%3Agenerate-sdks

.. |generate-postman-collection| image:: https://github.com/VNG-Realisatie/verzoeken-api/workflows/generate-postman-collection/badge.svg
    :alt: Generate Postman collection
    :target: https://github.com/VNG-Realisatie/verzoeken-api/actions?query=workflow%3Agenerate-postman-collection
