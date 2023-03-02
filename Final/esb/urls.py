from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("verify/<str:token>", views.verify, name="verify"),
    path("settings", views.settings_view, name="settings"),
    path("category", views.category, name="category"),
    path("pendings", views.pending_page, name="pendings"),
    path("inprogess", views.inprogress_page, name="inprogress"),
    path("order/<int:order_id>", views.order_page, name="order_page"),
    path("search_products", views.search_products, name="search_products"),
    # API routes
    path("settings/edit", views.edit_settings, name="edit-settings"),
    path("order/<int:order_id>/refresh",
         views.refresh_order, name="refresh_order")
    # path("categories/<str:category_type>", views.categor, name="categor"),
]
