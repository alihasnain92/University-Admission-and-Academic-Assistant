# backend/admission_assistant/models.py

from django.db import models
import uuid

class IntentCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    keywords = models.TextField(help_text="Comma-separated keywords")

    class Meta:
        verbose_name = "Intent Category"
        verbose_name_plural = "Intent Categories"

    def __str__(self):
        return self.name

class Response(models.Model):
    category = models.ForeignKey(IntentCategory, on_delete=models.CASCADE, related_name='responses')
    response_text = models.TextField()
    priority = models.IntegerField(default=1)

    class Meta:
        ordering = ['-priority']

    def __str__(self):
        return f"{self.category.name} - Response"

class Admission(models.Model):
    ADMISSION_STATUS = (
        ('pending', 'Pending'),
        ('reviewing', 'Under Review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    )
    
    admission_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    program = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=ADMISSION_STATUS, default='pending')
    entry_test_unlocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.admission_code}"

class Document(models.Model):
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=50)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.admission.admission_code} - {self.document_type}"

class Payment(models.Model):
    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    )

    admission = models.ForeignKey(Admission, on_delete=models.CASCADE, related_name='payments')
    payment_type = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.admission.admission_code} - {self.payment_type}"

class Guardian(models.Model):
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE, related_name='guardians')
    name = models.CharField(max_length=200)
    relation = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    occupation = models.CharField(max_length=100)
    income = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.admission.first_name}'s {self.relation}"

class EntryTest(models.Model):
    admission = models.OneToOneField(Admission, on_delete=models.CASCADE, related_name='entry_test')
    test_date = models.DateTimeField(null=True, blank=True)
    venue = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=20, default='scheduled')
    score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.admission.admission_code} - Entry Test"