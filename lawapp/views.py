from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
import requests
from firebase_admin import auth
import os
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage  # Import for file storage
from .forms import DocumentUploadForm  # Assuming you have a form for file upload
from reportlab.pdfgen import canvas  # For generating PDF reports
import spacy  # For keyword extraction with NLP+
import PyPDF2  # For handling PDF files
from io import BytesIO



# Import PyPDF2 if you are using it
# from PyPDF2 import PdfReader  # Uncomment if you are using PyPDF2

import firebase_config


nlp = spacy.load("en_core_web_sm")

import firebase_config

def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            api_key = 'AIzaSyASMdS69fhvzkCPqJO_6-H0Ca-N7nz5dyc'  # Replace with your Firebase API key
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": True
            }
            response = requests.post(url, json=payload)
            response.raise_for_status()  # Raise an error for bad responses

            data = response.json()
            id_token = data['idToken']  # Get ID token from the response

            # Here, you might want to create a session or store the ID token as needed
            messages.success(request, "Login successful!")
            return redirect('home')
        except requests.exceptions.HTTPError as e:
            error_message = e.response.json().get('error', {}).get('message', 'Unknown error')
            messages.error(request, f"Login failed: {error_message}")
    
    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html')

        try:
            # Create user in Firebase
            user = auth.create_user(
                email=email,
                password=password,
                display_name=username,
            )
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Error creating user: {str(e)}")
            return render(request, 'signup.html')

    return render(request, 'signup.html')

def home(request):
    return render(request, 'home.html')

import requests
from django.shortcuts import render
from django.conf import settings

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        api_key = 'AIzaSyAX9CLiAa1kqUJXvqWTcENJ2JAz0NwlPBM'  # Replace with your Firebase API Key

        url = f'https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={api_key}'
        data = {
            'requestType': 'PASSWORD_RESET',
            'email': email
        }
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()  # Raise an error if status is not 200
            return render(request, 'password_reset_email_sent.html')
        except requests.exceptions.RequestException as e:
            error_message = e.response.json().get('error', {}).get('message', 'Unknown error occurred')
            return render(request, 'forgot_password.html', {'error': error_message})
    return render(request, 'forgot_password.html')

def legal_research(request):
    return render(request, 'legal_research.html')

def legal_support(request):
    return render(request, 'legal_support.html')

def legal_bot(request):
    return render(request, 'legal_bot.html')

def profile(request):
    return render(request, 'profile.html')

def document_analysis(request):
    if request.method == 'POST':
        # Handle file upload and analysis
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['document']
            file_path = default_storage.save(f'documents/{uploaded_file.name}', uploaded_file)

            # Perform text extraction and keyword analysis
            # Ensure to handle the file type appropriately
            file_extension = uploaded_file.name.split('.')[-1].lower()

            if file_extension == 'txt':  # Handle text files
                with open(os.path.join(settings.MEDIA_ROOT, file_path), 'r', encoding="utf8") as f:
                    text = f.read()
            elif file_extension == 'pdf':  # Handle PDF files
                from PyPDF2 import PdfReader  # Import for PDF handling
                pdf_reader = PdfReader(os.path.join(settings.MEDIA_ROOT, file_path))
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            else:
                return JsonResponse({'error': 'Unsupported file type'}, status=400)

            doc = nlp(text)
            keywords = [ent.text for ent in doc.ents if ent.label_ in ('ORG', 'PERSON', 'GPE', 'LAW')]  # Extract keywords
            summary = f"Document has {len(text.split())} words and contains key legal terms."

            # Store results in the session
            request.session['keywords'] = keywords
            request.session['summary'] = summary

            # Return analysis results to the frontend via JSON
            return JsonResponse({'keywords': keywords, 'summary': summary})

    else:
        form = DocumentUploadForm()
    
    return render(request, 'document_analysis.html', {'form': form})

def download_report(request):
    # Generate a downloadable PDF report
    if not request.session.get('keywords') or not request.session.get('summary'):
        return HttpResponse("No analysis data available for download.", status=404)
    
    # Prepare PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="analysis_report.pdf"'
    pdf = canvas.Canvas(response)
    
    # Add content to PDF
    pdf.drawString(100, 750, "Document Analysis Report")
    pdf.drawString(100, 730, f"Keywords: {', '.join(request.session['keywords'])}")
    pdf.drawString(100, 710, f"Summary: {request.session['summary']}")
    
    # Finalize and save PDF
    pdf.showPage()
    pdf.save()
    
    return response

def upload_document(request):
    if request.method == "POST" and request.FILES.get('document'):
        document = request.FILES['document']

        # Extract text from the document
        file_extension = document.name.split('.')[-1].lower()
        text = ""

        # Handle different file types
        if file_extension == 'txt':
            text = document.read().decode('utf-8')
        elif file_extension == 'pdf':
            # Extract text from PDF
            pdf = PyPDF2.PdfReader(BytesIO(document.read()))
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        elif file_extension == 'docx':
            # Extract text from DOCX
            doc = docx.Document(BytesIO(document.read()))
            text = "\n".join([para.text for para in doc.paragraphs])

        # If no text is found, return an error
        if not text:
            return JsonResponse({'error': 'Failed to extract text from document.'}, status=400)

        # Process the text using spaCy
        doc = nlp(text)

        # Extract keywords (e.g., named entities, legal terms)
        keywords = [ent.text for ent in doc.ents]

        # Generate a simple summary (this can be improved with more complex logic)
        summary = "This document contains legal terms such as Contract, Jurisdiction, and Compliance."

        # Return the analysis results as JSON
        return JsonResponse({'keywords': keywords, 'summary': summary})

    return JsonResponse({'error': 'Invalid request.'}, status=400)




