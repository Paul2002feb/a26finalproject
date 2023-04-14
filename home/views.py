from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import generic
from allauth.account.views import SignupView
from allauth.socialaccount.views import SignupView as SocialSignupView
import requests
from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignup
from .forms import *
from django.forms.widgets import HiddenInput
from django.http import HttpResponse
from .models import *
from django.db.models.functions import Lower
from django.db.models import Q


# Create your views here.
def home(request):
    return render(request,'home/index.html')

def login(request):
    return render(request, 'home/login.html')

def notification_page(request):
    return render(request,'home/notificationpage.html')

def schedule_page(request):
    return render(request,'home/schedulepage.html')

def profile_page(request):
    return render(request,'home/profilepage.html')

def search_tutors(request):
    if request.method == 'POST':
        tutor_id = request.POST.get('tutor_id')
        tutor = TutoringUser.objects.filter(id=tutor_id).first()
        print(tutor.user,'diwhefidwj')
        if tutor:
            session_date = request.POST.get('session_date')
            session_time = request.POST.get('session_time')
            pay_rate = request.POST.get('pay_rate')
            student = request.user
            tutor_request = TutorRequest.objects.create(
                student=student,
                tutor=tutor.user,
                session_date=session_date,
                session_time=session_time,
                pay_rate=pay_rate,
                status='pending'
            )
            print(tutor_request)
            tutor_request.save()
            return redirect('/tutorsearch')  # replace with the appropriate URL for the student dashboard
        else:
            print('failed')
            return render(request, 'home/tutorsearch.html', {'error': 'Tutor not found'})
    elif request.method == 'GET':
        input = request.GET.get('search-input')
        if input is None:
            return render(request, 'home/tutorsearch.html', {'tutor_list': []})
        else:
            tutor_list = TutoringUser.objects.filter(
                Q(full_name__icontains=input) | Q(pay_rate__icontains=input) | Q(major__icontains=input) | Q(classes__icontains=input)
            )
            return render(request, 'home/tutorsearch.html', {'tutor_list': tutor_list})
    return render(request,'home/tutorsearch.html')



def view_requests(request):
    my_user = TutoringUser.objects.filter(user=request.user).first()
    print(my_user.is_tutor)
    if my_user.is_tutor == True:
        if request.method == 'GET':
            # request_list = TutorRequest.objects.get(request_user=request.user.username)
            request_list = TutorRequest.objects.filter(tutor=request.user)
            print(request_list,'udgwgduwgf')
            return render(request,'home/requestIndex.html', {'request_list' : request_list})
        
        if request.method == 'POST':
            request_id = request.POST.get('request_id')
            print(request_id)
            status = request.POST.get('status')
            try:
                tutor_request = TutorRequest.objects.get(id=request_id)
                # Update the status of the tutor_request
                tutor_request.status = status
                tutor_request.save()
                print(tutor_request.status)
                return redirect("/requestlist")  # Redirect to the request list page after successful update
            except TutorRequest.DoesNotExist:
                print('pass')
                pass  # Handle case where request_id does not exist
                print('pass')
    elif my_user.is_tutor == False:
        if request.method == 'GET':
            # request_list = TutorRequest.objects.get(request_user=request.user.username)
            request_list = TutorRequest.objects.filter(student=request.user)
            print(request_list,'udgwgduwgf')
            return render(request,'home/requestIndex.html', {'request_list' : request_list})
        
        if request.method == 'PUT':
            request_id = request.POST.get('request_id')
            status = request.POST.get('status')
            try:
                tutor_request = TutorRequest.objects.get(id=request_id)
                # Update the status of the tutor_request
                tutor_request.status = status
                tutor_request.save()
                return redirect(request,'home/requestIndex.html')  # Redirect to the request list page after successful update
            except TutorRequest.DoesNotExist:
                pass  # Handle case where request_id does not exist
                print('pass')
                    

def search_courses(request):
    tutoring_user = request.user.tutoringuser
    if request.method == 'GET':
        input = request.GET.get('search-input')
        if input is None:
            return render(request, 'home/courses.html', {'courses': []})
        else:
            input_args = input.split()
            len_input = len(input_args)
            if len_input == 1:
                course_num = input_args[0]
                url = f'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1232&class_nbr={course_num}'
                r = requests.get(url)
            elif len_input == 2:  # Use 'elif' instead of 'if' for multiple conditions
                department = input_args[0]
                department = department.upper()
                mneomonic = input_args[1]
                url = f'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1232&subject={department}&catalog_nbr={mneomonic}'
                r = requests.get(url)
            else:  
                name = input.replace(" ","+")
                url = f'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1232&keyword={name}'
                r = requests.get(url)
                
            courses = r.json()
            return render(request, 'home/courses.html', {'courses': courses})
    
    elif request.method == 'POST': 
        print("add is being clicked")
        selected_courses = request.POST.getlist('selected_courses')
        for course in selected_courses:
            tutoring_user.classes.append(course)
        tutoring_user.save()
        return HttpResponseRedirect('/profile/')
    else:
        return render(request, 'home/courses.html', {'courses': []})

class IndexView(generic.ListView):
    template_name = 'home/index.html'

class TutoringUserSignupView(SignupView):
    template_name = 'home/login.html'
    form_class = SignupForm
    view_name = 'tutoring_signup'

def tutor(request):
    if request.method == 'POST':
        form = TutorForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('/')
    else:
        form = TutorForm({'user': request.user})
        form.fields['user'].widget = HiddenInput()
    return render(request, 'home/tutorform.html', {'form':form})

def edit_profile(request):
    tutoring_user = request.user.tutoringuser
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        major = request.POST.get('major')
        pay_rate = request.POST.get('pay_rate')
        is_virtual = request.POST.get('is_virtual')
        new_location = request.POST.get('new_location') 
        locations_to_remove = request.POST.getlist('remove_location')
        if 'is_virtual' in request.POST and request.POST['is_virtual'] == 'true':
            is_virtual = True
        else:
            is_virtual = False

        if new_location:
            tutoring_user.locations.append(new_location)

        if locations_to_remove:
            for location in locations_to_remove:
                tutoring_user.locations.remove(location)

        # Update the TutoringUser object with the new values
        TutoringUser.objects.filter(pk=tutoring_user.pk).update(
            full_name=full_name,
            major=major,
            pay_rate=pay_rate,
            is_virtual=is_virtual,
            locations=tutoring_user.locations
        )

        return HttpResponseRedirect('/profile/')
    else:
        form_data = {
            'full_name': tutoring_user.full_name,
            'major': tutoring_user.major,
            'pay_rate': tutoring_user.pay_rate,
            'is_virtual': tutoring_user.is_virtual,
            'locations': tutoring_user.locations,
        }
        form = TutorForm(initial=form_data)

    return render(request, 'home/editprofile.html', {'form': form, 'tutoring_user': tutoring_user})
