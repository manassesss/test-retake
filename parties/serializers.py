from rest_framework import serializers
from .models import Party, PartyContact


class PartyContactSerializer(serializers.ModelSerializer):
    """Serializer for party contact information."""
    
    class Meta:
        model = PartyContact
        fields = ['id', 'contact_type', 'value', 'is_primary']
    
    def validate(self, data):
        """Validate contact information."""
        if data['contact_type'] == 'EMAIL':
            from django.core.validators import EmailValidator
            validator = EmailValidator()
            try:
                validator(data['value'])
            except:
                raise serializers.ValidationError(
                    {'value': 'Enter a valid email address.'}
                )
        
        elif data['contact_type'] == 'PHONE':
            import re
            phone_pattern = r'^\+?55?\s?\(?[0-9]{2}\)?\s?[0-9]{4,5}-?[0-9]{4}$'
            if not re.match(phone_pattern, data['value']):
                raise serializers.ValidationError(
                    {'value': 'Enter a valid phone number.'}
                )
        
        return data


class PartySerializer(serializers.ModelSerializer):
    """Serializer for party information."""
    contacts = PartyContactSerializer(many=True, read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = Party
        fields = [
            'id', 'process', 'name', 'document', 'category', 'category_display',
            'contacts', 'created_at', 'updated_at'
        ]


class PartyCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating parties."""
    
    class Meta:
        model = Party
        fields = ['process', 'name', 'document', 'category']
    
    def validate_document(self, value):
        """Validate document format (CPF/CNPJ)."""
        import re
        # Remove non-digits
        clean_doc = re.sub(r'[^\d]', '', value)
        
        if len(clean_doc) not in [11, 14]:  # CPF has 11 digits, CNPJ has 14
            raise serializers.ValidationError(
                "Document must be a valid CPF (11 digits) or CNPJ (14 digits)."
            )
        
        return value


class PartyContactCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating party contacts."""
    
    class Meta:
        model = PartyContact
        fields = ['party', 'contact_type', 'value', 'is_primary']
    
    def validate(self, data):
        """Validate contact information."""
        if data['contact_type'] == 'EMAIL':
            from django.core.validators import EmailValidator
            validator = EmailValidator()
            try:
                validator(data['value'])
            except:
                raise serializers.ValidationError(
                    {'value': 'Enter a valid email address.'}
                )
        
        elif data['contact_type'] == 'PHONE':
            import re
            phone_pattern = r'^\+?55?\s?\(?[0-9]{2}\)?\s?[0-9]{4,5}-?[0-9]{4}$'
            if not re.match(phone_pattern, data['value']):
                raise serializers.ValidationError(
                    {'value': 'Enter a valid phone number.'}
                )
        
        return data 