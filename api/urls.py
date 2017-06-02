from django.conf.urls import url
import views

urlpatterns = [
    url(r'^users/$', views.user_registration),
    url(r'^users/(?P<pk>[0-9]+)/$', views.user_detail),
    url(r'^users/login$', views.user_login),
    url(r'^users/(?P<pk>[0-9]+)/change_password/$', views.user_change_password),
    url(r'^password_reset/$', views.password_reset),
    url(r'^users/(?P<pk>[0-9]+)/password_reset/done/$', views.password_reset_done),
    url(r'^users/(?P<pk>[0-9]+)/password_reset/confirm/(?P<key>\w+)/$', views.password_reset_confirm),
    url(r'^products/$', views.products),
    url(r'^products/(?P<pk>[0-9]+)/$', views.product_detail),
    url(r'^services/$', views.services),
    url(r'^services/(?P<pk>[0-9]+)/$', views.service_detail),
    url(r'^blogs/$', views.blogs),
    url(r'^blogs/(?P<pk>[0-9]+)/$', views.blogs_detail)


]


