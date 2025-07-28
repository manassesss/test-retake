from django.contrib import admin
from .models import Process


@admin.register(Process)
class ProcessAdmin(admin.ModelAdmin):
    """Admin interface for Process model."""
    list_display = [
        'process_number', 'process_class', 'judge', 
        'parties_count', 'created_at'
    ]
    list_filter = ['process_class', 'judge', 'created_at']
    search_fields = ['process_number', 'subject', 'judge']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('process_number', 'process_class', 'subject', 'judge')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def parties_count(self, obj):
        """Display parties count."""
        return obj.parties_count
    parties_count.short_description = 'Parties Count'
