# Generated migration

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_user_plain_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedfile',
            name='document_type',
            field=models.CharField(blank=True, choices=[('expense_bill', 'Expense Bill'), ('cheque', 'Cheque'), ('purchase_bill', 'Purchase Bill'), ('legal_document', 'Legal Document'), ('other_bill', 'Other Bill')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='uploadedfile',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
    ]
