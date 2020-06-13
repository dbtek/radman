from django.db import models, migrations


def apply_migration(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.bulk_create([
        Group(name=u'superadmin'),
        Group(name=u'siteadmin'),
    ])


class Migration(migrations.Migration):

    dependencies = [
        ('stations', '0014_auto_20200610_1814'),
    ]

    operations = [
        migrations.RunPython(apply_migration)
    ]