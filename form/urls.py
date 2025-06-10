from django.urls import path
from .views import create_cv, PreviewCV, export_pdf,save_to_json, import_json_to_form,form_view

app_name = 'app_form'

urlpatterns = [
    path('', create_cv, name='create_cv'),
    path('preview/<slug:slug>/', PreviewCV.as_view(), name='preview'),
    path('export/<int:cv_id>/', export_pdf, name='export_pdf'),
    path('savejson/<slug:slug>/',save_to_json,name='savejson'),
    path('upload-json-form/', import_json_to_form, name='upload_json_form'),
    path('form/', form_view, name='form_view'),
]
