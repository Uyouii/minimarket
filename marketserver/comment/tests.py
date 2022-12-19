import logging
from django.test import TestCase
import comment
from comment import conf

# Create your tests here.
class AuthTests(TestCase):

    def test_gen_comment_id(self):
        product_id = 101
        comment_id = comment.GenCommentId(product_id)
        self.assertEqual(comment_id & 0x3f, 
            product_id % conf.COMMENT_TABLE_COUNT)
    
    def test_get_comment_id(self):
        pass
