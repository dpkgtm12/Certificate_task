import io
from django.http import FileResponse
from django.shortcuts import render, get_object_or_404
from .models import Certificate
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Image
from reportlab.pdfgen import canvas

def home(request):
    return render(request, 'home.html')

def generate_pdf_certificate(name, content,id,date):
    
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer,(740,570))
    template_image = Image('ct1.jpg')
    template_image.wrapOn(pdf,109,100)
    template_image.drawOn(pdf, 0, 0)
    pdf.setFont('Times-BoldItalic', 30)
    name_length=len(name)

    pdf.drawString(350-(name_length//2)*10, 330, name)
    pdf.setFillColorRGB(0.5, 0.4, 0.4)
    
    if len(content)>30:
        x=len(content)//2
        indx=content[x:].index(" ")
        content1=content[:x+indx]
        content2=content[x+indx:]
        pdf.setFont('Courier-Bold', 22)
        
        pdf.drawString(350-(x//2)*10, 250, content1)
        pdf.drawString(360-(x//2)*10, 230, content2)
    else:
        pdf.drawString(350-(len(content)//2)*10, 240, content)
    pdf.setFont('Courier', 18)
    pdf.setFillColorRGB(0, 0, 0)

    pdf.drawString(150, 170, str(date.strftime('%d-%m-%Y')))
    pdf.drawString(80, 80, "Certificate id-:"+str(id))
    pdf.save()
    buffer.seek(0)    
    return buffer

def CreateCertificate(request):
    if request.method == 'GET':
        return render(request, 'create_certificate.html')

    name = request.POST.get('name')
    content = request.POST.get('content')

    certificate = Certificate.objects.create(name=name, content=content)
    buffer = generate_pdf_certificate(name, content,certificate.id,certificate.created_at)
    certificate.pdf.save(f'certificate_{certificate.id}.pdf', buffer)
    return FileResponse(open(certificate.pdf.path, 'rb'), content_type='application/pdf')


def VerifyCertificate(request):
    if request.method == 'GET':
        return render(request, 'verify_certificate.html')
    certificate_id = request.POST.get('certificate_id')
    certificate = Certificate.objects.filter(id=certificate_id).first()
    if certificate is None:
        return render(request, 'verify_certificate.html', {'bool': 1})
    return render(request, 'verify_certificate.html', {'certificate': certificate})


def download_certificate(request, certificate_id):
    certificate = get_object_or_404(Certificate, id=certificate_id)
    if certificate.pdf:
        return FileResponse(open(certificate.pdf.path, 'rb'), content_type='application/pdf')
    return render(request, 'verify_certificate.html', {'certificate_id': certificate_id})