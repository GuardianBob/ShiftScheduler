from django.shortcuts import render, redirect
from datetime import datetime, date, timedelta
from .forms import ShiftForm, ShiftTypeForm, ScheduleShiftForm, RequestForm
from loginApp.forms import UpdateUserForm, UpdatePasswordForm, Register_Form
from loginApp.models import User, Address
from .models import Shift, ShiftType, ScheduleShift, Request
import bcrypt
from django.template import loader
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from dateutil import relativedelta
from django.db.models import Count, Sum


def validate_user(id, level="user"):
    if not len(User.objects.filter(id=id)) > 0:
        return False
    user = User.objects.get(id=id)
    return user.user_level

def validate_admin(request):
    validate_user(request)
    user_id = request.session['user_id']
    if not validate_level(user_id) is True:
        return redirect('/')

def index(request):
    cal_date = date.today()
    if not 'user_id' in request.session:
        # return redirect('/login')
        context = {
            'cal_date': cal_date.strftime("%Y-%m-%d"),
            # 'schedule' : events,
            'nav_bar': 'guest_nav.html',
        }
        return render(request, 'cal_home.html', context)
    else:
        user = User.objects.get(id=request.session['user_id'])        
        print('date: ', cal_date)
        nav_bar = get_nav(request.session['user_id'])
        context = {
            'cal_date': cal_date.strftime("%Y-%m-%d"),
            # 'schedule' : events,
            'nav_bar': nav_bar,
        }
        return render(request, 'cal_home.html', context)

def get_nav(user_id):
    user = User.objects.get(id=user_id)
    if user.user_level == True:
            nav_bar = 'admin_nav.html'
    else:
        nav_bar = 'user_nav.html'
    return nav_bar

def validate_level(user_id):
    user = User.objects.get(id=user_id)
    return user.user_level

def admin(request):    
    context = {
        'page_title' : 'Admin Dashboard',        
    }

def dashboard(request):
    pass

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
        'nav_bar': get_nav(current_user.id),
        'user_level' : current_user.user_level,
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
    if not user_id == request.session['user_id']:
        if validate_user(request.session['user_id']) == False:
            print(validate_user(request.session['user_id']))
            return redirect('/')
    context = {
        'form' : UpdateUserForm(),
        'password_form' : UpdatePasswordForm(),
        'update': '',        
    }    
    return render_edit_page(request, context, user_id)

def update_user(request):
    if request.method != "POST":
        return redirect("/")
    # if request.POST['user_id'] == '2' or request.POST['user_id'] == '3':
    #     return redirect('/')
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
    if validate_user(request.session['user_id'], "admin") is False:
        return redirect('/')
    user_id = request.session['user_id']
    if remove_id == '1':
        return redirect('/')
    remove = User.objects.get(id=remove_id)
    remove.delete()
    return redirect('/manage_users')

def new_user(request):
    user_id = request.session['user_id']
    if validate_user(user_id, "admin") is False:
        return redirect('/') 
    form = Register_Form()
    context = {
        'nav': get_nav(user_id),
        'user_id': user_id,
        'register_form': form,
        'page_title': 'Add User',
    }
    return render(request, 'add_user.html', context)

def show_user(request, user_id=None):
    user = User.objects.get(id=request.session['user_id'])
    if not user_id==None:
        if len(User.objects.filter(id=user_id)) == 0:
            return redirect('/')
        profile = User.objects.get(id=user_id)
    else:
        profile = user
    shifts = get_type_count(datetime.now(), profile.id)
    # shift_types = ShiftType.objects.all()
    # year = datetime.now().year
    # month = datetime.now().month
    # shifts_month = {}
    # shifts_year = {}
    # for s_type in shift_types:
    #     m_count = ScheduleShift.objects.filter(user=profile, date__year=year, date__month=month, shift_type=s_type).count()
    #     y_count = ScheduleShift.objects.filter(user=profile, date__year=year, shift_type=s_type).count()
    #     shifts_month.update({s_type.name : {m_count: y_count}})
        # shifts_year.update({s_type.name : y_count})
    # print(shifts_month, shifts_year) 
    context = {
        'nav_bar': get_nav(user.id),
        'profile': profile,
        'user': user,
        'user_id': user.id,
        # 'shifts_year': shifts_year,
        'shifts': shifts,
    }
    # print(shifts)
    return render(request, 'profile.html', context)

def get_user_shift_count():
    pass

def manage_users(request):
    if validate_user(request.session['user_id'], "admin") is False:
        return redirect('/')
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
    context = {
        'admin' : user.user_level,
        'users' : User.objects.all(),
        'user_id': user.id,
        'page_title': 'Manage Users',
    }
    return render(request, 'user_dash.html', context)

def manage_shifts(request):    
    user = User.objects.get(id=request.session['user_id'])
    if validate_user(request.session['user_id']) is False:
        return redirect('/')
    context = {
        'shift_form' : ShiftForm(),
        'type_form' : ShiftTypeForm(),
        'shifts': Shift.objects.all(),
        'types': ShiftType.objects.all(),
    }
    return render(request, 'edit_shifts.html', context)

def admin_tools(request):
    if not validate_user(request.session['user_id']) is True:
        return redirect('/')
    context = {
        'form' : ScheduleShiftForm(),
    }
    return render(request, 'admin_tools.html', context)

def sched_list(request):
    pass

def schedule_shifts(request, date=None):
    if validate_user(request.session['user_id'], "admin") is False:
        return redirect('/') 
    date = datetime.now()
    user_shifts = get_shift_count(date)
    context = {
        'form' : ScheduleShiftForm(),
        'action': 'update_schedule',
        # 'schedule' : ScheduleShift.objects.all(),
        'user_shifts': user_shifts,
    }
    return render(request, 'schedule.html', context)

def get_shift_count(date, user=None):
    if not user == None:
        users = User.objects.get(id=user.id)
    else:
        users = User.objects.all()
    year = date.year
    month = date.month
    user_shifts = {}
    user_shifts2 = {}
    for user in users:
        m_count = ScheduleShift.objects.filter(user=user, date__year=year, date__month=month).count()
        y_count = ScheduleShift.objects.filter(user=user, date__year=year).count()
        # user_shifts.update({user.id : {user.last_name: {m_count: y_count}}})
        user_shifts.update({user.id: {"name": user.last_name, "month": m_count, "year": y_count}})
    t_month = ScheduleShift.objects.filter(date__year=year, date__month=month).count()
    t_year = ScheduleShift.objects.filter(date__year=year).count()
    user_shifts.update({99999: {"name": "Total", "month": t_month, "year": t_year}})
    # print(user_shifts)
    return user_shifts

def get_type_count(date, user_id):
    user = User.objects.get(id=user_id)
    shift_types = ShiftType.objects.all()
    year = date.year
    month = date.month
    shifts_type = {}
    for s_type in shift_types:
        m_count = ScheduleShift.objects.filter(user=user, date__year=year, date__month=month, shift_type=s_type).count()
        y_count = ScheduleShift.objects.filter(user=user, date__year=year, shift_type=s_type).count()
        shifts_type.update({s_type.id: {"name": s_type.name, 'month': m_count, "year": y_count}})
    t_month = ScheduleShift.objects.filter(user=user, date__year=year, date__month=month).count()
    t_year = ScheduleShift.objects.filter(user=user, date__year=year).count()
    shifts_type.update({99999: {"name": "Total", "month": t_month, "year": t_year}})
    return shifts_type
    
    

def update_schedule(request):
    if request.method != 'POST':
        return redirect('/')
    if validate_user(request.session['user_id'], "admin") is False:
        return redirect('/')
    if 'multi-date' in request.POST:
        dates = request.POST['multi-date'].split(',')
        for xDate in dates:
            save_shifts(request, xDate)
    else:
        update_sched_shift(request, request.POST['date'])
    return redirect('/schedule')

def update_sched_shift(request, xDate):
    nDate = datetime.strptime(xDate, "%m-%d-%Y")
    date = nDate.strftime("%Y-%m-%d")
    # print(xDate)
    user = User.objects.get(id=request.POST['user'])
    shift = Shift.objects.get(id=request.POST['shift'])    
    shift_type = ShiftType.objects.get(id=request.POST['shift_type'])
    print(request.POST['id'])
    if not request.POST['id'] == '':
        shedule_shift = ScheduleShift.objects.get(id=request.POST['id'])
        shedule_shift.user = user
        shedule_shift.shift = shift
        shedule_shift.shift_type = shift_type
        shedule_shift.save()
    else:
        schedule_shift = ScheduleShift.objects.create(date=date, shift=shift, shift_type=shift_type, user=user)    
    return

def save_shifts(request, xDate):
    # print(request)
    nDate = datetime.strptime(xDate, "%m-%d-%Y")
    date = nDate.strftime("%Y-%m-%d")
    # print(xDate)
    user = User.objects.get(id=request.POST['user'])
    shift = Shift.objects.get(id=request.POST['shift'])
    shift_type = ShiftType.objects.get(id=request.POST['shift_type'])
    shedule_shift = ScheduleShift.objects.create(date=date, shift=shift, shift_type=shift_type, user=user)
    return

def delete_sched_shift(request):
    # print("trying to delete")
    if request.method != 'POST':
        return redirect('/')
    if validate_user(request.session['user_id'], "admin") is False:
        # print("validation failed")
        return redirect('/')
    ScheduleShift.objects.get(id=request.POST['id']).delete()
    return redirect('/schedule')

def delete_multiple(request):
    if request.method != 'POST':
        return redirect('/')
    if validate_user(request.session['user_id'], "admin") is False:
        return redirect('/')
    # print(request.POST['user'])
    user = User.objects.get(id=request.POST['user'])
    if 'multi-date' in request.POST:
        dates = request.POST['multi-date'].split(',')        
        for xDate in dates:
            # print(xDate)
            nDate = datetime.strptime(xDate, "%m-%d-%Y")
            date = nDate.strftime("%Y-%m-%d")
            ScheduleShift.objects.filter(user=user, date=date).delete()
    return redirect('/admin_tools')

def update_shifts(request, shift_id=None):
    if request.method != 'POST':
        return redirect('/')
    if validate_user(request.session['user_id'], "admin") is False:
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
    if not shift_id == None:
        shift = Shift.objects.get(id=shift_id)
        shift.shift=start_time + "-" + end_time
        shift.start_time=request.POST['start_time']
        shift.end_time=request.POST['end_time']
        shift.save()
    else:
        shift = Shift.objects.create(shift=start_time + "-" + end_time, start_time=request.POST['start_time'], end_time=request.POST['end_time'])
    return redirect('/manage_shifts') 

def remove_shift(request, shift_id):
    if validate_user(request.session['user_id'], "admin") is False:
        return redirect('/') 
    Shift.objects.get(id=shift_id).delete()
    return redirect('/manage_shifts')

def clear_month(request):
    date = datetime.strptime(request.POST['month_clear2'], "%m-%d-%Y")
    year = date.strftime('%Y')
    month = date.strftime('%m')
    ScheduleShift.objects.filter(date__year=year, date__month=month).delete()
    return redirect('/admin_tools')

def clear_user(request):
    print("Made it here!")
    date = datetime.strptime(request.POST['month_clear'], "%m-%d-%Y")
    year = date.strftime('%Y')
    month = date.strftime('%m')
    user= User.objects.get(id=request.POST['user'])
    ScheduleShift.objects.filter(date__year=year, date__month=month, user=user).delete()
    return redirect('/admin_tools')

def get_ampm(time):
    time_s = int(time) - 12
    if 22 > int(time) > 11:        
        time_ampm = '0' + str(time_s) + 'pm'
    elif int(time) > 21:
        time_ampm = str(time_s) + 'pm'
    else:
        time_ampm = time + 'am'
    return time_ampm

def update_types(request, type_id=None):
    if validate_user(request.session['user_id'], "admin") is False:
        return redirect('/')
    if request.method != 'POST':
        return redirect('/')
    form = ShiftTypeForm(request.POST)
    print(request.POST)
    if not form.is_valid():
        print("Not Valid! ", form)
        context = {
            'type_form' : form,
            'shift_form' : ShiftForm(),
            'shifts': Shift.objects.all(),
            'types': ShiftType.objects.all(),
        }
        return render(request, 'edit_shifts.html', context)
    if not type_id == None:
        shift_type = ShiftType.objects.get(id=type_id)
        shift_type.name = request.POST['name']
        shift_type.color = request.POST['color']
        shift_type.save()
    else:
        shift_type = ShiftType.objects.create(name=request.POST['name'], color=request.POST['color'])
    return redirect('/manage_shifts') 

def remove_shift_type(request, type_id):
    if validate_user(request.session['user_id'], "admin") is False:
        return redirect('/')
    ShiftType.objects.get(id=type_id).delete()
    return redirect('/manage_shifts')


def get_shifts(request, date, user_id=""):
    date = datetime.strptime(date, "%Y-%m-%d")
    start_shifts = date - timedelta(days=12)
    end_shifts = date + timedelta(days=45)
    print(f"start: {start_shifts}, end: {end_shifts}")
    year = date.strftime('%Y')
    month = date.strftime('%m')
    if user_id != "":
        # print("got user_id: ", user_id)     
        user = User.objects.get(id=user_id)
        # print(user.last_name)
        shifts = ScheduleShift.objects.filter(user=user, date__year=year, date__month=month) 
    else:
        # shifts = ScheduleShift.objects.filter(date__year=year, date__month=month)     
        shifts = ScheduleShift.objects.filter(date__gte=start_shifts, date__lte=end_shifts)
    events = []
    i = 0
    for shift in shifts:
        start_date = datetime.strftime(shift.date, "%Y-%m-%d")  
        start_time = str(shift.shift.start_time)
        events.append({
            "title" : shift.user.last_name,
            "start" : start_date, 
            "time" : start_time,
            "shift_h": shift.shift.shift,
            "shift_type": shift.shift_type.name,
            "id": shift.id,
            "color": shift.shift_type.color,
        })
        i += 1     
    # print(events)
    response = {
        'cal_date': date.strftime("%Y-%m-%d"),
        'schedule' : events,
    }
    return JsonResponse(response)

def update_shift_count(request, date_in):
    # print(date_in)
    date = datetime.strptime(date_in, "%Y-%m-%d")
    shift_count = get_shift_count(date)
    # print(shift_count)
    response = {
        'shift_count': shift_count,
    }
    return JsonResponse(response)

def update_type_count(request, date_in, user_id):
    date = datetime.strptime(date_in, "%Y-%m-%d")
    type_count = get_type_count(date, user_id)
    # print(type_count)
    response = {
        'shift_count': type_count,
    }
    return JsonResponse(response)
