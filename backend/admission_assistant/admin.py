# backend/admission_assistant/admin.py

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count
from .models import (
    IntentCategory, 
    Response, 
    Admission, 
    Document, 
    Payment, 
    Guardian, 
    EntryTest
)

@admin.register(IntentCategory)
class IntentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'keywords_list', 'response_count')
    search_fields = ('name', 'description', 'keywords')
    
    def keywords_list(self, obj):
        return obj.keywords
    keywords_list.short_description = 'Keywords'
    
    def response_count(self, obj):
        return obj.responses.count()
    response_count.short_description = 'Responses'

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('category', 'short_response', 'priority', 'action_buttons')
    list_filter = ('category', 'priority')
    search_fields = ('response_text', 'category__name')
    ordering = ('category', '-priority')
    
    def short_response(self, obj):
        return format_html('<div style="max-width: 500px; white-space: pre-wrap;">{}</div>', 
            obj.response_text[:100] + '...' if len(obj.response_text) > 100 else obj.response_text)
    short_response.short_description = 'Response Text'
    
    def action_buttons(self, obj):
        return format_html(
            '<a class="button" href="{}"">Edit</a> &nbsp;'
            '<a class="button" style="background: #ba2121;" href="{}">Delete</a>',
            reverse('admin:admission_assistant_response_change', args=[obj.id]),
            reverse('admin:admission_assistant_response_delete', args=[obj.id])
        )
    action_buttons.short_description = 'Actions'
    
    fieldsets = (
        ('Category Information', {
            'fields': ('category',)
        }),
        ('Response Details', {
            'fields': ('response_text', 'priority'),
            'description': 'Enter the response text and set its priority (higher number = higher priority)'
        }),
    )

@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = ('admission_code', 'full_name', 'email', 'program', 'status', 
                   'entry_test_status', 'created_at', 'action_buttons')
    list_filter = ('status', 'program', 'entry_test_unlocked', 'created_at')
    search_fields = ('admission_code', 'first_name', 'last_name', 'email', 'cnic')
    readonly_fields = ('admission_code', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Full Name'

    def entry_test_status(self, obj):
        if obj.entry_test_unlocked:
            return format_html('<span style="color: green;">Unlocked</span>')
        return format_html('<span style="color: red;">Locked</span>')
    entry_test_status.short_description = 'Entry Test'

    def action_buttons(self, obj):
        unlock_icon = "🔓" if obj.entry_test_unlocked else "🔒"
        return format_html(
            '<a class="button" href="{}"">View</a> &nbsp;'
            '<a class="button" href="{}">{}</a>',
            reverse('admin:admission_assistant_admission_change', args=[obj.id]),
            reverse('admin:admission_assistant_admission_change', args=[obj.id]),
            unlock_icon
        )
    action_buttons.short_description = 'Actions'

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('admission_link', 'document_type', 'uploaded_at', 'verified', 'doc_preview')
    list_filter = ('document_type', 'verified', 'uploaded_at')
    search_fields = ('admission__admission_code', 'admission__first_name')
    readonly_fields = ('uploaded_at',)

    def admission_link(self, obj):
        url = reverse('admin:admission_assistant_admission_change', args=[obj.admission.id])
        return format_html('<a href="{}">{}</a>', url, obj.admission.admission_code)
    admission_link.short_description = 'Admission'

    def doc_preview(self, obj):
        if obj.file and hasattr(obj.file, 'url'):
            return format_html('<a href="{}" target="_blank">View Document</a>', obj.file.url)
        return "No file"
    doc_preview.short_description = 'Preview'

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('admission_link', 'payment_type', 'amount', 'status', 
                   'payment_date', 'transaction_id')
    list_filter = ('payment_type', 'status', 'payment_date')
    search_fields = ('admission__admission_code', 'transaction_id')
    readonly_fields = ('payment_date',)

    def admission_link(self, obj):
        url = reverse('admin:admission_assistant_admission_change', args=[obj.admission.id])
        return format_html('<a href="{}">{}</a>', url, obj.admission.admission_code)
    admission_link.short_description = 'Admission'

@admin.register(Guardian)
class GuardianAdmin(admin.ModelAdmin):
    list_display = ('name', 'relation', 'admission_link', 'phone', 'occupation', 'income')
    list_filter = ('relation',)
    search_fields = ('name', 'admission__admission_code', 'cnic')

    def admission_link(self, obj):
        url = reverse('admin:admission_assistant_admission_change', args=[obj.admission.id])
        return format_html('<a href="{}">{}</a>', url, obj.admission.admission_code)
    admission_link.short_description = 'Admission'

@admin.register(EntryTest)
class EntryTestAdmin(admin.ModelAdmin):
    list_display = ('admission_link', 'test_date', 'venue', 'status', 'score')
    list_filter = ('status', 'test_date')
    search_fields = ('admission__admission_code', 'admission__first_name')

    def admission_link(self, obj):
        url = reverse('admin:admission_assistant_admission_change', args=[obj.admission.id])
        return format_html('<a href="{}">{}</a>', url, obj.admission.admission_code)
    admission_link.short_description = 'Admission'

# Customize admin site
admin.site.site_header = 'University Admission Assistant'
admin.site.site_title = 'Admission Assistant Admin'
admin.site.index_title = 'Content Management'