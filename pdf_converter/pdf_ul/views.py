from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.generic import View
import datetime
import os
import django.contrib.messages as messages
import pdf_converter.utils as  converter

async def home(request):    
    return render(request, 'home.html')    

async def pdf_converter(request):
    if request.method == 'POST':        
        try:            
            uploaded_files = request.FILES.getlist('document')         
            if len(uploaded_files) == 0:          
                context = {
                "messege": "You didn't pick any files",
                }
                messages.add_message(request, messages.ERROR, context)
                return render(request, 'pdf/pdf.html',context)  
            pdf = converter.image_to_pdf(uploaded_files)          
            context = {
            'pdf': pdf,  
            }            
            return render(request, 'pdf/return_pdf.html', context)        
        except:
            context = {
                "messege": "Something Went Wrong",
            }
            messages.add_message(request, messages.ERROR, context)
            return render(request, 'pdf/pdf.html', context)      
    else:        
        return render(request, 'pdf/pdf.html')     


async def download_file(request):    
    if request.method == "POST":       
        file_name = request.POST['file_name']
        save_file_path = converter.get_dir_path()       
        file_path = save_file_path + file_name
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/force_download")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                temp = converter.remove_file_by_name(file_name)
                return response
    raise Http404

async def download_zip(request):
    if request.method == "POST": 
            try:       
                #file_path = converter.make_zip()
                file_path = converter.make_zip_using_zipfile()
                if file_path != False:
                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as fh:
                            response = HttpResponse(fh.read(), content_type="application/force_download")
                            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                            temp = converter.remove_file_by_path(file_path)
                            dir_path = converter.get_dir_path()
                            switch = converter.remove_all_files_from_dir(dir_path)
                            print(temp)
                            return response
                    else:
                        context = {
                            "messege": "Files doesn't exist",
                        }  
                        messages.add_message(request, messages.ERROR, context)                  
                        return render(request, 'pdf/pdf.html', context)
                else:
                    context = {
                            "messege": "Can't create archivum",
                        } 
                    messages.add_message(request, messages.ERROR, context)                   
                    return render(request, 'pdf/pdf.html', context)
            except:
                context = {
                        "messege": "Something went wrong",
                    } 
                messages.add_message(request, messages.ERROR, context)                   
                return render(request, 'pdf/pdf.html', context)
    raise Http404


async def download_tar(request):
    if request.method == "POST": 
            try:       
                file_path = converter.make_tar()
                if file_path != False:
                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as fh:
                            response = HttpResponse(fh.read(), content_type="application/force_download")
                            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                            temp = converter.remove_file_by_path(file_path)
                            dir_path = converter.get_dir_path()
                            switch = converter.remove_all_files_from_dir(dir_path)
                            print(temp)
                            return response
                    else:
                        context = {
                            "messege": "Files doesn't exist",
                        }          
                        messages.add_message(request, messages.ERROR, context)          
                        return render(request, 'pdf/pdf.html', context)
                else:
                    context = {
                            "messege": "Can't create archivum",
                        } 
                    messages.add_message(request, messages.ERROR, context)                   
                    return render(request, 'pdf/pdf.html', context)
            except:
                context = {
                        "messege": "Something went wrong",
                    }      
                messages.add_message(request, messages.ERROR, context)               
                return render(request, 'pdf/pdf.html', context)
    raise Http404

async def clear(request):
    if request.method == "POST":
        try:
            dir_path = converter.get_dir_path()
            if os.path.exists(dir_path):
                switch = converter.remove_all_files_from_dir(dir_path)
                context = {
                    'messege': 'Already cleaned',
                }
                messages.add_message(request, messages.ERROR, context) 
                return render(request, 'home.html', context)            
        except:
            context = {
                        "messege": "Something went wrong",
                    }                    
            messages.add_message(request, messages.ERROR, context)       
            return render(request, 'pdf/pdf.html', context)
    raise Http404