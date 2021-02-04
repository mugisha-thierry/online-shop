from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url,include
from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name = 'home'),
    path('category/<category>',views.product_category,name = 'category'),
    path('categorys/<category>',views.products_category,name = 'categorys'),
    path('product_list/',views.product_list,name = 'product_list'),
    path('signup/',views.signup , name='signup'),
    path('product/<pk>', views.comment, name='comment'),
    path('profile/<username>/', views.profile, name='profile'),
    path('clear_from_cart/',views.clear_from_cart,name='clear_from_cart'),
    path('admin_page',views.admin_page,name='admin_page'),
    path('search',views.search_product,name = 'search_product'),
    path('searching',views.search_products,name = 'search_products'),
    path('about/',views.about,name = 'about'),
    url(r'^add-to-cart/(?P<item_id>[-\w]+)/$', views.add_to_cart, name="add_to_cart"),
    url(r'^order-summary/$', views.order_details, name="order_summary"),
    url(r'^item/delete/(?P<item_id>[-\w]+)/$', views.delete_from_cart, name='delete_item'),
    url(r'^checkout/$', views.checkout, name='checkout'),
]