from django.db import models

# Create your models here.
class PdfDocument(models.Model):
    name = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to='pdfs/')
    date_uploded = models.DateTimeField(auto_now_add=True)

class Sentence(models.Model):
    pdf = models.ForeignKey(PdfDocument,on_delete=models.CASCADE,related_name="PdfFile")
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)