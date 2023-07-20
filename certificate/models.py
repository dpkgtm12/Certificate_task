from django.db import models

# Create your models here.

def certificate_pdf_upload_path(instance, filename):
    return f'certificates/certificate_{instance.id}.pdf'

class Certificate(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    pdf = models.FileField(upload_to=certificate_pdf_upload_path, blank=True, null=True)

    def __str__(self):
        return self.name