from django.db import models
from django.core.validators import EmailValidator
from processes.models import Process


class Party(models.Model):
    """
    Model to store party information in legal processes.
    """
    PARTY_CATEGORY_CHOICES = [
        ('EXEQUENTE', 'Exequente'),
        ('EXECUTADA', 'Executada'),
        ('AUTOR', 'Autor'),
        ('REU', 'Réu'),
        ('TERCEIRO', 'Terceiro'),
        ('ADVOGADO', 'Advogado'),
        ('PROCURADOR', 'Procurador'),
    ]

    process = models.ForeignKey(
        Process,
        on_delete=models.CASCADE,
        related_name='parties',
        verbose_name="Process"
    )
    name = models.CharField(
        max_length=200,
        verbose_name="Name"
    )
    document = models.CharField(
        max_length=20,
        verbose_name="Document (CPF/CNPJ)"
    )
    category = models.CharField(
        max_length=20,
        choices=PARTY_CATEGORY_CHOICES,
        verbose_name="Party Category"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated At"
    )

    class Meta:
        verbose_name = "Party"
        verbose_name_plural = "Parties"
        ordering = ['name']
        unique_together = ['process', 'name', 'document']

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class PartyContact(models.Model):
    """
    Model to store contact information for parties.
    """
    CONTACT_TYPE_CHOICES = [
        ('EMAIL', 'Email'),
        ('PHONE', 'Phone'),
    ]

    party = models.ForeignKey(
        Party,
        on_delete=models.CASCADE,
        related_name='contacts',
        verbose_name="Party"
    )
    contact_type = models.CharField(
        max_length=10,
        choices=CONTACT_TYPE_CHOICES,
        verbose_name="Contact Type"
    )
    value = models.CharField(
        max_length=255,
        verbose_name="Contact Value"
    )
    is_primary = models.BooleanField(
        default=False,
        verbose_name="Is Primary Contact"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At"
    )

    class Meta:
        verbose_name = "Party Contact"
        verbose_name_plural = "Party Contacts"
        ordering = ['-is_primary', 'contact_type', 'value']

    def __str__(self):
        return f"{self.party.name} - {self.get_contact_type_display()}: {self.value}"

    def clean(self):
        """Validate contact information."""
        from django.core.exceptions import ValidationError
        
        if self.contact_type == 'EMAIL':
            validator = EmailValidator()
            try:
                validator(self.value)
            except ValidationError:
                raise ValidationError({'value': 'Enter a valid email address.'})
        
        elif self.contact_type == 'PHONE':
            # Basic phone validation (Brazilian format)
            import re
            phone_pattern = r'^\+?55?\s?\(?[0-9]{2}\)?\s?[0-9]{4,5}-?[0-9]{4}$'
            if not re.match(phone_pattern, self.value):
                raise ValidationError({'value': 'Enter a valid phone number.'})
