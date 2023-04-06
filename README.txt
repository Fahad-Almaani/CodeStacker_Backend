<<<<<<< HEAD
Hi, My name is Fahad 
happy to particpate 

This Backend Api Built with Django
these are the the urls avalibel


How To Run:
    after downloading the files 
    create the docker container with this command:
        -docker compose up --build
    then the server will be runing on the local host port 8000
    **enjoy testing
        

all urls using basic Auth passing [username=fahad,password=5005]

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






# Notes
 - seting fixed username and password to make things quick
 - If you know Django I was traing to use diffrent types of View out of changes :\
 - I am using sqlite to make it smoth but it can be replaced essaly with mysql or other options 

Contacts:
Phone: 90943436
gmail: fahad.almaani.fa@gmail.com
