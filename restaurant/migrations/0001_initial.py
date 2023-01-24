# Generated by Django 3.2.16 on 2023-01-24 16:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('aid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('firstaddress', models.CharField(max_length=100)),
                ('street', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('zip_code', models.CharField(max_length=10)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('cid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='category/photos/')),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, unique=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Modifier',
            fields=[
                ('mid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, unique=True)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ModifierGroup',
            fields=[
                ('mgid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, unique=True)),
                ('modifiers', models.ManyToManyField(blank=True, null=True, related_name='groups', to='restaurant.Modifier')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('slug', models.CharField(blank=True, max_length=250, null=True, unique=True)),
                ('lid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurant.address')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('pid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, unique=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='product/photos/')),
                ('category', models.ManyToManyField(blank=True, null=True, to='restaurant.Category')),
                ('location', models.ManyToManyField(blank=True, null=True, related_name='location', to='restaurant.Restaurant')),
                ('modifier_groups', models.ManyToManyField(blank=True, null=True, related_name='products', to='restaurant.ModifierGroup')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=250, null=True)),
                ('category', models.ManyToManyField(blank=True, null=True, to='restaurant.Category')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ManyToManyField(blank=True, null=True, to='restaurant.Product')),
                ('restaurant', models.ManyToManyField(blank=True, null=True, to='restaurant.Restaurant')),
            ],
        ),
    ]
