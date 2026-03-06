from django.db import migrations


def create_missing_header_tables(apps, schema_editor):
    connection = schema_editor.connection
    existing_tables = set(connection.introspection.table_names())

    site_header = apps.get_model("core", "SiteHeader")
    header_menu_link = apps.get_model("core", "HeaderMenuLink")

    if site_header._meta.db_table not in existing_tables:
        schema_editor.create_model(site_header)
        existing_tables.add(site_header._meta.db_table)

    if header_menu_link._meta.db_table not in existing_tables:
        schema_editor.create_model(header_menu_link)


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_missing_header_tables, migrations.RunPython.noop),
    ]
