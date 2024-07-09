from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.user_login),
    path('home', views.home),
    path('signout', views.signout),
    path('customer', views.customer),

    path('dashboard/', views.dashboard),
    path('users/', views.users, name='users'),
    path('products/', views.products),
    path('categories/', views.categories),
    path('suppliers/', views.suppliers),
    path('orders/', views.orders),


    path('customerrecord/<int:page>', views.customerrecord),
    path('order/<int:id>', views.order),

    path('records/<int:page>', views.records),
    path('adduser/', views.adduser, name='adduser'),
    path('deleteuser/<int:id>', views.deleteuser, name='deleteuser'),
    
    path('productsrecord/<int:page>', views.productsrecord),
    path('addproduct/', views.addproduct, name='addproduct'),
    path('deleteproduct/<int:id>', views.deleteproduct, name='deleteproduct'),
    path('editproduct/<int:id>', views.editproduct, name='editproduct'),
    path('editproduct/updateproduct/<int:id>', views.updateproduct, name='editproduct'),

    path('categoryrecord/<int:page>', views.categoryrecord),
    path('addcategory/', views.addcategory, name='addcategory'),
    path('deletecategory/<int:id>', views.deletecategory, name='deletecategory'),

    path('suppliersrecord/<int:page>', views.suppliersrecord),
    path('addsuppliers/', views.addsuppliers, name='addsuppliers'),
    path('deletesuppliers/<int:id>', views.deletesuppliers, name='deletesuppliers'),
    path('editsuppliers/<int:id>', views.editsuppliers, name='editsuppliers'),
    path('editsuppliers/updatesuppliers/<int:id>', views.updatesuppliers, name='editsuppliers'),


]