"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),

    path('admin_login', views.admin_login, name='admin_login'),
    path('admin_changepassword', views.admin_changepassword, name='admin_changepassword'),
    path('admin_logout', views.admin_logout, name='admin_logout'),
    path('admin_home', views.admin_home, name='admin_home'),

    path('admin_view_castingteam_new', views.admin_view_castingteam_new, name='admin_view_castingteam_new'),
    path('admin_view_castingteam_accepted', views.admin_view_castingteam_accepted, name='admin_view_castingteam_accepted'),
    path('admin_view_castingteam_rejected', views.admin_view_castingteam_rejected, name='admin_view_castingteam_rejected'),
    path('admin_approvals_castingteam', views.admin_approvals_castingteam, name='admin_approvals_castingteam'),

    path('admin_add_prod_master', views.admin_add_prod_master, name='admin_add_prod_master'),
    path('admin_view_prod_master', views.admin_view_prod_master, name='admin_view_prod_master'),
    path('admin_delete_prod_master', views.admin_delete_prod_master, name='admin_delete_prod_master'),
    path('admin_edit_prod_master', views.admin_edit_prod_master, name='admin_edit_prod_master'),

    path('castingteam_reg', views.castingteam_reg, name='castingteam_reg'),
    path('castingteam_login', views.castingteam_login, name='castingteam_login'),
    path('castingteam_logout', views.castingteam_logout, name='castingteam_logout'),
    path('castingteam_home', views.castingteam_home, name='castingteam_home'),
    path('castingteam_update_profile', views.castingteam_update_profile, name='castingteam_update_profile'),
    path('castingteam_changepassword', views.castingteam_changepassword, name='castingteam_changepassword'),
    path('castingteam_forgot_password', views.castingteam_forgot_password, name='castingteam_forgot_password'),

    path('castingteam_prods_add', views.castingteam_prods_add, name='castingteam_prods_add'),
    path('castingteam_prods_view', views.castingteam_prods_view, name='castingteam_prods_view'),
    path('castingteam_prods_delete', views.castingteam_prods_delete, name='castingteam_prods_delete'),

    path('castingteam_view_artist', views.castingteam_view_artist, name='castingteam_view_artist'),

    path('casting_call_add', views.casting_call_add, name='casting_call_add'),
    path('casting_call_view', views.casting_call_view, name='casting_call_view'),
    path('casting_call_delete', views.casting_call_delete, name='casting_call_delete'),
    path('casting_call_edit', views.casting_call_edit, name='casting_call_edit'),

    path('castingteam_add_plot', views.castingteam_add_plot, name='castingteam_add_plot'),
    path('castingteam_view_plot', views.castingteam_view_plot, name='castingteam_view_plot'),
    path('castingteam_edit_plot', views.castingteam_edit_plot, name='castingteam_edit_plot'),

    path('casting_application_view', views.casting_application_view, name='casting_application_view'),
    path('castingteam_accept_reject_appl', views.castingteam_accept_reject_appl, name='castingteam_accept_reject_appl'),

    path('artist_reg', views.artist_reg, name='artist_reg'),
    path('artist_login', views.artist_login, name='artist_login'),
    path('artist_logout', views.artist_logout, name='artist_logout'),
    path('artist_home', views.artist_home, name='artist_home'),
    path('artist_details_update', views.artist_details_update, name='artist_details_update'),
    path('artist_photo_update', views.artist_photo_update, name='artist_photo_update'),
    path('artist_changepassword', views.artist_changepassword, name='artist_changepassword'),
    path('artist_forgot_password', views.artist_forgot_password, name='artist_forgot_password'),

    path('artist_view_castingteam', views.artist_view_castingteam, name='artist_view_castingteam'),

    path('artist_casting_call_view', views.artist_casting_call_view, name='artist_casting_call_view'),
    path('artist_casting_search', views.artist_casting_search, name='artist_casting_search'),

    path('artist_view_plot', views.artist_view_plot, name='artist_view_plot'),

    path('artist_casting_application_add', views.artist_casting_application_add, name='artist_casting_application_add'),
    path('artist_casting_application_view', views.artist_casting_application_view, name='artist_casting_application_view'),
    path('artist_casting_application_del', views.artist_casting_application_del, name='artist_casting_application_del'),

]

