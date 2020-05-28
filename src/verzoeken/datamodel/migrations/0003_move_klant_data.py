from django.db import migrations


def copy_to_klantverzoek(apps, schema_editor):
    Verzoek = apps.get_model("datamodel", "Verzoek")
    KlantVerzoek = apps.get_model("datamodel", "KlantVerzoek")

    relaties = []
    for verzoek in Verzoek.objects.filter(klant__isnull=False):
        relaties.append(KlantVerzoek(verzoek=verzoek, klant=verzoek.klant))

    KlantVerzoek.objects.bulk_create(relaties)


def copy_from_klantverzoek(apps, schema_editor):
    KlantVerzoek = apps.get_model("datamodel", "KlantVerzoek")

    for klantverzoek in KlantVerzoek.objects.all():
        klantverzoek.verzoek.klant = klantverzoek.klant
        klantverzoek.verzoek.save()


class Migration(migrations.Migration):

    dependencies = [("datamodel", "0002_auto_20200528_1306")]

    operations = [migrations.RunPython(copy_to_klantverzoek, copy_from_klantverzoek)]
