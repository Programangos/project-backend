from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_set_admin_inmortal'),
    ]

    operations = [
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zone_id', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('route', models.CharField(default='/notices', max_length=100)),
                ('bounds_south', models.FloatField()),
                ('bounds_west', models.FloatField()),
                ('bounds_north', models.FloatField()),
                ('bounds_east', models.FloatField()),
            ],
            options={
                'db_table': 'zone',
            },
        ),
    ]
