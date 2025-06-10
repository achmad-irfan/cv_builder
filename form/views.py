from django.conf import settings
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.urls import reverse
from .models import CV, Education,Skill,Experience,Certificate
from .form import CVForm, EducationFormSet,Education,SkillFormSet,ExperienceFormSet,CertificateFormSet, EducationForm, ExperienceForm, SkillForm, CertificateForm
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
import os
import json
from django.forms import modelformset_factory

def create_cv(request):
    if request.method == 'POST':
        cv_form = CVForm(request.POST)
        education_formset = EducationFormSet(request.POST, prefix='education')
        experience_formset = ExperienceFormSet(request.POST, prefix='experience')
        skill_formset = SkillFormSet(request.POST, prefix='skill')
        certificate_formset = CertificateFormSet(request.POST, prefix='certificate')

        if (
            cv_form.is_valid()
            and education_formset.is_valid()
            and experience_formset.is_valid()
            and skill_formset.is_valid()
            and certificate_formset.is_valid()
        ):
            cv = cv_form.save()

            # Save only filled education
            for form in education_formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    edu = form.save(commit=False)
                    if edu.school_name:
                        edu.cv = cv
                        edu.save()

            # Save experience
            for form in experience_formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    exp = form.save(commit=False)
                    if exp.experience_name:
                        exp.cv = cv
                        exp.save()

            # Save skill
            for form in skill_formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    skill = form.save(commit=False)
                    if skill.skill_name:
                        skill.cv = cv
                        skill.save()

            # Save certificate
            for form in certificate_formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    cert = form.save(commit=False)
                    if cert.certificate_name:
                        cert.cv = cv
                        cert.save()

            return redirect('app_form:preview', slug=cv.slug)

    else:
        # GET
        cv_form = CVForm()
        education_formset = EducationFormSet(queryset=Education.objects.none(), prefix='education')
        experience_formset = ExperienceFormSet(queryset=Experience.objects.none(), prefix='experience')
        skill_formset = SkillFormSet(queryset=Skill.objects.none(), prefix='skill')
        certificate_formset = CertificateFormSet(queryset=Certificate.objects.none(), prefix='certificate')

    return render(request, 'form/index.html', {
        'cv_form': cv_form,
        'education_formset': education_formset,
        'experience_formset': experience_formset,
        'skill_formset': skill_formset,
        'certificate_formset': certificate_formset,
    })



class PreviewCV(DetailView):
    model = CV
    template_name = 'form/preview.html'
    context_object_name = 'CV'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

def export_pdf(request, cv_id):
    cv = CV.objects.get(id=cv_id)
    selected_file=request.GET.get("style","cv_style1")
    css_filename=f"{selected_file}.css"
    css_path = os.path.join(settings.BASE_DIR, 'form', 'static', 'form', 'css', css_filename)
    html_string = render_to_string('form/cv.html', {'CV': cv})
    css_file = CSS(filename=css_path)
    pdf_file = HTML(string=html_string).write_pdf(stylesheets=[css_file])

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="cv.pdf"'
    return response



def save_to_json(request, slug):
    cv = CV.objects.get(slug=slug)

    data = {
        "cv": {
            "name": cv.name,
            "roles": cv.roles,
            "location": cv.location,
            "email": cv.email,
            "telp": cv.telp,
            "web": cv.web,
            "summary": cv.summary
        },
        "education": list(cv.education.values()),
        "experience": list(cv.experience.values()),
        "skill": list(cv.skill.values()),
        "certificate": list(cv.certificate.values())
    }

    response = HttpResponse(
        json.dumps(data, indent=4),
        content_type='application/json'
    )
    response['Content-Disposition'] = f'attachment; filename="{slug}.json"'
    return response


def form_view(request):
    data = request.session.pop('cv_json_data', None)
    cv_form = CVForm()
    education_formset = EducationFormSet(queryset=Education.objects.none(), prefix='education')
    skill_formset = SkillFormSet(queryset=Skill.objects.none(), prefix='skill')
    certificate_formset = CertificateFormSet(queryset=Certificate.objects.none(), prefix='certificate')
    experience_formset = ExperienceFormSet(queryset=Experience.objects.none(), prefix='experience')

    if data:
        # Isi CVForm
        cv_form = CVForm(initial=data.get('cv', {}))

        # Helper: fungsi filter fields
        def filter_fields(item, allowed_fields):
            return {k: v for k, v in item.items() if k in allowed_fields}

        # Education
        education_fields = [f.name for f in EducationForm._meta.model._meta.fields if f.name != 'cv']
        education_items = [filter_fields(e, education_fields) for e in data.get('education', [])]
        education_formset = EducationFormSet(initial=education_items, queryset=Education.objects.none(), prefix='education')

        # Skill
        skill_fields = [f.name for f in SkillForm._meta.model._meta.fields if f.name != 'cv']
        skill_items = [filter_fields(s, skill_fields) for s in data.get('skill', [])]
        skill_formset = SkillFormSet(initial=skill_items, queryset=Skill.objects.none(), prefix='skill')

        # Certificate
        certificate_fields = [f.name for f in CertificateForm._meta.model._meta.fields if f.name != 'cv']
        certificate_items = [filter_fields(c, certificate_fields) for c in data.get('certificate', [])]
        certificate_formset = CertificateFormSet(initial=certificate_items, queryset=Certificate.objects.none(), prefix='certificate')

        # Experience
        experience_fields = [f.name for f in ExperienceForm._meta.model._meta.fields if f.name != 'cv']
        experience_items = [filter_fields(e, experience_fields) for e in data.get('experience', [])]
        experience_formset = ExperienceFormSet(initial=experience_items, queryset=Experience.objects.none(), prefix='experience')

    context = {
        'cv_form': cv_form,
        'education_formset': education_formset,
        'skill_formset': skill_formset,
        'certificate_formset': certificate_formset,
        'experience_formset': experience_formset,
    }

    return render(request, 'form/index.html', context)



def import_json_to_form(request):
    if request.method == 'POST' and request.FILES.get('json_file'):
        json_file = request.FILES['json_file']
        try:
            data = json.load(json_file)
        except json.JSONDecodeError:
            return redirect('app_form:form_view')

        # Simpan ke session
        request.session['cv_json_data'] = data
        return redirect('app_form:form_view')

    return redirect('app_form:form_view')





# from django.conf import settings
# from django.shortcuts import render,redirect
# from django.views.generic.edit import CreateView
# from django.views.generic.detail import DetailView
# from django.urls import reverse
# from .models import CV
# from .form import CVForm, EducationFormSet,Education
# from django.template.loader import render_to_string
# from weasyprint import HTML, CSS
# from django.http import HttpResponse
# import os


# # class CVCreateView(CreateView):
# #     model = CV
# #     form_class = CVForm
# #     template_name = 'form/index.html'

# #     def get_success_url(self):
# #         # Arahkan ke halaman preview dengan pk dari data yang baru dibuat
# #         return reverse('app_form:preview', kwargs={'slug': self.object.slug})


# class PreviewCV(DetailView):
#     model = CV
#     template_name = 'form/preview.html'
#     context_object_name = 'CV'  # supaya di template bisa pakai {{ cv.name }} dll
#     slug_field = 'slug'
#     slug_url_kwarg = 'slug'

# def export_pdf(request, cv_id):
#     cv = CV.objects.get(id=cv_id)
#     html_string = render_to_string('form/cv.html', {'CV':cv})
#     css_path = os.path.join(settings.BASE_DIR, 'form','static', 'form', 'css', 'cv.css')
#     css_file = CSS(filename=css_path)
#     pdf_file = HTML(string=html_string).write_pdf(stylesheets=[css_file])
    
#     response = HttpResponse(pdf_file, content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="cv.pdf"'
#     return response



# def create_cv_with_education(request):
#     if request.method == 'POST':
#         cv_form = CVForm(request.POST)
#         edu_formset = EducationFormSet(request.POST, queryset=Education.objects.none())

#         if cv_form.is_valid() and edu_formset.is_valid():
#             cv = cv_form.save()
#             educations = edu_formset.save(commit=False)
#             for edu in educations:
#                 edu.cv = cv
#                 edu.save()
#             return redirect('success_page')  # Ganti dengan nama URL kamu

#     else:
#         cv_form = CVForm()
#         edu_formset = EducationFormSet(queryset=Education.objects.none())

#     return render(request, 'form/index.html', {
#         'cv_form': cv_form,
#         'edu_formset': edu_formset,
#     })

