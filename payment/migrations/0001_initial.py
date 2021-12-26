# Generated by Django 3.2.6 on 2021-08-30 07:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tid', models.CharField(default='0', max_length=128)),
                ('check', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('c_name', models.CharField(max_length=20)),
                ('c_code', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('location', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CompanyAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ca_id', models.CharField(max_length=11)),
                ('ca_password', models.CharField(max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('m_name', models.CharField(max_length=20)),
                ('m_id', models.CharField(max_length=11, primary_key=True, serialize=False)),
                ('m_password', models.CharField(max_length=11)),
                ('m_number', models.CharField(max_length=11)),
                ('mail', models.EmailField(max_length=128)),
                ('m_point', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Pay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=None, null=True)),
                ('total', models.IntegerField()),
                ('c_code', models.ForeignKey(db_column='c_code', on_delete=django.db.models.deletion.CASCADE, to='payment.company')),
                ('m_id', models.ForeignKey(db_column='m_id', on_delete=django.db.models.deletion.CASCADE, to='payment.member')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('p_code', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('p_name', models.CharField(max_length=20)),
                ('price', models.IntegerField(default=0)),
                ('image_path', models.CharField(max_length=200)),
                ('p_desc', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='PayItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cnt', models.IntegerField()),
                ('opt', models.BooleanField(default=False)),
                ('p_code', models.ForeignKey(db_column='p_code', on_delete=django.db.models.deletion.CASCADE, to='payment.product')),
                ('pay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.pay')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cnt', models.IntegerField()),
                ('opt', models.BooleanField(default=False)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.cart')),
                ('p_code', models.ForeignKey(db_column='p_code', on_delete=django.db.models.deletion.CASCADE, to='payment.product')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='c_code',
            field=models.ForeignKey(db_column='c_code', on_delete=django.db.models.deletion.CASCADE, to='payment.company'),
        ),
        migrations.AddField(
            model_name='cart',
            name='m_id',
            field=models.ForeignKey(db_column='m_id', on_delete=django.db.models.deletion.CASCADE, to='payment.member'),
        ),
    ]
