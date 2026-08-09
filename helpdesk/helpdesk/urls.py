from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("register/", views.register, name="register"),
    path("tickets/", views.ticket_list, name="ticket_list"),
    path("tickets/create/", views.ticket_create, name="ticket_create"),
    path("tickets/<int:pk>/", views.ticket_detail, name="ticket_detail"),
    path("tickets/<int:pk>/assign/", views.ticket_assign, name="ticket_assign"),
    path("tickets/<int:pk>/status/", views.ticket_status_update, name="ticket_status_update"),
    path("tickets/<int:pk>/close/", views.close_ticket, name="close_ticket"),
    path("tickets/<int:pk>/reopen/", views.reopen_ticket, name="reopen_ticket"),
    path("categories/", views.category_list, name="category_list"),
    path("categories/create/", views.category_create, name="category_create"),
    path("notifications/", views.notifications, name="notifications"),
]
