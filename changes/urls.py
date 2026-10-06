from django.urls import path
from . import views

app_name = "changes"

urlpatterns = [
    path("", views.changes, name="changes"),
    path("<int:change_id>/", views.change_detail, name="change_detail"),
]
