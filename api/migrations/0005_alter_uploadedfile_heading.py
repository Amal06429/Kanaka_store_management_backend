# Generated migration

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_uploadedfile_document_type_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedfile',
            name='heading',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
