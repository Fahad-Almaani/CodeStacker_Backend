# Backend API Built with Django

This backend API is built with Django and provides several endpoints for various functionalities. Below, you'll find a table summarizing the available URLs, HTTP methods, and any required body parameters.

## How to Run

To run the server, follow these steps:

1. Download the files.
2. Create the Docker container with this command: docker compose up --build
3. The server will be running on `localhost` at port `8000`. You can now enjoy testing the API.

**Note**: All URLs require Basic Authentication with the following credentials:
- Username: fahad
- Password: 5005

## Available URLs

| URL                          | Method           | Body Params     |
|------------------------------|------------------|-----------------|
| `/api/pdfs/`                 | GET              |                 |
| `/api/pdfs/`                 | POST             | {pdf_file}      |
| `/api/pdfs/<id>/`            | GET, DELETE, PUT |                 |
| `/api/search/`               | POST             | {keyword}       |
| `/api/Sentences/`            | POST             | {id}            |
| `/api/download-pdf/<int:pk>/`| GET              |                 |
| `/api/occurrnce/`            | POST             | {pdf_file, word}|
| `/api/top-5`                 | POST             | {pdf_file}      |
| `/api/pdf-to-image`          | POST             | {id, page_num}  |
