import json
import math
from datetime import datetime

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,
                              redirect, render)
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .forms import *
from .models import *


def architect_home(request):
    architect = get_object_or_404(Architect, admin_id=request.user.id)
    total_projects = ConstructionProjects.objects.filter(project_architect=architect).count()
    total_tasks = ArchitectTask.objects.filter(constructionproject__project_architect=architect).count()
    total_completed = ArchitectTask.objects.filter(constructionproject__project_architect=architect,status="Complete").count()
    total_incomplete = ArchitectTask.objects.filter(constructionproject__project_architect=architect,status="Incomplete").count()

    context={
    'total_projects':total_projects,
    'total_tasks':total_tasks,
    'total_completed':total_completed,
    'total_incomplete':total_incomplete,
    }
    return render(request, 'architect/architect_content.html',context)



def architect_project(request):
    # form = ProjectStudentForm(request.POST,request.FILES or None)
    architect = get_object_or_404(Architect, admin_id=request.user.id)
    context = {
        # 'form': form,
        'projects': ConstructionProjects.objects.filter(project_architect=architect),
        'page_title': 'Architect Project'

    }
    # if request.method == 'POST':
    #     if form.is_valid():
    #         try:
    #             obj = form.save(commit=False)
    #             obj.student = student
    #             obj.save()
    #             messages.success(
    #                 request, "Project submitted for review")
    #             return redirect(reverse('student_feedback'))
    #         except Exception:
    #             messages.error(request, "Could not Submit!")
    #     else:
    #         messages.error(request, "Form has errors!")
    return render(request, "architect/architect_view_project.html", context)

def architect_details(request):
    admin = get_object_or_404(Architect, admin_id=request.user.id)
    form = ArchitectEditForm(request.POST or None, request.FILES or None)
    # architect = CustomUser.objects.filter(architect=request.user)
    context = {
          'form':form,
          'admins':Architect.objects.filter(admin=request.user),
          # 'page_title':'architect details'
    }
    if request.method == 'POST':
        if form.is_valid():
            admin = form.cleaned_data['admin']
            admin.save()
            try:
                obj.form.save(commit=False)
                obj.admin = admin
                obj.save()
                messages.success(
                    request,"Saved")
                return redirect(reverse('architect_details'))
            except Exception:
                messages.error(request,"form error")
        else:
            messages.error(request,"c")
    return render(request,'architect/views.html',context)

def architect_task(request):
    architect = get_object_or_404(Architect, admin_id=request.user.id)
    form = TaskArchitectForm(request.POST,request.FILES or None)
    context = {
        'form': form,
        'archictect': ArchitectTask.objects.filter(constructionproject__project_architect=architect),   
        'page_title': 'Architect Project Tasks'

    }
    if request.method == 'POST':
        if form.is_valid():
            
            architect = form.cleaned_data['constructionproject']
            architect.save()
            try:
                obj = form.save(commit=False)
                obj.architect = architect
                obj.save()
                messages.success(
                    request, "Task submitted for review by client")
                return redirect(reverse('architect_task'))
            except Exception:
                messages.error(request, "Could not Submit!")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "architect/architect_task.html", context)



def architect_view_profile(request):
    architect = get_object_or_404(Architect, admin=request.user)
    form = ArchitectEditForm(request.POST or None, request.FILES or None,
                           instance=architect)
    context = {'form': form,
               'page_title': 'Update Architect Details'
               }
    if request.method == 'POST':
        try:
            if form.is_valid():
                # first_name = form.cleaned_data.get('first_name')
                # last_name = form.cleaned_data.get('last_name')
                # password = form.cleaned_data.get('password') or None
                # address = form.cleaned_data.get('address')
                # gender = form.cleaned_data.get('gender')
                # passport = request.FILES.get('profile_pic') or None
                # admin = architect.admin
                # if password != None:
                #     admin.set_password(password)
                # if passport != None:
                #     fs = FileSystemStorage()
                #     filename = fs.save(passport.name, passport)
                #     passport_url = fs.url(filename)
                #     admin.profile_pic = passport_url
                # admin.first_name = first_name
                # admin.last_name = last_name
                # admin.address = address
                # admin.gender = gender
                # admin.save()
                architect.save()
                messages.success(request, "Profile Updated!")
                # return redirect(reverse('architect_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
        except Exception as e:
            messages.error(request, "Error Occured While Updating Profile " + str(e))

    return render(request, "architect/architect_view_profile.html", context)


@csrf_exempt
def architect_fcmtoken(request):
    token = request.POST.get('token')
    archictect_user = get_object_or_404(CustomUser, id=request.user.id)
    try:
        archictect_user.fcm_token = token
        architect_user.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


def architect_view_notification(request):
    archictect = get_object_or_404(Architect, admin=request.user)
    notifications = NotificationArchitect.objects.filter(archictect=archictect)
    context = {
        'notifications': notifications,
        'page_title': "View Notifications"
    }
    return render(request, "architect/architect_view_notification.html", context)


