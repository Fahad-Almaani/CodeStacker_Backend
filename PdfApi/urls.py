
from django.urls import path,include
from .views import *
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'pdfs', AddPdf, basename="pdf") 
router.register(r'search', SearchViewSet, basename="search") 
router.register(r'Sentences', SentencesViewSet, basename="Sentences") 
# router.register(r'download-pdf', PdfDownloadView, basename="download-pdf") 
urlpatterns = [
 
    path('download-pdf/<int:pk>/', PdfDownloadView.as_view(), name='pdf_download'),
    path('occurrnce/', CheackOccurrenceView.as_view(), name='pdf_download'),
    path('top-5/', Top5OccurrenceView.as_view(), name='top-5'),
    path('pdf-to-image/', PageImgView.as_view(), name='pdf-to-image'),
]
urlpatterns += router.urls