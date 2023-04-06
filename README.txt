<<<<<<< HEAD
Hi, My name is Fahad 
happy to particpate 

This Backend Api Built with Django
these are the the urls avalibel

all urls using basic Auth passing [username,password]
in postman testing make sure you use BasickAuth
                               |                   |
urls                           |  Method           |  body params
-------------------------------------------------------------------
/api/pdfs/                     |  Get              |  
/api/pdfs/                     |  Post             |  {pdf_file}
/api/pdfs/<id>/                |  Get,Delete,Put   |  # note the last slash / is importient to delete
/api/search/                   |  Post             |  {keyword}
/api/Sentences/                |  Post             |  {id}
/api/download-pdf/<int:pk>/    |  Get              |  
/api/occurrnce/                |  Post             |  {pdf_file,word}
/api/top-5                     |  Post             |  {pdf_file}
/api/pdf-to-image              |  Post             |  {id,page_num}
