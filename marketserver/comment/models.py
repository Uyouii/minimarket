import json
from django.db import models
from comment import conf


class Comment(models.Model):
    class Meta:
        abstract = True

    id = models.BigIntegerField(primary_key=True)
    product_id = models.BigIntegerField()
    user_id = models.BigIntegerField()
    resp_comment_id = models.BigIntegerField()
    content = models.CharField(max_length=256)
    create_time = models.BigIntegerField()
    update_time = models.BigIntegerField()
    img = models.CharField(max_length=128)

    def getDict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'user_id': self.user_id,
            'content': self.content,
            'create_time': self.create_time,
            'img': self.img
        }

    def __unicode__(self):
        return json.dumps(self.getDict())

    @classmethod
    def getModel(cls, index=0):
        tab_index = index % conf.COMMENT_TABLE_COUNT
        table_name = 'comment_tab_{}'.format(tab_index)
        if table_name in cls._model_dict:
            return cls._model_dict[table_name]

        class Meta:
            db_table = table_name

        attrs = {
            '__module__': cls.__module__,
            'Meta': Meta
        }

        model = type('Comment{}'.format(tab_index), (cls,), attrs)
        cls._model_dict[table_name] = model
        return model

    _model_dict = {}  # help to reuse the model object
