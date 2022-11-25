import json
import requests
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, redirect, render)
from django.templatetags.static import static
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView
from django.db.models import Q
from .forms import *
from .models import *
from .forms import AdminRequestForm
from . import forms,models

def admin_home(request):
    total_projects = ConstructionProjects.objects.all().count()
    total_tasks = ArchitectTask.objects.all().count()
    total_engineer_task = EngineerTask.objects.all().count()
    total_incomplete = ArchitectTask.objects.filter(status="Incomplete").count()
    context = {
    'total_projects':total_projects,
    'total_tasks':total_tasks,
    'total_engineer_task':total_engineer_task,
    'total_incomplete':total_incomplete,
    }
    return render(request,'Client/home.html',context)

def addproect(request):
    form = ConstructionProjectsForm(request.POST,request.FILES or None)
    project_client = get_object_or_404(Client, admin_id=request.user.id)
    context = {
        'form': form,
        'projects': ConstructionProjects.objects.filter(project_client=project_client),
        # 'page_title': 'Projects'

    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.project_client = project_client
                obj.save()
                messages.success(
                    request, "Project submitted ")
                # return redirect(reverse('client_viewprojects'))
            except Exception:
                messages.error(request, "Could not Submit!")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "Client/addproject.html", context)

def addproject(request):
    user = request.user
    projects = Client.objects.filter(admin=user)
    # project_client = Client.objects.filter(admin_id=admin)
    if request.method  == "POST":
        descrition = request.POST.get('descrition')
        project = request.POST.get('project')
        project_client = request.POST.get('client')
        project_type = request.POST.get('project_type')
        srch = request.POST['project_type']
        # obj = project_client
        # obj.save()
        data = request.POST

        if data['project_client'] != 'none':
            project_client = Client.objects.get(id=data['project_client'])
            # form.save()
        else:    
            project_client = None

        report = ConstructionProjects.objects.create(
            descrition=descrition,
            project_client = project_client,
            project = project,
            project_type=project_type,

            )
        if srch:
            match = Architect.objects.filter(Q(project_type__icontains=srch)|
                                            Q(budget__icontains=srch))
            if match:
                return render(request,'Client/addproject.html',{'sr':match})
    context = {'projects':projects}            
    return render(request,'Client/addproject.html',context)


def updateproject(request, id):
    form =forms.AdminRequestForm()
    project = ConstructionProjects.objects.get(id=id)
    architects = Architect.objects.all()
    # engineers = Engineer.objects.all()
    context = {'project':project,'form':form,'architects':architects}

    if request.method == 'POST':
        form = forms.AdminRequestForm(request.POST,request.FILES)
        if form.is_valid():
            project_architect=form.cleaned_data['project_architect']
            project_eng = form.cleaned_data['project_eng']
            project_eng.save()
            project_architect.save()
        else:
            print("form is invalid")

    return render(request,'Client/updateproject.html',context)


def updateprojectdetails(request,id):    
    project = ConstructionProjects.objects.get(id=id)
    form = ConstructionForm(request.POST, request.FILES, instance=project)
    if form.is_valid():
        form.save()
        return redirect('client_viewprojects')
    return render(request,'Client/updateproject.html',{'project':project})

# def updateprojctdetails(request,id):    
#     project = ConstructionProjects.objects.get(id=id)
#     if request.method == 'POST':
#         descrition = request.POST.get('descrition')
#         project = request.POST.get('project')
#         project_type = request.POST.get('project_type')
#         project_architect = request.POST.get('project_architect')

#         report = ConstructionProjects.objects.create(
#             descrition=descrition,
#             project_architect = project_architect,
#             project = project,
#             project_type=project_type,

#             )    

#     return render(request,'Client/updateproject.html',{'project':project})
# @login_required
def deleteproject(request):
    id = request.GET.get('id',None)
    ConstructionProjects.objects.get(id=id).delete()
    response_data = {
        'deleted':True
    }
    return JsonResponse(response_data)


def add_staff(request):
    form = StaffForm(request.POST or None, request.FILES or None)
    context = {'form': form, 'page_title': 'Add Staff'}
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password')
            course = form.cleaned_data.get('course')
            passport = request.FILES.get('profile_pic')
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=2, first_name=first_name, last_name=last_name, profile_pic=passport_url)
                user.gender = gender
                user.address = address
                user.staff.course = course
                user.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_staff'))

            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Please fulfil all requirements")

    return render(request, 'hod_template/add_staff_template.html', context)


def add_student(request):
    student_form = StudentForm(request.POST or None, request.FILES or None)
    context = {'form': student_form, 'page_title': 'Add Student'}
    if request.method == 'POST':
        if student_form.is_valid():
            first_name = student_form.cleaned_data.get('first_name')
            last_name = student_form.cleaned_data.get('last_name')
            address = student_form.cleaned_data.get('address')
            email = student_form.cleaned_data.get('email')
            gender = student_form.cleaned_data.get('gender')
            password = student_form.cleaned_data.get('password')
            course = student_form.cleaned_data.get('course')
            session = student_form.cleaned_data.get('session')
            passport = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(
                    email=email, password=password, user_type=3, first_name=first_name, last_name=last_name, profile_pic=passport_url)
                user.gender = gender
                user.address = address
                user.student.session = session
                user.student.course = course
                user.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_student'))
            except Exception as e:
                messages.error(request, "Could Not Add: " + str(e))
        else:
            messages.error(request, "Could Not Add: ")
    return render(request, 'hod_template/add_student_template.html', context)




@csrf_exempt
def check_email_availability(request):
    email = request.POST.get("email")
    try:
        user = CustomUser.objects.filter(email=email).exists()
        if user:
            return HttpResponse(True)
        return HttpResponse(False)
    except Exception as e:
        return HttpResponse(False)


@csrf_exempt
def student_feedback_message(request):
    if request.method != 'POST':
        feedbacks = StudentProject.objects.all()
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Student Project Details'
        }
        return render(request, 'hod_template/student_feedback_template.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(StudentProject, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)

@csrf_exempt
def architect_task_message(request):
    client = get_object_or_404(Client, admin_id=request.user.id)
    if request.method != 'POST':
        feedbacks = ArchitectTask.objects.filter(constructionproject__project_client=client)
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Architect Task Details'
        }
        return render(request, 'Client/architect_task_template.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(ArchitectTask, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)


@csrf_exempt
def engineer_task_message(request):
    client = get_object_or_404(Client, admin_id=request.user.id)
    if request.method != 'POST':
        feedbacks = EngineerTask.objects.filter(constructionproject__project_client=client)
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Engineer Task Details'
        }
        return render(request, 'Client/engineer_task_template.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(EngineerTask, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)


@csrf_exempt
def architect_feedback_message(request):
    if request.method != 'POST':
        feedbacks = FeedbackArchitect.objects.all()
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Architect Feedback Messages'
        }
        return render(request, 'Client/architect_feedback_template.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(FeedbackArchitect, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)

@csrf_exempt
def engineer_feedback_message(request):
    if request.method != 'POST':
        feedbacks = FeedbackEngineer.objects.all()
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Engineer Feedback Messages'
        }
        return render(request, 'Client/engineer_feedback_template.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(FeedbackEngineer, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)





def admin_view_profile(request):
    admin = get_object_or_404(Admin, admin=request.user)
    form = AdminForm(request.POST or None, request.FILES or None,
                     instance=admin)
    context = {'form': form,
               'page_title': 'View/Edit Profile'
               }
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                passport = request.FILES.get('profile_pic') or None
                custom_user = admin.admin
                if password != None:
                    custom_user.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    custom_user.profile_pic = passport_url
                custom_user.first_name = first_name
                custom_user.last_name = last_name
                custom_user.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('admin_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
        except Exception as e:
            messages.error(
                request, "Error Occured While Updating Profile " + str(e))
    return render(request, "hod_template/admin_view_profile.html", context)


def admin_notify_architect(request):
    archictect = CustomUser.objects.filter(user_type=2)
    context = {
        'page_title': "Send Notifications To Architect",
        'allarchictect': archictect
    }
    return render(request, "Client/architect_notification.html", context)


def admin_notify_engineer(request):
    engineer = CustomUser.objects.filter(user_type=3)
    context = {
        'page_title': "Send Notifications To Contractor",
        'engineers': engineer
    }
    return render(request, "Client/engineer_notification.html", context)


@csrf_exempt
def send_engineer_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    engineer = get_object_or_404(Engineer, admin_id=id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': "Construction Management System",
                'body': message,
                'click_action': reverse('engineer_view_notification'),
                'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': engineer.admin.fcm_token
        }
        headers = {'Authorization':
                   'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationEngineer(engineer=engineer, message=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


@csrf_exempt
def send_architect_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    archictect = get_object_or_404(Architect, admin_id=id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': "Construction Management System",
                'body': message,
                # 'click_action': reverse('staff_view_notification'),
                'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': archictect.admin.fcm_token
        }
        headers = {'Authorization':
                   'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationArchitect(archictect=archictect, message=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")




def client_viewprojects(request):
    # client = get_object_or_404(Client, admin=request.user)
    project = ConstructionProjects.objects.all()
    return render(request,'Client/viewprojects.html',{'project':project})


def student_feedback(request):
    form = ProjectStudentForm(request.POST,request.FILES or None)
    student = get_object_or_404(Student, admin_id=request.user.id)
    context = {
        'form': form,
        'projects': StudentProject.objects.filter(student=student),
        'page_title': 'Student Project'

    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.student = student
                obj.save()
                messages.success(
                    request, "Project submitted for review")
                return redirect(reverse('student_feedback'))
            except Exception:
                messages.error(request, "Could not Submit!")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "student_template/student_feedback.html", context)
