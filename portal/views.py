from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.db import transaction
import uuid

from .models import Teacher, Student, AuditLog
from .utils import (
    hash_password, verify_password, require_login, require_csrf, calculate_new_marks
)
from .middleware import SESSIONS, CSRF_TOKENS

@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == "GET":
        if request.teacher:
            return redirect("home")
        return render(request, "login.html")

    username = (request.POST.get("username") or "").strip()
    password = request.POST.get("password") or ""

    try:
        t = Teacher.objects.get(username=username)
    except Teacher.DoesNotExist:
        return render(request, "login.html", {"error": "Invalid credentials"})

    if verify_password(password, t.salt, t.password_hash):
        session_token = uuid.uuid4().hex
        SESSIONS[session_token] = t.id
        CSRF_TOKENS[session_token] = uuid.uuid4().hex
        resp = redirect("home")
        resp.set_cookie(
            "session_token", session_token,
            httponly=True, secure=False, samesite="Strict"
        )
        resp.set_cookie("csrf_token", CSRF_TOKENS[session_token],
                        httponly=False, secure=False, samesite="Strict")
        return resp

    return render(request, "login.html", {"error": "Invalid credentials"})

def logout_view(request):
    tok = request.COOKIES.get("session_token")
    if tok in SESSIONS:
        del SESSIONS[tok]
    if tok in CSRF_TOKENS:
        del CSRF_TOKENS[tok]
    resp = redirect("login")
    resp.delete_cookie("session_token")
    resp.delete_cookie("csrf_token")
    return resp

@require_login
def home_view(request):
    students = Student.objects.order_by("name", "subject").all()
    return render(request, "home.html", {"students": students, "teacher": request.teacher})

@require_http_methods(["POST"])
@require_login
@require_csrf
def add_student(request):
    name = (request.POST.get("name") or "").strip()
    subject = (request.POST.get("subject") or "").strip()
    marks_raw = request.POST.get("marks") or ""

    # server-side validation
    if not name or not subject:
        return JsonResponse({"error": "Name and subject are required"}, status=400)
    try:
        marks = int(marks_raw)
    except ValueError:
        return JsonResponse({"error": "Marks must be an integer"}, status=400)
    if marks < 0 or marks > 100:
        return JsonResponse({"error": "Marks must be between 0 and 100"}, status=400)

    with transaction.atomic():
        existing = Student.objects.select_for_update().filter(name=name, subject=subject).first()
        if existing:
            new_marks = calculate_new_marks(existing.marks, marks)
            if new_marks > 100:
                return JsonResponse({"error": "Total marks cannot exceed 100"}, status=400)
            # log + update
            AuditLog.objects.create(
                student=existing, updated_by=request.teacher.username,
                old_marks=existing.marks, new_marks=new_marks
            )
            existing.marks = new_marks
            existing.save()
        else:
            Student.objects.create(name=name, subject=subject, marks=marks)

    return JsonResponse({"success": True})

@require_http_methods(["POST"])
@require_login
@require_csrf
def update_marks(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    marks_raw = request.POST.get("marks") or ""
    try:
        new_marks = int(marks_raw)
    except ValueError:
        return JsonResponse({"error": "Marks must be an integer"}, status=400)
    if new_marks < 0 or new_marks > 100:
        return JsonResponse({"error": "Marks must be between 0 and 100"}, status=400)

    old = student.marks
    if old == new_marks:
        return JsonResponse({"success": True})  # no-op

    with transaction.atomic():
        AuditLog.objects.create(
            student=student,
            updated_by=request.teacher.username,
            old_marks=old,
            new_marks=new_marks,
        )
        student.marks = new_marks
        student.save()

    return JsonResponse({"success": True})

@require_http_methods(["POST"])
@require_login
@require_csrf
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    return JsonResponse({"success": True})
