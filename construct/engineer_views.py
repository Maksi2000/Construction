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

def engineer_home(request):
    engineer = get_object_or_404(Engineer, admin_id=request.user.id)
    total_projects = ConstructionProjects.objects.filter(project_eng=engineer).count()
    total_tasks = EngineerTask.objects.filter(constructionproject__project_eng=engineer).count()
    # total_completed = EngineerTask.objects.filter(constructionproject__project_eng=engineer,status="Complete").count()
    # total_incomplete = EngineerTask.objects.filter(constructionproject__project_eng=engineer,status="Incomplete").count()

    context={
    'total_projects':total_projects,
    'total_tasks':total_tasks,
    # 'total_completed':total_completed,
    # 'total_incomplete':total_incomplete,
    }
    return render(request, 'engineer/engineer_content.html',context)


def engineer_project(request):
    # form = ProjectStudentForm(request.POST,request.FILES or None)
    engineer = get_object_or_404(Engineer, admin_id=request.user.id)
    context = {
        # 'form': form,
        'projects': ConstructionProjects.objects.filter(project_eng=engineer),
        # 'page_title': 'Engineer Project'

    }
    return render(request, "engineer/engineer_view_project.html", context)

def engineer_task(request):
    engineer = get_object_or_404(Engineer, admin_id=request.user.id)
    form = TaskEngineerForm(request.POST,request.FILES or None)
    context = {
        'form': form,
        'engineer': EngineerTask.objects.filter(constructionproject__project_eng=engineer),   
        # 'page_title': 'Engineer Project Tasks'

    }
    if request.method == 'POST':
        if form.is_valid():
            
            engineer = form.cleaned_data['constructionproject']
            engineer.save()
            try:
                obj = form.save(commit=False)
                obj.engineer = engineer
                obj.save()
                messages.success(
                    request, "Task submitted for review by client")
                return redirect(reverse('engineer_task'))
            except Exception:
                messages.error(request, "Could not Submit!")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "engineer/engineer_task.html", context)


def engineer_view_profile(request):
    admin = get_object_or_404(Engineer, admin=request.user)
    form = EngineerEditForm(request.POST or None, request.FILES or None,
                           instance=admin)
    context = {'form': form,
               'admins':Engineer.objects.filter(admin=request.user),
               'page_title': 'Update Engineer Details'
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
                admin.save()
                messages.success(request, "Profile Updated!")
                # return redirect(reverse('architect_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
        except Exception as e:
            messages.error(request, "Error Occured While Updating Profile " + str(e))

    return render(request, "engineer/engineer_view_profile.html", context)


@csrf_exempt
def engineer_fcmtoken(request):
    token = request.POST.get('token')
    engineer_user = get_object_or_404(CustomUser, id=request.user.id)
    try:
        engineer_user.fcm_token = token
        engineer_user.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


def engineer_view_notification(request):
    engineer = get_object_or_404(Engineer, admin=request.user)
    notifications = NotificationEngineer.objects.filter(engineer=engineer)
    context = {
        'notifications': notifications,
        'page_title': "View Notifications"
    }
    return render(request, "engineer/engineer_view_notification.html", context)
