"""
Defines the scopes used in the CMC component.
"""

from vng_api_common.scopes import Scope

SCOPE_VERZOEKEN_ALLES_VERWIJDEREN = Scope(
    "verzoeken.verwijderen",
    description="""
**Laat toe om**:

* verzoeken te verwijderen
""",
)

SCOPE_VERZOEKEN_ALLES_LEZEN = Scope(
    "verzoeken.lezen",
    description="""
**Laat toe om**:

* verzoeken te lezen
* verzoekdetails op te vragen
""",
)

SCOPE_VERZOEKEN_BIJWERKEN = Scope(
    "verzoeken.bijwerken",
    description="""
**Laat toe om**:

* attributen van een verzoek te wijzingen
""",
)

SCOPE_VERZOEKEN_AANMAKEN = Scope(
    "verzoeken.aanmaken",
    description="""
**Laat toe om**:

* verzoeken aan te maken
""",
)
