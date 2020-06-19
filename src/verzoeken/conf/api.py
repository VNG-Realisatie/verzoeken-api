from vng_api_common.conf.api import *  # noqa - imports white-listed

API_VERSION = "1.0.0-beta"

REST_FRAMEWORK = BASE_REST_FRAMEWORK.copy()

SECURITY_DEFINITION_NAME = "JWT-Claims"

SWAGGER_SETTINGS = BASE_SWAGGER_SETTINGS.copy()

SWAGGER_SETTINGS.update(
    {
        "DEFAULT_INFO": "verzoeken.api.schema.info",
        "SECURITY_DEFINITIONS": {
            SECURITY_DEFINITION_NAME: {
                # OAS 3.0
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                # not official...
                # 'scopes': {},  # TODO: set up registry that's filled in later...
                # Swagger 2.0
                # 'name': 'Authorization',
                # 'in': 'header'
                # 'type': 'apiKey',
            }
        },
        "DEFAULT_FIELD_INSPECTORS": (
            "vng_api_common.inspectors.fields.HyperlinkedIdentityFieldInspector",
            "vng_api_common.inspectors.fields.HyperlinkedRelatedFieldInspector",
        )
        + BASE_SWAGGER_SETTINGS["DEFAULT_FIELD_INSPECTORS"],
    }
)

GEMMA_URL_INFORMATIEMODEL_VERSIE = "1.0"


drc_repo = "vng-realisatie/gemma-documentregistratiecomponent"
drc_commit = "a1602ccf397527add6bc2b4b12e997accf287339"
DRC_API_SPEC = f"https://raw.githubusercontent.com/{drc_repo}/{drc_commit}/src/openapi.yaml"  # noqa

zrc_repo = "vng-realisatie/gemma-zaakregistratiecomponent"
zrc_commit = "8ea1950fe4ec2ad99504d345eba60a175eea3edf"
ZRC_API_SPEC = f"https://raw.githubusercontent.com/{zrc_repo}/{zrc_commit}/src/openapi.yaml"  # noqa
