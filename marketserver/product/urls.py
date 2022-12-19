from django.conf.urls import patterns, url

import product

urlpatterns = patterns(
    '',
    url(r'^id/(?P<product_id>\d+)/$',
        product.getProductByIdApi, name='getproductbyid'),
    url(r'^all/', product.getAllProductApi, name='getAllProduct'),
    url(r'^searchname/', product.searchProductByNameApi, name='searchProductByNameApi'),
    url(r'^searchcate/', product.searchProductByCateApi, name='searchProductByCateApi'),
    url(r'^add/', product.addProductApi, name='addProductApi'),
)
