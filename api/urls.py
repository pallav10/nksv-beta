from django.conf.urls import url
import views


urlpatterns = [
    url(r'^users/$', views.user_registration),
    url(r'^users/(?P<pk>[0-9]+)/$', views.user_detail),
    url(r'^users/login/$', views.user_login),
    url(r'^users/(?P<pk>[0-9]+)/change_password/$', views.user_change_password),
    url(r'^password_reset/$', views.password_reset),
    url(r'^users/(?P<pk>[0-9]+)/password_reset/done/$', views.password_reset_done),
    url(r'^users/(?P<pk>[0-9]+)/password_reset/confirm/(?P<key>\w+)/$', views.password_reset_confirm),
    url(r'^users/(?P<pk>[0-9]+)/cart/(?P<key>\w+)/$', views.cart),
    url(r'^users/(?P<pk>[0-9]+)/cart/$', views.cart_detail),

    # url(r'^product_categories/$', views.product_categories),
    # url(r'^product_categories/(?P<pk>[0-9]+)/$', views.products),
    # url(r'^products/(?P<pk>[0-9]+)/$', views.product_detail),
    # url(r'^service_categories/$', views.service_categories),
    # url(r'^service_categories/(?P<pk>[0-9]+)/$', views.services),
    # url(r'^services/(?P<pk>[0-9]+)/$', views.product_detail),

    url(r'^categories/$', views.item_categories),
    url(r'^categories/(?P<pk>[0-9]+)/$', views.categories),
    url(r'^categories/(?P<pk>[0-9]+)/items/$', views.items),
    url(r'^articles/$', views.articles),
    url(r'^images/$', views.images),
    url(r'^videos/$', views.videos),
]
