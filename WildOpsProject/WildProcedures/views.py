# filepath: /home/guym/Desktop/Nextcloud/Documents/wildops_project/WildOpsProject/WildProcedures/views.py

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from .forms import ProcedureForm
from .checklist_generator import ChecklistGenerator
import os
import io
import zipfile

def create_procedure(request):
    pdf_generated = False
    checklist_pdf_url = ''
    procedure_pdf_url = ''
    
    if request.method == 'POST':
        form = ProcedureForm(request.POST)
        if form.is_valid():
            procedure = form.save()
            checklist_files = [
                os.path.join(settings.BASE_DIR, 'WildProcedures', 'data', 'json', '09_emergency_procedures.json'),
                os.path.join(settings.BASE_DIR, 'WildProcedures', 'data', 'json', '08_contingency_procedures.json'),
                os.path.join(settings.BASE_DIR, 'WildProcedures', 'data', 'json', '03_first_flight.json'),
                os.path.join(settings.BASE_DIR, 'WildProcedures', 'data', 'json', '04_pre_flight.json'),
                os.path.join(settings.BASE_DIR, 'WildProcedures', 'data', 'json', '05_in_flight.json'),
                os.path.join(settings.BASE_DIR, 'WildProcedures', 'data', 'json', '06_post_flight.json'),
                os.path.join(settings.BASE_DIR, 'WildProcedures', 'data', 'json', '00_operation_planning.json'),
                os.path.join(settings.BASE_DIR, 'WildProcedures', 'data', 'json', '01_pre_operation.json'),
                os.path.join(settings.BASE_DIR, 'WildProcedures', 'data', 'json', '02_packing.json'),
                os.path.join(settings.BASE_DIR, 'WildProcedures', 'data', 'json', '07_post_operation.json'),
            ]
            generator = ChecklistGenerator(
                checklist_files,
                procedure.operation_type,
                procedure.drone_platform,
                procedure.number_of_drones
            )
            
            # Generate PDFs in MEDIA_ROOT/pdfs/
            generator.generate_checklist_pdf('checklist.pdf')
            generator.generate_procedure_pdf('procedure.pdf')

            pdf_generated = True
            # Point to their media URLs
            checklist_pdf_url = settings.MEDIA_URL + 'pdfs/checklist.pdf'
            procedure_pdf_url = settings.MEDIA_URL + 'pdfs/procedure.pdf'
    else:
        form = ProcedureForm()

    context = {
        'form': form,
        'pdf_generated': pdf_generated,
        'checklist_pdf_url': checklist_pdf_url,
        'procedure_pdf_url': procedure_pdf_url,
        'download_url': '/procedures/download_zip/'
    }
    return render(request, 'WildProcedures/create_procedure.html', context)

def download_zip(request):
    # Path of the two existing PDFs
    checklist_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', 'checklist.pdf')
    procedure_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', 'procedure.pdf')
    
    # Build an in-memory ZIP
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w') as z:
        if os.path.exists(checklist_path):
            z.write(checklist_path, arcname='checklist.pdf')
        if os.path.exists(procedure_path):
            z.write(procedure_path, arcname='procedure.pdf')
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="procedures.zip"'
    return response