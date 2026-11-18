from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("changes", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="change",
            name="attachment",
            field=models.FileField(
                blank=True,
                upload_to="changes/%Y/%m/",
                verbose_name="Вложение",
            ),
        ),
        migrations.AddField(
            model_name="change",
            name="status",
            field=models.CharField(
                choices=[("active", "Активно"), ("cancelled", "Отменено")],
                default="active",
                editable=False,
                max_length=20,
                verbose_name="Статус",
            ),
        ),
    ]
