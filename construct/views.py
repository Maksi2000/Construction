from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import render,redirect,reverse
from django.db.models import Q
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from  django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.shortcuts import render,redirect,reverse
# from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
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

# from .forms import ClientUserForm,ArchitectUserForm,ConstructionProjectForm
from .models import *
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
# Create your views here.


def homepage(request):
	return render(request,'pages/home.html')

# def home(request):
# 	return render(request,'Client/home.html')





	