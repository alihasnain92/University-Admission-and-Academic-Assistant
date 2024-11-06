# backend/admission_assistant/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response as DRFResponse
from rest_framework.reverse import reverse
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import (
    IntentCategory, 
    Response, 
    Admission, 
    Document, 
    Payment, 
    Guardian, 
    EntryTest
)
from .serializers import (
    AdmissionSerializer,
    DocumentSerializer,
    PaymentSerializer,
    GuardianSerializer,
    EntryTestSerializer
)
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
def api_root(request):
    """
    API root endpoint showing available endpoints
    """
    return DRFResponse({
        'message': 'Welcome to University Admission Assistant API',
        'endpoints': {
            'query': request.build_absolute_uri(reverse('process-query')),
            'admissions': request.build_absolute_uri(reverse('admission-list')),
        },
        'status': 'API is running'
    })

@api_view(['POST'])
def process_query(request):
    """
    Process chatbot queries and return appropriate responses
    """
    try:
        query = request.data.get('query', '').lower()
        logger.info(f"Received query: {query}")
        
        # Find matching category
        matching_category = None
        for category in IntentCategory.objects.all():
            keywords = [k.strip().lower() for k in category.keywords.split(',')]
            if any(keyword in query for keyword in keywords):
                matching_category = category
                break
        
        if matching_category:
            response = Response.objects.filter(
                category=matching_category
            ).order_by('-priority').first()
            
            if response:
                return DRFResponse({
                    'response': response.response_text,
                    'category': matching_category.name,
                    'status': 'success'
                })
        
        return DRFResponse({
            'response': "I'm sorry, I don't understand that question. Could you please rephrase it?",
            'category': None,
            'status': 'no_match'
        })
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        return DRFResponse({
            'response': "Sorry, there was an error processing your request.",
            'status': 'error',
            'error': str(e)
        }, status=500)

class AdmissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling admission-related operations
    """
    queryset = Admission.objects.all()
    serializer_class = AdmissionSerializer
    
    @action(detail=False, methods=['POST'])
    def submit_application(self, request):
        """
        Submit a new admission application
        """
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                admission = serializer.save()
                return DRFResponse({
                    'message': 'Application submitted successfully',
                    'admission_code': admission.admission_code,
                    'status': 'success'
                }, status=status.HTTP_201_CREATED)
            return DRFResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error submitting application: {str(e)}")
            return DRFResponse({
                'message': 'Error submitting application',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['GET'])
    def check_status(self, request, pk=None):
        """
        Check the status of an admission application
        """
        try:
            admission = self.get_object()
            return DRFResponse({
                'status': admission.status,
                'entry_test_unlocked': admission.entry_test_unlocked,
                'application_details': AdmissionSerializer(admission).data
            })
        except Exception as e:
            logger.error(f"Error checking status: {str(e)}")
            return DRFResponse({
                'message': 'Error checking application status',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DocumentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling document uploads
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    parser_classes = (MultiPartParser, FormParser)

    @action(detail=False, methods=['POST'])
    def upload_document(self, request):
        """
        Upload a document for an admission application
        """
        try:
            admission_code = request.data.get('admission_code')
            admission = get_object_or_404(Admission, admission_code=admission_code)
            
            serializer = self.get_serializer(data={
                **request.data,
                'admission': admission.id
            })
            
            if serializer.is_valid():
                document = serializer.save()
                return DRFResponse({
                    'message': 'Document uploaded successfully',
                    'document_id': document.id
                }, status=status.HTTP_201_CREATED)
            return DRFResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error uploading document: {str(e)}")
            return DRFResponse({
                'message': 'Error uploading document',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling payments
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    @action(detail=False, methods=['POST'])
    def process_payment(self, request):
        """
        Process a payment for an admission application
        """
        try:
            admission_code = request.data.get('admission_code')
            admission = get_object_or_404(Admission, admission_code=admission_code)
            
            serializer = self.get_serializer(data={
                **request.data,
                'admission': admission.id,
                'status': 'pending'
            })
            
            if serializer.is_valid():
                payment = serializer.save()
                # Here you would typically integrate with a payment gateway
                return DRFResponse({
                    'message': 'Payment initiated successfully',
                    'payment_id': payment.id,
                    'status': payment.status
                }, status=status.HTTP_201_CREATED)
            return DRFResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error processing payment: {str(e)}")
            return DRFResponse({
                'message': 'Error processing payment',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EntryTestViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling entry test related operations
    """
    queryset = EntryTest.objects.all()
    serializer_class = EntryTestSerializer

    @action(detail=True, methods=['POST'])
    def toggle_access(self, request, pk=None):
        """
        Toggle entry test access for an admission
        """
        try:
            entry_test = self.get_object()
            admission = entry_test.admission
            admission.entry_test_unlocked = not admission.entry_test_unlocked
            admission.save()
            
            return DRFResponse({
                'message': f'Entry test access {"granted" if admission.entry_test_unlocked else "revoked"}',
                'entry_test_unlocked': admission.entry_test_unlocked
            })
        except Exception as e:
            logger.error(f"Error toggling entry test access: {str(e)}")
            return DRFResponse({
                'message': 'Error toggling entry test access',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['GET'])
    def check_access(self, request, pk=None):
        """
        Check if entry test is accessible
        """
        try:
            entry_test = self.get_object()
            return DRFResponse({
                'entry_test_unlocked': entry_test.admission.entry_test_unlocked,
                'test_status': entry_test.status
            })
        except Exception as e:
            logger.error(f"Error checking entry test access: {str(e)}")
            return DRFResponse({
                'message': 'Error checking entry test access',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)