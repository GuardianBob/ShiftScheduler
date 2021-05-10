from django.shortcuts import render, redirect
import datetime
from .forms import ShiftForm, ShiftTypeForm, ScheduleShiftForm, RequestForm
from loginApp.forms import UpdateUserForm, UpdatePasswordForm
from loginApp.models import User, Address
from .models import Shift, ShiftType, ScheduleShift, Request
import bcrypt
from django.template import loader
from django.http import JsonResponse, HttpResponseRedirect

def validate_user(request):
    if not 'user_id' in request.session:
        return redirect('/')

def validate_admin(request):
    validate_user(request)
    user_id = request.session['user_id']
    if not validate_level(user_id) is True:
        return redirect('/')

def index(request):
    if not 'user_id' in request.session:
        return redirect('/login')
    else:
        context = {

        }
        return render(request, 'calendar.html', context)

def get_nav(request):
    nav = 'nav_out.html'
    if 'user_id' in request.session:
        nav = "nav_in.html"
    return nav

def validate_level(user_id):
    user = User.objects.get(id=user_id)
    return user.user_level

def admin(request):    
    context = {
        'page_title' : 'Admin Dashboard',        
    }

def render_edit_page(request, context, user_id):
    current_user = User.objects.get(id=request.session['user_id'])
    if validate_user(current_user.id) is True:
        user = User.objects.get(id=user_id)
        form_title = user.full_name + ' : User ' + str(user_id)
    else:
        user = User.objects.get(id=request.session['user_id'])
        form_title = 'Profile'    
    user_level = "Normal"
    if current_user.user_level is True:
        user_level = "Admin"
    add_info = {
        'nav': get_nav(request),
        # 'admin' : current_user.user_level,
        'user': user,
        # 'user_id': current_user.id,
        'current_user': current_user,
        'user_id': current_user.id,
        'form_title': form_title,
        'page_title': 'Edit' + form_title,
        'level_select': {False:'Normal',True:'Admin'},
    }
    context.update(add_info)
    return render(request, 'edit_user.html', context)

def success(request, user_id):
    context = {
        'form' : UpdateUserForm(),
        'password_form' : UpdatePasswordForm(),
        'update': 'Update successful!',
        }
    return render_edit_page(request, context, user_id)

def update_password(request):
    if request.method != "POST":
        return redirect("/register")
    check_form = UpdatePasswordForm(request.POST)
    if not check_form.is_valid():
        # password_form = Register_Form()
        context = { 
            'password_form' : check_form,
            'form': UpdateUserForm(),
            # 'user_id': request.POST['user_id'],
            }
        return render_edit_page(request, context, request.POST['user_id'])
    else:
        user = User.objects.get(id=request.POST['user_id'])
        password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user.password = password
        user.save()
        print('success!')
        return success(request, request.POST['user_id'])

def edit_user(request, user_id):
    context = {
        'form' : UpdateUserForm(),
        'password_form' : UpdatePasswordForm(),
        'update': '',        
    }    
    return render_edit_page(request, context, user_id)

def update_user(request):
    if request.method != "POST":
        return redirect("/login/register")
    if request.POST['user_id'] == '2' or request.POST['user_id'] == '3':
        return redirect('/dashboard')
    check_form = UpdateUserForm(request.POST)
    if not check_form.is_valid():
        print(check_form)
        context = { 
            'password_form' : UpdatePasswordForm(),
            'form': check_form,
            # 'user_id': request.POST['user_id'],                       
            }
        return render_edit_page(request, context, request.POST['user_id'])
    else:
        # print(request.POST)
        user = User.objects.get(id=request.POST['user_id'])
        user.email = request.POST['email']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.user_type = request.POST['user_type']
        # user.user_level = request.POST['user_level']
        user.save()
        if request.POST['address'] != '':            
            address = Address.ogjects.filter(user=user)   
            addr_split = request.POST['address'].split(" ", 1)
            address.number = addr_split[0]
            address.street = addr_split[1]
            address.street2 = request.POST['address_line2']
            address.apt_num = request.POST['apt_num']
            address.city = request.POST['city']
            address.state = request.POST['state']
            address.zipcode = request.POST['zipcode']
            address.save()
        print('success!')
        return success(request, request.POST['user_id'])

def remove_user(request, remove_id):
    validate_admin()
    user_id = request.session['user_id']
    if remove_id == '2' or remove_id == '3':
        return redirect('/')
    remove = User.objects.get(id=remove_id)
    remove.delete()
    return redirect('/dashboard/')

def manage_users(request):
    pass

def manage_shifts(request):
    validate_admin(request)
    user_id = request.session['user_id']
    context = {
        'shift_form' : ShiftForm(),
        'type_form' : ShiftTypeForm(),
    }
    return render(request, 'edit_shifts.html', context)

def totals(request):
    pass

def sched_list(request):
    pass

def schedule_shifts(request):
    validate_admin(request)
    user_id = request.session['user_id']
    context = {
        'form' : ScheduleShiftForm(),
        'action': 'update_schedule',
    }
    return render(request, 'schedule.html', context)

def update_schedule(request):
    pass