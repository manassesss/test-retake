from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Party, PartyContact
from .serializers import (
    PartySerializer,
    PartyCreateUpdateSerializer,
    PartyContactSerializer,
    PartyContactCreateUpdateSerializer
)


class PartyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing parties in legal processes.
    """
    queryset = Party.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'process']
    search_fields = ['name', 'document']
    ordering_fields = ['name', 'created_at', 'updated_at']
    ordering = ['name']

    def get_serializer_class(self):
        """Return appropriate serializer class based on action."""
        if self.action in ['create', 'update', 'partial_update']:
            return PartyCreateUpdateSerializer
        return PartySerializer

    @action(detail=True, methods=['get'])
    def contacts(self, request, pk=None):
        """Get all contacts for a specific party."""
        party = self.get_object()
        contacts = PartyContact.objects.filter(party=party)
        serializer = PartyContactSerializer(contacts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_contact(self, request, pk=None):
        """Add a contact to a party."""
        party = self.get_object()
        data = request.data.copy()
        data['party'] = party.id
        
        serializer = PartyContactCreateUpdateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PartyContactViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing party contacts.
    """
    queryset = PartyContact.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['contact_type', 'party', 'is_primary']
    search_fields = ['value']
    ordering_fields = ['contact_type', 'is_primary', 'created_at']
    ordering = ['-is_primary', 'contact_type']

    def get_serializer_class(self):
        """Return appropriate serializer class based on action."""
        if self.action in ['create', 'update', 'partial_update']:
            return PartyContactCreateUpdateSerializer
        return PartyContactSerializer

    @action(detail=False, methods=['get'])
    def emails(self, request):
        """Get all email contacts."""
        emails = self.get_queryset().filter(contact_type='EMAIL')
        serializer = self.get_serializer(emails, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def phones(self, request):
        """Get all phone contacts."""
        phones = self.get_queryset().filter(contact_type='PHONE')
        serializer = self.get_serializer(phones, many=True)
        return Response(serializer.data)
