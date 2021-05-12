from .models import Shift, ShiftType, ScheduleShift, Request
from loginApp.models import User
from django import forms
from datetime import datetime
from django.forms.widgets import TextInput

class Date_In(TextInput):
    input_type = 'date'

class Time_In(TextInput):
    input_type = 'time'

doctor_objs = User.objects.filter(user_type='doctor').values_list('id', 'last_name')
doc_list = [('', ' ')]
for doctor in doctor_objs:
    doc_list.append((f'{doctor[0]}', f'Dr. {doctor[1]}',))
# print(DOC_LIST)

shift_objs = Shift.objects.all().values_list('id', 'shift')
shift_list = [('', ' ')]
for shift in shift_objs:
    shift_list.append((f'{shift[0]}', f'{shift[1]}',))
# print(shift_list)

shiftType_objs = ShiftType.objects.all().values_list('id', 'name')
shift_type_list = [('', ' ')]
for shiftType in shiftType_objs:
    shift_type_list.append((f'{shiftType[0]}', f'{shiftType[1]}',))
# print(shift_type_list)

class ScheduleShiftForm(forms.Form):
    user = forms.ChoiceField(widget=forms.Select, choices=doc_list, required=True)
    date = forms.DateTimeField(widget=Date_In, required=True)
    shift = forms.ChoiceField(widget=forms.Select, choices=shift_list, required=True)
    shift_type = forms.ChoiceField(widget=forms.Select, choices=shift_type_list, required=True, initial=0)

    def __init__(self, *args, **kwargs):
        super(ScheduleShiftForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
        
class ShiftTypeForm(forms.Form):
    name = forms.CharField(max_length=20, widget=forms.TextInput)
    color = forms.CharField(max_length=7, widget=forms.TextInput)    

    def __init__(self, *args, **kwargs):
        super(ShiftTypeForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class' : 'form-control',
            })

    def clean(self):
        super(ShiftTypeForm, self).clean()
        name = self.cleaned_data.get('name')
        color = self.cleaned_data.get('color')
        
        return self.cleaned_data

class ShiftForm(forms.Form):
    start_time = forms.TimeField(widget=Time_In)
    end_time = forms.TimeField(widget=Time_In)

    def __init__(self, *args, **kwargs):
        super(ShiftForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class' : 'form-control',
            })

    def clean(self):
        super(ShiftForm, self).clean()
        start_time = self.cleaned_data.get('start_time')
        end_time = self.cleaned_data.get('end_time')

        def check_time_after(start, end, varName, message):            
            # time_checking = start.replace(tzinfo=None)
            # time_compared_to = end.replace(tzinfo=None)
            # if time_checking >= time_compared_to: 
            if start >= end:
                self.errors[f"{varName}"] = self.error_class([f'{message}'])
                print('time failed')

        # check_time_after(start_time, end_time, 'end_time','End time is invalid.')

        return self.cleaned_data

class RequestForm(forms.Form):
    request_user = forms.ChoiceField(widget=forms.Select, choices=doc_list, required=True)
    switch_user = forms.ChoiceField(widget=forms.Select, choices=doc_list, required=True)
    request_type = forms.CharField(max_length=20, widget=forms.Select)
    start_date = forms.DateTimeField(widget=Date_In, required=True)
    end_date = forms.DateTimeField(widget=Date_In, required=True)

    def __init__(self, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class' : 'form-control',
            })

    def clean(self):
        super(RequestForm, self).clean()
        request_user = self.cleaned_data.get('request_user')
        switch_user = self.cleaned_data.get('switch_user')
        request_type = self.cleaned_data.get('request_type')
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')

        def check_string(string, length, varName, message):
            if len(string) < length: 
                self.errors[f"{varName}"] = self.error_class([
                    f'{message}'])
                print('string failed')

        def check_date_after(date, compare, varName, message):            
            date_checking = date.replace(tzinfo=None)
            date_compared_to = compare.replace(tzinfo=None)
            if date_checking <= date_compared_to: 
                self.errors[f"{varName}"] = self.error_class([f'{message}'])
                print('label failed')

        check_date_after(start_date, datetime.now(), 'start_date','Time travel is not allowed, our delorian is under repair.')
        check_date_after(end_date, start_date, 'end_date','End date is invalid.')
        
        return self.cleaned_data

