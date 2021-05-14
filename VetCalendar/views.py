from django.shortcuts import render, redirect
from datetime import datetime, date
from .forms import ShiftForm, ShiftTypeForm, ScheduleShiftForm, RequestForm
from loginApp.forms import UpdateUserForm, UpdatePasswordForm
from loginApp.models import User, Address
from .models import Shift, ShiftType, ScheduleShift, Request
import bcrypt
from django.template import loader
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from dateutil import relativedelta


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
        cal_date = date.today()
        # year = cal_date.strftime('%Y')
        # month = cal_date.strftime('%m')
        # shifts = ScheduleShift.objects.filter(date__year=year, date__month=month)
        # events = {}
        # for shift in shifts:
        #     start_date = datetime.strftime(shift.date, "%Y-%m-%d")  
        #     new_event = {
        #         "title" : f'Dr. {shift.user.last_name}',
        #         "start" : start_date
        #     }

        context = {
            'cal_date': cal_date.strftime("%Y-%m-%d"),
            # 'schedule' : events,
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
        'shifts': Shift.objects.all(),
        'types': ShiftType.objects.all(),
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
        'schedule' : ScheduleShift.objects.all(),
    }
    return render(request, 'schedule.html', context)

def update_schedule(request):
    if request.method != 'POST':
        return redirect('/')
    form = ScheduleShiftForm(request.POST)
    if not form.is_valid():
        context = {
            'form' : form,
        }
        return render(request, 'schedule.html', context)       
    # print(request.POST)
    user = User.objects.get(id=request.POST['user'])
    shift = Shift.objects.get(id=request.POST['shift'])
    shift_type = ShiftType.objects.get(id=request.POST['shift_type'])
    shedule_shift = ScheduleShift.objects.create(date=request.POST['date'], shift=shift, shift_type=shift_type, user=user)
    return redirect('/schedule') 

def update_shifts(request):
    if request.method != 'POST':
        return redirect('/')
    form = ShiftForm(request.POST)
    if not form.is_valid():
        context = {
            'shift_form' : form,
        }
        return render(request, 'edit_shifts.html', context)
    start_time = get_ampm(request.POST['start_time'][:2])
    end_time = get_ampm(request.POST['end_time'][:2])
    # print(start_time + "-" + end_time)
    shift = Shift.objects.create(shift=start_time + "-" + end_time, start_time=request.POST['start_time'], end_time=request.POST['end_time'])
    return redirect('/manage_shifts') 

def get_ampm(time):
    time_s = int(time) - 12
    if 22 > int(time) > 11:        
        time_ampm = '0' + str(time_s) + 'pm'
    elif int(time) > 21:
        time_ampm = str(time_s) + 'pm'
    else:
        time_ampm = time + 'am'
    return time_ampm

def update_types(request):
    if request.method != 'POST':
        return redirect('/')
    form = ShiftTypeForm(request.POST)
    if not form.is_valid():
        context = {
            'type_form' : form,
        }
        return render(request, 'edit_shifts.html', context)
    shift_type = ShiftType.objects.create(name=request.POST['name'], color=request.POST['color'])
    return redirect('/manage_shifts') 

def get_shifts(request, date, change):       
    # print(date, change) 
    # if change == "next":        
    #     response = next_month(date)
    # elif change == "prev":
    #     response = prev_month(date)
    # else:
    # print(date)
    response = filter_shifts(date)    
    print(response)    
    return JsonResponse(response)

def next_month(date):
    cur_date = datetime.strptime(date, "%Y-%m-%d")    
    add_month = relativedelta.relativedelta(months=1)
    new_date = datetime.strftime(cur_date + add_month, "%Y-%m-%d")
    response = filter_shifts(new_date)
    return response

def prev_month(date):
    cur_date = datetime.strptime(date, "%Y-%m-%d")    
    add_month = relativedelta.relativedelta(months=1)
    new_date = datetime.strftime(cur_date - add_month, "%Y-%m-%d")
    response = filter_shifts(new_date)
    return response

def filter_shifts(new_date):
    date = datetime.strptime(new_date, "%Y-%m-%d")
    year = date.strftime('%Y')
    month = date.strftime('%m')
    shifts = ScheduleShift.objects.filter(date__year=year, date__month=month)        
    events = []
    i = 0
    for shift in shifts:
        start_date = datetime.strftime(shift.date, "%Y-%m-%d")  
        start_time = str(shift.shift.start_time)
        events.append({
                "title" : f'Dr. {shift.user.last_name}',
                "start" : start_date, 
                "time" : start_time,
        })
        i += 1     
    # print(events)
    response = {
        'cal_date': date.strftime("%Y-%m-%d"),
        'schedule' : events,
    }
    return response