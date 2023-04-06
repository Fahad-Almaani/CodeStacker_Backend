from .models import PdfDocument,Sentence
from rest_framework import serializers
from PyPDF2 import PdfReader
import os

class PdfDocumentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    class Meta:
        model = PdfDocument
        fields = ['id','name','pdf_file']

class PdfDocumentListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    num_pages = serializers.SerializerMethodField()
    file_size_KB = serializers.SerializerMethodField()
    class Meta:
        model = PdfDocument
        fields = ['id','name','pdf_file','num_pages', 'file_size_KB']

    def get_num_pages(self,obj):
        with open(obj.pdf_file.path,"rb") as file:
            pdf_reader = PdfReader(file)
            num_pages = len(pdf_reader.pages)
        return num_pages
    
    def get_file_size_KB(self,obj):
        file_size = os.path.getsize(obj.pdf_file.path)
        file_size_KB = file_size / 1000
        return file_size_KB
    
class SentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentence
        fields = "__all__"

# class SearchSentenceSerializer(serializers.ModelSerializer):
#     class Meta:
        