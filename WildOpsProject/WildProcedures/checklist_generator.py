import json
import os
from fpdf import FPDF
import math
from django.conf import settings
from datetime import datetime
from shared.constants import OPERATION_TYPE_CHOICES, DRONE_PLATFORM_CHOICES, NUMBER_OF_DRONES_CHOICES

class ChecklistGenerator:

    def __init__(self, checklist_files, operation_type, drone_platform, number_of_drones):
        self.checklist_files = checklist_files
        self.operation_type = operation_type
        self.drone_platform = drone_platform
        self.number_of_drones = number_of_drones
        self.checklists = self.load_checklists()
        self.font_path_open_sans_regular = os.path.join(settings.BASE_DIR, 'WildProcedures/static/WildProcedures/fonts/Open_Sans/static/OpenSans-Regular.ttf')
        self.font_path_open_sans_bold = os.path.join(settings.BASE_DIR, 'WildProcedures/static/WildProcedures/fonts/Open_Sans/static/OpenSans-Bold.ttf')
        self.font_path_montserrat_bold = os.path.join(settings.BASE_DIR, 'WildProcedures/static/WildProcedures/fonts/Montserrat/static/Montserrat-Bold.ttf')
        self.font_path_montserrat_medium = os.path.join(settings.BASE_DIR, 'WildProcedures/static/WildProcedures/fonts/Montserrat/static/Montserrat-Medium.ttf')
        self.logo_path = os.path.join(settings.BASE_DIR, 'WildProcedures/static/WildProcedures/media/WD_logo.png')

    def load_checklists(self):
        checklists = []
        for file in self.checklist_files:
            with open(file, 'r', encoding='utf-8') as f:
                checklists.append(json.load(f))
        return checklists

    def filter_procedures(self, procedures):
        filtered_procedures = []
        for procedure in procedures:
            if (self.operation_type in procedure['operation_types'] or 'ALL' in procedure['operation_types']) and \
               (self.drone_platform in procedure['drone_platforms'] or 'ALL' in procedure['drone_platforms']) and \
               (self.number_of_drones in procedure['number_of_drones'] or 'ALL' in procedure['number_of_drones']):
                filtered_procedures.append(procedure)
        return filtered_procedures

    def add_branding_banner(self, pdf, title, max_title_width, vertical_spacing):
        pdf.image(self.logo_path, 10, 6, 28)  # Adjust the position and size as needed
        pdf.set_font("Montserrat-Bold", size=20)
        combined_title = f"{title}".upper()
        pdf.set_x((pdf.w - max_title_width) / 2)  # Center the title horizontally
        pdf.multi_cell(max_title_width, 10, combined_title, align='C')
        pdf.ln(vertical_spacing)

    def add_metadata(self, pdf, font_size, box_width):
        pdf.set_font("OpenSans", size=font_size)
        operation_type_expanded = dict(OPERATION_TYPE_CHOICES).get(self.operation_type, self.operation_type)
        drone_platform_expanded = dict(DRONE_PLATFORM_CHOICES).get(self.drone_platform, self.drone_platform)
        number_of_drones_expanded = dict(NUMBER_OF_DRONES_CHOICES).get(self.number_of_drones, self.number_of_drones)
        current_datetime = datetime.now().strftime("%d-%m-%Y %H:%M")
        metadata = f"{operation_type_expanded} | {drone_platform_expanded} | {number_of_drones_expanded} | {current_datetime}"
        pdf.set_fill_color(211, 211, 211) 
        pdf.cell(box_width, font_size*0.6, metadata, border=1, ln=True, align='C', fill=True)

    def generate_checklist_pdf(self, output_file):
        ## STYLING
        bullet_spacing = 5
        font_size = 10
        box_width = 120
        vertical_spacing = font_size / 2
        max__title_width = 75  # Set the maximum width for the title text box
        ## Code to generate the PDF
        pdf = FPDF(format='A5')
        pdf.add_font("OpenSans", "", self.font_path_open_sans_regular, uni=True)
        pdf.add_font("OpenSans", "B", self.font_path_open_sans_bold, uni=True)
        pdf.add_font("Montserrat-Bold", "", self.font_path_montserrat_bold, uni=True)
        pdf.add_font("Montserrat-Medium", "", self.font_path_montserrat_medium, uni=True)
        pdf.set_font("OpenSans", size=font_size)
        for checklist in self.checklists:
            title = checklist['title']
            color = checklist.get('color', [0, 0, 0])
            items = checklist['items']
            page_number = 1
            pdf.add_page()
            # Check if the section fits on the current page
            section_height = vertical_spacing  # Initialize section height
            for section in items:
                filtered_procedures = self.filter_procedures(section['procedures'])
                for procedure in filtered_procedures:
                    text_width = pdf.get_string_width(procedure['checklist_entry'])
                    lines = max(1, ((text_width+bullet_spacing) // (box_width))+1)
                    section_height += vertical_spacing * lines
            if pdf.get_y() + section_height > pdf.h - pdf.b_margin:
                self.add_branding_banner(pdf, f"{title} ({page_number})", max__title_width, vertical_spacing * 1.5)
            else:
                self.add_branding_banner(pdf, f"{title}", max__title_width, vertical_spacing * 1.5)
            self.add_metadata(pdf, font_size-3, box_width)
            pdf.set_fill_color(*color)
            pdf.rect(140, 0, 10, 210, 'F')  # Thin color band on the right for A5
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("OpenSans", size=font_size)
            for section in items:
                section_height = vertical_spacing  # Initialize section height
                filtered_procedures = self.filter_procedures(section['procedures'])
                for procedure in filtered_procedures:
                    text_width = pdf.get_string_width(procedure['checklist_entry'])
                    lines = max(1, ((text_width+bullet_spacing) // (box_width))+1)
                    section_height += vertical_spacing * lines

                # Check if the section fits on the current page
                if pdf.get_y() + section_height > pdf.h - pdf.b_margin:
                    # Add a new page if the section doesn't fit
                    page_number += 1
                    pdf.add_page()
                    self.add_branding_banner(pdf, f"{title} ({page_number})", max__title_width, vertical_spacing * 1.5)
                    self.add_metadata(pdf, font_size-3, box_width)
                    pdf.set_fill_color(*color)
                    pdf.rect(140, 0, 10, 210, 'F')  # Thin color band on the right for A5
                    pdf.set_text_color(0, 0, 0)
                    pdf.set_font("OpenSans", size=font_size)

                pdf.rect(10, pdf.get_y(), box_width, section_height, 'D')  # Section box with dynamic height
                pdf.set_fill_color(*color)
                pdf.rect(10, pdf.get_y(), box_width, vertical_spacing, 'F')  # Section title background with less height
                pdf.set_font("Montserrat-Medium", size=font_size + 2)
                pdf.set_text_color(255, 255, 255)
                pdf.cell(box_width, vertical_spacing, txt=section['section'], ln=True, align='C')  # Less height for section title
                pdf.set_text_color(0, 0, 0)
                pdf.set_font("OpenSans", size=font_size)
                for procedure in filtered_procedures:
                    text_width = pdf.get_string_width(procedure['checklist_entry'])
                    lines = max(1, text_width // (box_width - bullet_spacing))
                    pdf.cell(bullet_spacing, vertical_spacing * lines, txt='o', ln=False)  # Unicode empty checkbox with less height
                    pdf.multi_cell(box_width - bullet_spacing, vertical_spacing, txt=procedure['checklist_entry'], ln=True)  # Wrap text
            pdf.ln(vertical_spacing)
        output_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', output_file)
        pdf.output(output_path)
        #os.system(f'chmod 666 {output_path}')  # Change the file permissions to be writable by the group

    def generate_procedure_pdf(self, output_file):
        ## STYLING
        font_size = 12
        section_font_size = 14
        vertical_spacing = 10
        single_par_spacing = 8
        right_margin = 20
        box_width = 200 - right_margin
        max__title_width = 125  # Set the maximum width for the title text box
        ## Code to generate the PDF
        pdf = FPDF(format='A4')
        pdf.set_right_margin(right_margin)  # Set the right margin to control text width
        pdf.add_font("OpenSans", "", self.font_path_open_sans_regular, uni=True)
        pdf.add_font("OpenSans", "B", self.font_path_open_sans_bold, uni=True)
        pdf.add_font("Montserrat-Bold", "", self.font_path_montserrat_bold, uni=True)
        pdf.add_font("Montserrat-Medium", "", self.font_path_montserrat_medium, uni=True)
        pdf.set_font("OpenSans", size=font_size)
        for checklist in self.checklists:
            title = checklist['title']
            color = checklist.get('color', [0, 0, 0])
            items = checklist['items']
            page_number = 1
            pdf.add_page()
            # Check if the section fits on the current page
            section_height = vertical_spacing  # Initialize section height
            for section in items:
                filtered_procedures = self.filter_procedures(section['procedures'])
                for procedure in filtered_procedures:
                    entry = procedure['checklist_entry']
                    description = procedure['procedure_description']
                    entry_height = -(-pdf.get_string_width(entry + ": " + description) // (box_width-7))
                    section_height += (entry_height - 1) * single_par_spacing + vertical_spacing
            if pdf.get_y() + section_height > pdf.h - pdf.b_margin:
                self.add_branding_banner(pdf, f"{title} ({page_number})", max__title_width, vertical_spacing)
            else:
                self.add_branding_banner(pdf, f"{title}", max__title_width, vertical_spacing)
            self.add_metadata(pdf, font_size-3, box_width)
            pdf.set_fill_color(*color)
            pdf.rect(200, 0, 10, 297, 'F')  # Thin color band on the right for A4
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("OpenSans", size=font_size)
            for section in items:
                section_height = vertical_spacing  # Initialize section height
                filtered_procedures = self.filter_procedures(section['procedures'])
                for procedure in filtered_procedures:
                    entry = procedure['checklist_entry']
                    description = procedure['procedure_description']
                    entry_height = -(-pdf.get_string_width(entry + ": " + description) // (box_width-10))
                    section_height += (entry_height - 1) * single_par_spacing + vertical_spacing

                # Check if the section fits on the current page
                if pdf.get_y() + section_height > pdf.h - pdf.b_margin:
                    # Add a new page if the section doesn't fit
                    page_number += 1
                    pdf.add_page()
                    self.add_branding_banner(pdf, f"{title} ({page_number})", max__title_width, vertical_spacing)
                    self.add_metadata(pdf, font_size-3, box_width)
                    pdf.set_fill_color(*color)
                    pdf.rect(200, 0, 10, 297, 'F')  # Thin color band on the right for A4
                    pdf.set_text_color(0, 0, 0)
                    pdf.set_font("OpenSans", size=font_size)

                pdf.rect(10, pdf.get_y(), box_width, section_height, 'D')  # Section box with dynamic height
                pdf.set_fill_color(*color)
                pdf.rect(10, pdf.get_y(), box_width, vertical_spacing, 'F')  # Section title background
                pdf.set_font("Montserrat-Medium", size=section_font_size)
                pdf.set_text_color(255, 255, 255)
                pdf.cell(box_width, vertical_spacing, txt=section['section'], ln=True, align='C')
                pdf.set_text_color(0, 0, 0)
                pdf.set_font("OpenSans", size=font_size)
                for procedure in filtered_procedures:
                    entry = procedure['checklist_entry']
                    description = procedure['procedure_description']
                    pdf.set_font("OpenSans", size=font_size, style='B')
                    pdf.write(single_par_spacing, f"{entry}: ")
                    pdf.set_font("OpenSans", size=font_size)
                    pdf.write(single_par_spacing, description)
                    pdf.ln(vertical_spacing)
            pdf.ln(vertical_spacing)
        output_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', output_file)
        pdf.output(output_path)
        #os.system(f'chmod 666 {output_path}')  # Change the file permissions to be writable by the group