from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import pdfreader
from pdfreader import PDFDocument, SimplePDFViewer
import PyPDF2 as pdf2
import fitz
from django.template.loader import get_template
from django.template import Context
import pdfkit
from bs4 import BeautifulSoup
import cloudconvert
import os
import requests

# Create your views here.

#General URLs

def register(request):
    return render(request, 'officelyapp/register.html', {})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == 'admin':
                return redirect('/officelyapp/dashboard/')
        else:
            print("Login Failed")
            return HttpResponse("Invalid Details")
    else:
        return render(request, 'login.html',{})

def dashboard(request):
    return render(request, 'officelyapp/dashboard.html')

def profile(request):
    return render(request, 'officelyapp/profile.html')

def whatsapp(request):
    return render(request, 'officelyapp/apps/whatsapp.html')

def todo(request):
    return render(request, 'officelyapp/apps/todo.html')

def mail(request):
    return render(request, 'officelyapp/apps/mail.html')

def getSignatureLink(request):
    return render(request, 'officelyapp/signature/signatureLink.html')

def getSignatureTemplate(request):
    return render(request, 'officelyapp/signature/signatureTemplate.html')

def enduserSignature(request):
    return render(request, 'officelyapp/signature/enduserSignature.html')

def getMeetingLink(request):
    return render(request, 'officelyapp/schedule/meetingLink.html')

def getMeetingTemplate(request):
    return render(request, 'officelyapp/schedule/meetingTemplate.html')

def enduserMeetingLink(request):
    return render(request, 'officelyapp/schedule/enduserMeetingLink.html')

def getNewDoc(request):
    return render(request, 'officelyapp/ocr/getNewDoc.html')

def enduserDoc(request):
    return render(request, 'officelyapp/ocr/enduserDoc.html')

def newCustomer(request):
    return render(request, 'officelyapp/customer/newCustomer.html')

def uploadCustomer(request):
    return render(request, 'officelyapp/customer/uploadCustomer.html')

def getCustomer(request):
    return render(request, 'officelyapp/customer/getCustomer.html')

def apiCustomer(request):
    return render(request, 'officelyapp/customer/apiCustomer.html')

def getDoc(request):
    context={}
    uploaded_file = request.FILES['file']
    fs = FileSystemStorage()
    name = fs.save(uploaded_file.name, uploaded_file)
    context['filelink']=fs.url(name)
    print(context['filelink'])
    cloudconvert.configure(api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiY2QxNzA3YzI1NDJkZjg1MzRmYjIxZTRjMzk1ODhmMjhlYzNhNjQ5NTljNTJhZWE1OGRmYzNmOGE5YjkxYTYyZjE4MmY3YTg3OWU0ZGU4NjkiLCJpYXQiOiIxNjA5OTk2OTM1LjAxNzk4MiIsIm5iZiI6IjE2MDk5OTY5MzUuMDE4MDA2IiwiZXhwIjoiNDc2NTY3MDUzNC45NzU5NDciLCJzdWIiOiI0ODAyNDIxOCIsInNjb3BlcyI6WyJ1c2VyLnJlYWQiLCJ1c2VyLndyaXRlIiwidGFzay5yZWFkIiwidGFzay53cml0ZSIsIndlYmhvb2sucmVhZCIsIndlYmhvb2sud3JpdGUiLCJwcmVzZXQucmVhZCIsInByZXNldC53cml0ZSJdfQ.knL0Iwyy3yyYd-oilImNyF7g-VQes_CnfkKp-o_o_EcaXZC6Fd7-vibJL2qbAYp6kPMr95fyWoQgt6ax62nhSj8lT2jEPXbrDWxcOlnkS4-vW4Bp29tmlBlqQmx1dRa-ZbokPhqncfwFC1IK-uZenm-sDsaXIAmhnRZSVNefbG67kVOlSFN8bnYJOVYszcgrSW5OlAdE-vuWZ0GuP5aPrwC-FE3RtmADpeRigEDM_sgKUoE_8vNHnOPjsCrHAi_T5zd8qqOEtFL4zf8c89yNImlkkhx-M352KyjdLAb-aN-AJ4Vy_7qCZhQ9ty2984Qm7TIM2m3pQs4K5GcSKj6YH14vkVjklhEvmUSfssiiSJCTQxYRBf80HQglTwaqeX2dfC-kjAa45a0EjFjbbw_HZLp4KJ2cJPYT7CUzrS0M9WqyXUtCdJNveD9FhmOCprKHn5u1AI5CzenCQluqPOb0ZNHN8HVZYnCUXeGn3JeRPFYk_SFFzlU85vBZMwYeHY9_M43syWiQ6iF1gIlGPdzIU5EqKetAZGW4LciGodt1AJa65YzW6GydStFEbyc0-6LL7kra_XnI0qR6UUb2t-ljnWfRN9rc9iym8QEQxTALfB5R0LSEJZOZNhcZnfANrBktGqi669rh-9e1bfKA6A3_OjhoFgB8U_gLYcROmJ5A6bA', sandbox = False)
    test = cloudconvert.Job.create(payload={
        "tasks": {
            'import-my-file': {
                'operation': 'import/url',
                'url': 'http://localhost:8000'+context['filelink']
            },
            'convert-my-file': {
                'operation': 'convert',
                'input': 'import-my-file',
                'output_format': 'html'
            },
            'export-my-file': {
                'operation': 'export/url',
                'input': 'convert-my-file'
            }
        }
    })
    print(test['tasks'][0]['id'])
    exported_url_task_id = test['tasks'][0]['id']
    res = cloudconvert.Task.wait(id=exported_url_task_id) # Wait for job completion
    # file = res.get("result").get("files")[0]
    # res = cloudconvert.download(filename=file['filename'], url=file['url'])
    print(res)
    # context={}
    # file = fitz.open('media/test.pdf')
    # for pageNumber, page in enumerate(file.pages(), start=1):
    #     text = page.getText()
    #     #print(text)
    # context['page_text'] = text
    return render(request, 'officelyapp/signature/signatureLink.html')

def saveTemplate(request):
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
    }
    pdfkit.from_file("templates/officelyapp/signature/signatureLink.html", "string.pdf", options=options)
    return render(request, 'officelyapp/signature/signatureLink.html')
