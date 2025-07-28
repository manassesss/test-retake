from django.contrib import admin
from .models import Party, PartyContact


class PartyContactInline(admin.TabularInline):
    """Inline admin for party contacts."""
    model = PartyContact
    extra = 1
    fields = ['contact_type', 'value', 'is_primary']


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    """Admin interface for Party model."""
    list_display = [
        'name', 'document', 'category', 'process', 
        'contacts_count', 'created_at'
    ]
    list_filter = ['category', 'created_at', 'process']
    search_fields = ['name', 'document', 'process__process_number']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['name']
    inlines = [PartyContactInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('process', 'name', 'document', 'category')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def contacts_count(self, obj):
        """Display contacts count."""
        return obj.contacts.count()
    contacts_count.short_description = 'Contacts Count'


@admin.register(PartyContact)
class PartyContactAdmin(admin.ModelAdmin):
    """Admin interface for PartyContact model."""
    list_display = [
        'party', 'contact_type', 'value', 'is_primary', 'created_at'
    ]
    list_filter = ['contact_type', 'is_primary', 'created_at', 'party__category']
    search_fields = ['value', 'party__name']
    readonly_fields = ['created_at']
    ordering = ['-is_primary', 'contact_type']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('party', 'contact_type', 'value', 'is_primary')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
