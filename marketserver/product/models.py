from copy import deepcopy
import json
from django.db import models

from django.db.models.base import ModelBase
from common import conf


class Product(models.Model):

    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=128)
    cate = models.CharField(max_length=32)
    create_time = models.BigIntegerField()
    update_time = models.BigIntegerField()
    descript = models.CharField(max_length=1024)
    photo = models.CharField(max_length=256)

    class Meta:
        db_table = 'product_tab'

    def getDict(self):
        return {
            'id': self.id,
            'name': self.name,
            'cate': self.cate,
            'descript': self.descript,
            'photo': self.photo
        }

    def __unicode__(self):
        return json.dumps(self.getDict())
