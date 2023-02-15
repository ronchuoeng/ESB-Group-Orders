from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("verify/<str:token>", views.verify, name="verify"),
    path("settings", views.settings_view, name="settings"),
    path("pending", views.pending_page, name="pending"),
    # API routes
    path("settings/edit", views.edit_settings, name="edit-settings"),
]
