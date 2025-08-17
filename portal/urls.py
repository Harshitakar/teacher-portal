from django.urls import path
from .views import login_view, logout_view, home_view, add_student, update_marks, delete_student

urlpatterns = [
    path("", home_view, name="home"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("students/add/", add_student, name="add_student"),
    path("students/<int:student_id>/update/", update_marks, name="update_marks"),
    path("students/<int:student_id>/delete/", delete_student, name="delete_student"),
]
