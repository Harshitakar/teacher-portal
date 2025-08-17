from django.db import models

class Teacher(models.Model):
    username = models.CharField(max_length=50, unique=True)
    salt = models.CharField(max_length=64)
    password_hash = models.CharField(max_length=128)  # hex of pbkdf2

    def __str__(self):
        return self.username

class Student(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    marks = models.PositiveIntegerField()

    class Meta:
        unique_together = ("name", "subject")

    def __str__(self):
        return f"{self.name} - {self.subject}"

class AuditLog(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="audit_logs")
    updated_by = models.CharField(max_length=50)
    old_marks = models.IntegerField()
    new_marks = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} | {self.updated_by} | {self.timestamp}"
