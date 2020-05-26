from django.conf import settings

from vng_api_common.notifications.kanalen import Kanaal

from verzoeken.datamodel.models import Verzoek

KANAAL_VERZOEKEN = Kanaal(
    settings.NOTIFICATIONS_KANAAL,
    main_resource=Verzoek,
    kenmerken=("bronorganisatie",),
)
