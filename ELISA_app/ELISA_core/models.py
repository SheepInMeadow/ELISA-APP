from django.db import models


class Plates(models.Model):
    id = models.TextField(db_column='ID', blank=True, primary_key=True)
    name = models.TextField(db_column='Name', blank=True, null=True)
    data = models.TextField(db_column='Data', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plates'
