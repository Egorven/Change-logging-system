from django.urls import path
from . import views

app_name = "changes"

urlpatterns = [
    path("", views.changes, name="changes"),
    path("create/", views.change_create, name="change_create"),
    path("<int:change_id>/", views.change_detail, name="change_detail"),
    path("<int:change_id>/edit/", views.change_edit, name="change_edit"),
    path("<int:change_id>/cancel/", views.change_cancel, name="change_cancel"),
]
