from rest_framework import serializers
from .models import Process
from parties.models import Party, PartyContact


class PartyContactSerializer(serializers.ModelSerializer):
    """Serializer for party contact information."""
    
    class Meta:
        model = PartyContact
        fields = ['id', 'contact_type', 'value', 'is_primary']


class PartySerializer(serializers.ModelSerializer):
    """Serializer for party information."""
    contacts = PartyContactSerializer(many=True, read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = Party
        fields = [
            'id', 'name', 'document', 'category', 'category_display',
            'contacts', 'created_at', 'updated_at'
        ]


class ProcessSerializer(serializers.ModelSerializer):
    """Serializer for process information."""
    parties = PartySerializer(many=True, read_only=True)
    parties_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Process
        fields = [
            'id', 'process_number', 'process_class', 'subject', 'judge',
            'parties', 'parties_count', 'created_at', 'updated_at'
        ]


class ProcessListSerializer(serializers.ModelSerializer):
    """Simplified serializer for process listing."""
    parties_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Process
        fields = [
            'id', 'process_number', 'process_class', 'subject', 'judge',
            'parties_count', 'created_at'
        ]


class ProcessCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating processes."""
    
    class Meta:
        model = Process
        fields = ['process_number', 'process_class', 'subject', 'judge']
    
    def validate_process_number(self, value):
        """Validate process number format."""
        # Basic validation for Brazilian process number format
        import re
        # Remove common separators
        clean_number = re.sub(r'[^\d]', '', value)
        
        if len(clean_number) < 10:
            raise serializers.ValidationError(
                "Process number must have at least 10 digits."
            )
        
        return value 