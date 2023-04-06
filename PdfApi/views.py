
from rest_framework.response import Response
from django.http import HttpResponse, Http404
from django.http import FileResponse
from rest_framework.decorators import action
from rest_framework import status
from django.views import View
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet,ViewSet
from .serializer import PdfDocumentSerializer,PdfDocumentListSerializer,SentenceSerializer
from .models import PdfDocument,Sentence
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import PyPDF2
from django.shortcuts import get_object_or_404
import re
import nltk
nltk.download("stopwords")
from nltk.corpus import stopwords
# from wand.image import Image
from pdf2image import convert_from_path
from io import BytesIO
import os
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
# this View is to display pdf files and to upload files
# to get file by id pass the id in the urld   api/pdfs/1 to get file with id 1

class AddPdf(ModelViewSet):
    queryset = PdfDocument.objects.all()
    serializer_class = PdfDocumentListSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        pdf_file = request.FILES.get('pdf_file')
        content_type = (pdf_file.content_type).split('/')
        if content_type[-1] != "pdf":
            return Response(f"{content_type} is not supported",status=status.HTTP_400_BAD_REQUEST)
       
        pdf_document = PdfDocument(name=pdf_file.name[:-4],pdf_file=pdf_file)
        pdf_document.save()
        serializer = PdfDocumentSerializer(pdf_document)

        # this block will get the sentences from the PDF to be stored in the database 
        with open(pdf_document.pdf_file.path,'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text = page.extract_text()
                sentences = text.split('.')
                for sentence in sentences:
                    new_sentance = Sentence(pdf=pdf_document,text=sentence.lower())
                    new_sentance.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,headers=headers)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        pdf_path = instance.pdf_file.path
        self.perform_destroy(instance)
        # delete the file from the pdfs folder
        os.remove(pdf_path)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# in this View You can search by keyword pass it throug post request {"keyword":"example"}
# you will get sentances and files containig that word
class SearchViewSet(ViewSet):
    queryset= Sentence.objects.all()
    serializer_class = SentenceSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        search_keyword = request.data.get('keyword',None)
        if search_keyword:
            queryset = Sentence.objects.filter(text__icontains=search_keyword)
            serializer = self.serializer_class(queryset,many=True)
            files_ids = []
            for sentance in queryset:
                files_ids.append(sentance.pdf.id)
            pdf_files = PdfDocument.objects.filter(id__in=files_ids)
            serializer_files = PdfDocumentSerializer(pdf_files,many=True)
            return Response({"files":serializer_files.data,"sentances":serializer.data})            
        else:
            return Response({"Message":"No Keyword provided"})
    
    # list function is add just to make it easy to see in the aoi root link for easy navigation for the teasting
    def list(self, request):
        return Response({"Message":"This End-point to search using keyword"})


# this View to Display all Sentences realted to file py providing file id pass it {"id":<id>}

class SentencesViewSet(ViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        file = PdfDocument.objects.get(id=request.data['id'])
        sentences = Sentence.objects.filter(pdf=file)
        serializer = SentenceSerializer(sentences,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    # list function is add just to make it easy to see in the aoi root link for easy navigation for the teasting
    def list(self, request):
        return Response({"Message":r"This End-point to get all sentences related to file pass {'id':<id>}"})

class PdfDownloadView(View):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
    # Retrieve the PdfDocument object by its ID
        pdf_doc = get_object_or_404(PdfDocument, pk=pk)

        # Open the corresponding file and read its contents
        with open(pdf_doc.pdf_file.path, 'rb') as f:
            pdf_contents = f.read()

        # Set the response content type to PDF
        response = HttpResponse(pdf_contents, content_type='application/pdf')

        # Set the Content-Disposition header to force the file download
        response['Content-Disposition'] = f'attachment; filename="{pdf_doc.pdf_file.name}"'

        return response


class CheackOccurrenceView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        word = str(request.data['word']).lower()
        pdf_file = request.FILES.get('pdf_file')
        content_type = (pdf_file.content_type).split('/')
        if content_type[-1] != "pdf":
            return Response(f"{content_type} is not supported",status=status.HTTP_400_BAD_REQUEST)
        
        pdf_document = PdfDocument(name=pdf_file.name[:-4],pdf_file=pdf_file)
        pdf_document.save()
        serializer = PdfDocumentSerializer(pdf_document)

        # this block will get the sentences from the PDF to be stored in the database 
        with open(pdf_document.pdf_file.path,'rb') as file:
            sentences_list = []
            pdf_reader = PyPDF2.PdfReader(file)
            num_occurrnece=0
            for page in pdf_reader.pages:
                text = page.extract_text()
                sentences = text.split('.')
                for sentence in sentences:
                    num_occurrnece += (sentence.lower()).count(word)
                    sentences_list.append(sentence.lower())
            sentences = [x for x in sentences_list if word in x]
            return Response({"num_of_occurrnece":num_occurrnece,'sentences':sentences})


class Top5OccurrenceView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        

        pdf_file = request.FILES.get('pdf_file')
        content_type = (pdf_file.content_type).split('/')
        if content_type[-1] != "pdf":
            return Response(f"{content_type} is not supported",status=status.HTTP_400_BAD_REQUEST)
        
        pdf_document = PdfDocument(name=pdf_file.name[:-4],pdf_file=pdf_file)
        pdf_document.save()
       

        # this block will get the sentences from the PDF to be stored in the database 
        with open(pdf_document.pdf_file.path,'rb') as file:
           
            all_words = []
            words_with_occurr = {}
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page in pdf_reader.pages:
                text = page.extract_text()

                words = text.split()
                pattern = re.compile(r'[^\w\s]')
                clean_words = [re.sub(pattern, '', word) for word in words]
                all_words.extend(clean_words)

            
            # removig stop words
            stop_words = set(stopwords.words('english'))
            all_words = [word for word in all_words if word.lower() not in stop_words]
            all_words = list(map(str.lower,all_words))
            for word in all_words:
                if word not in words_with_occurr.keys():
                    words_with_occurr[word] =  all_words.count(word)

            sorted_items = sorted(words_with_occurr.items(), key=lambda x: x[1], reverse=True)
            top_5 = [item[0] for item in sorted_items[:5]]
            return Response(top_5)
   

# this end-point to retrive a page as image data needed : {page_num,id} :id->pdf fiel id
class PageImgView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        import fitz
        pdf_id = request.data['id']
        page_num = int(request.data['page_num'])-1
        pdf_file = get_object_or_404(PdfDocument,id=pdf_id)
        if not pdf_file:
            return Response(f"No file with the id ({pdf_id}) Found",status=status.HTTP_404_NOT_FOUND)
        
        with fitz.open(pdf_file.pdf_file.path) as doc:
            # Get the specified page
            page = doc[page_num]

            # Render the page as a PNG image
            pixmap = page.get_pixmap()
            img_bytes = pixmap.tobytes()

            return HttpResponse(img_bytes,content_type="image/png")



class DeleteAllData(ModelViewSet):
    queryset = PdfDocument.objects.all()
    serializer_class = PdfDocumentSerializer
    def create(self,request,*args):
        PdfDocument.objects.all().delete()
        Sentence.objects.all().delete()
        return Response("Deleted")