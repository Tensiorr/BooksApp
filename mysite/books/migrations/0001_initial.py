from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100, null=True)),
                ('author', models.CharField(max_length=200, null=True)),
                ('publication_date', models.CharField(max_length=50, null=True)),
                ('isbn', models.CharField(max_length=100, unique=True)),
                ('pages', models.IntegerField(null=True)),
                ('cover', models.CharField(max_length=500, null=True)),
                ('language', models.CharField(max_length=3, null=True)),
            ],
        ),
    ]
