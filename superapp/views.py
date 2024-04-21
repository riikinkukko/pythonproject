from .forms import *
from .models import *
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import login, authenticate, logout
from datetime import datetime, date
from django.db.models import Q
from random import randint
from django.contrib import messages

def doctor_form(request):
    """
    Регистрация
    """
    html = ''
    if request.method == 'POST':
        register_form = RegisterFormDoctors(request.POST)
        if register_form.is_valid():
            new_user = register_form.save(commit=False)
            codes = [randint(1000, 10000), randint(1000, 10000), randint(1000, 10000)]
            for i in range(1, len(codes)):
                if codes[i] == codes[i-1]:
                    codes[i] = randint(1000, 5000)
            new_user.save()
            new_user = Doctor.objects.get(id=new_user.id)
            new_user.codes = codes[0], codes[1], codes[2]
            new_user.save()
            return redirect('login')
        else:
            html = register_form.errors
    else:
        register_form = RegisterFormDoctors()
    return render(request, 'superapp/doctor_form.html', {'form': register_form, 'html': html})


#Авторизация пользователя
def doctor_login(request):
    html = ''
    if request.method == 'POST':
        form = DoctorLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user) #C помощью этого метода от джанго происходит авторизация
            return redirect('profile')
        else:
            html = form.errors
    else:
        form = DoctorLoginForm()
    return render(request, 'superapp/doctor_auth_form.html', {'form': form, 'html': html})


# логаут
def logout_user(request):
    logout(request)
    return redirect('login')

#Домашняя страница - отсутсвует, редирект на профиль
def home(request):
    return redirect('profile')

#Профили пользователей

def profile_view(request):
    """
    :param request:
    :return: Профили для пациента/доктора
    """

    global patient_id
    user = Doctor.objects.get(id=request.user.id)
    if request.user.is_authenticated:
        if request.user.is_doctor:
            if request.user.name == '':
                return redirect('about')
            else:
                patients = Doctor.objects.filter(doctor_id=request.user.id)
                if request.method == 'POST':
                    if 'table_submit' in request.POST:
                        l_time = []
                        l_drugs = []
                        patient_id = request.POST.get('patient_id')
                        patient = Doctor.objects.get(id=patient_id)
                        for i in range(1, 30):
                            if 'time' + str(i) in request.POST:
                                if patient.time_drugs_patient != None:
                                    if i == 1:
                                        patient.time_drugs_patient = request.POST.get('time' + str(i)) + ','
                                        patient.save()
                                    else:
                                        patient.time_drugs_patient += request.POST.get('time' + str(i)) + ','
                                        patient.save()
                                    if patient.drugs != None:
                                        if i == 1:
                                            patient.drugs = request.POST.get('drug'+str(i))+','
                                        else:
                                            patient.drugs += request.POST.get('drug'+str(i))+','
                                            patient.save()
                                    else:
                                        drugs, created = Doctor.objects.update_or_create(id=patient_id, defaults={
                                            "drugs": request.POST.get('drug' + str(i)) + ','})
                                else:
                                    time, created = Doctor.objects.update_or_create(id=patient_id, defaults={
                                        "time_drugs_patient": request.POST.get('time' + str(i)) + ','})
                                    drugs, created = Doctor.objects.update_or_create(id=patient_id, defaults={
                                        "drugs": request.POST.get('drug' + str(i)) + ','})
                    else:
                        patient_id = request.POST['patient_id']
                        patient = get_object_or_404(Doctor, id=patient_id)
                        data_comments = request.POST['comments']
                        data_illnesses = request.POST['illnesses']
                        data_created_at = request.POST['created_at']
                        data_visit_date = request.POST['visit_date']
                        side_effects = patient.side_effects
                        comments_paitent = patient.comments_patient
                        if 'called' in request.POST:  # Проверяем нажата ли кнопка для вызова пациента
                            patient.is_called = True
                            patient.date_of_visit = data_visit_date
                            patient.save()
                        if data_comments == '':
                            # add messages
                            pass
                        else:
                            comments_list = patient.comments
                            comments_list = [word for word in comments_list.split(',')]
                            last_comment = comments_list[-1]
                            if last_comment == 'Отсутствуют':
                                patient.comments = data_comments
                                patient.times_of_creating_comments = data_created_at
                                patient.save()
                            else:
                                patient.comments += ','
                                patient.comments += data_comments
                                patient.times_of_creating_comments += ','
                                patient.times_of_creating_comments += data_created_at
                                patient.save()

                        if data_illnesses == '':
                            # add messages
                            pass
                        else:
                            patient.illnesses = data_illnesses
                            patient.save()


                return render(request, 'superapp/doctor_profile.html', {'patients': patients})
        elif request.user.klapan == '':
            return redirect('about')
        else:
            if request.user.is_doctor == False: #Если пользователь пациент

                drugs = request.user.drugs
                time_drugs = request.user.time_drugs_patient

                if drugs is not None:
                    drugs = [word for word in drugs.split(',')]
                else:
                    drugs = []

                if time_drugs is not None:
                    time_drugs = [word for word in time_drugs.split(',')]
                else:
                    time_drugs = []

                time_and_drugs = []

                for i in range(min(len(drugs), len(time_drugs))):
                    if drugs[i] == '' or time_drugs[i] == '':
                        pass
                    else:
                        time_and_drugs.append(time_drugs[i])
                        time_and_drugs.append(drugs[i])

                print(time_and_drugs)
                length = ''

                for i in range(1, len(time_and_drugs)+1):
                    length += str(i)

                print(length)
                even = []
                odd = []

                for i in length:
                    if int(i) % 2 == 0:
                        even.append(int(i))
                    else:
                        odd.append(int(i))

                comments_list = request.user.comments
                created_at_list = request.user.times_of_creating_comments

                if comments_list == '' or created_at_list == '':
                    comments, created = Doctor.objects.update_or_create(id=request.user.id, defaults={
                        'times_of_creating_comments': "Нет", 'comments': "Отсутствуют"})
                    last_comment = 'Отсутствуют'
                    last_created_at = "Нет"

                    comments_and_time_list = []
                else:
                    comments_list = [word for word in comments_list.split(',')]
                    last_comment = comments_list[-1]
                    created_at_list = [word for word in created_at_list.split(',')]
                    last_created_at = created_at_list[-1]

                    comments_and_time_list = []

                    for i in range(min(len(comments_list), len(created_at_list))):
                        if comments_list[i] == '' or created_at_list[i] == '':
                            pass
                        else:
                            comments_and_time_list.append(comments_list[i])
                            comments_and_time_list.append(created_at_list[i])

                    comments_and_time_list = comments_and_time_list[::-1]
                    length = []

                    for i in range(1, len(comments_list)*2+1):
                        length.append(i)

                    print(length)

                    even = []
                    odd = []

                    for i in length:
                        if i % 2 == 0:
                            even.append(int(i))
                        else:
                            odd.append(int(i))

                print(comments_and_time_list, odd, even)
                if request.method == 'POST':
                    if 'button' in request.POST:
                        patient_id = request.user.id
                        patient = Doctor.objects.get(id=patient_id)
                        obj, created = Doctor.objects.update_or_create(id=patient_id, defaults={'is_called': False})

                    if 'send' in request.POST:
                        data_effects = request.POST['side_effects']
                        if user.side_effects == None or user.side_effects == '':
                            obj, created = Doctor.objects.update_or_create(id=request.user.id, defaults={'side_effects': data_effects})
                        elif data_effects == '':
                            pass
                        else:
                            user.side_effects = data_effects
                            user.save()
                    if 'send_comment' in request.POST:
                        data_comment = request.POST['comments_patient']
                        if user.comments_patient == None:
                            obj, created = Doctor.objects.update_or_create(id=request.user.id, defaults={'comments_patient': data_comment})
                        elif data_comment == '':
                            pass
                        else:
                            user.comments_patient = data_comment
                            user.save()
                    return redirect('profile')


                return render(request, 'superapp/patient_profile.html',
                              {'comments_list': comments_list, 'last_comment': last_comment, 'created_at_list': created_at_list, 'last_created_at': last_created_at,
                               'full_list': comments_and_time_list, 'drugs': drugs, 'time_drugs': time_drugs, 'length': length, 'even': even, 'odd': odd, 'time_and_drugs': time_and_drugs})

            else: #Если пользователь доктор
                patients = Doctor.objects.filter(doctor_id=request.user.id)
                if request.method == 'POST':
                    patient_id = request.POST['patient_id']
                    patient = get_object_or_404(Doctor, id=patient_id)
                    data_comments = request.POST['comments']
                    data_drugs = request.POST['drugs']
                    data_illnesses = request.POST['illnesses']
                    data_created_at = request.POST['created_at']
                    data_visit_date = request.POST['visit_date']
                    data_schedule = request.POST['medication_schedule']
                    side_effects = patient.side_effects
                    comments_paitent = patient.comments_patient
                    if 'called' in request.POST:  # Проверяем нажата ли кнопка для вызова пациента
                        patient.is_called = True
                        patient.date_of_visit = data_visit_date
                        patient.save()
                    if data_comments == '':
                        # add messages
                        pass
                    else:
                        comments_list = patient.comments
                        comments_list = [word for word in comments_list.split(',')]
                        last_comment = comments_list[-1]
                        if last_comment == 'Отсутствуют':
                            patient.comments = data_comments
                            patient.times_of_creating_comments = data_created_at
                            patient.save()
                        else:
                            patient.comments += ','
                            patient.comments += data_comments
                            patient.times_of_creating_comments += ','
                            patient.times_of_creating_comments += data_created_at
                            patient.save()

                    if data_drugs == '':
                        # add messages
                        pass
                    else:
                        patient.drugs = data_drugs
                        patient.save()

                    if data_illnesses == '':
                        # add messages
                        pass
                    else:
                        patient.illnesses = data_illnesses
                        patient.save()

                    if data_schedule == '':
                        # add messages
                        pass
                    else:
                        patient.medication_schedule = data_schedule
                        patient.save()

                return render(request, 'superapp/doctor_profile.html', {'patients': patients})

                    #return redirect('profile')
    else:
        return redirect('login')

#почти работает, советую - форма внесения данных о себе (доделать чекание отсутствия/наличия записи в поле)
#upd все работает шикарно
def about_user_form(request):

    """
    :param request:
    :return: about_user_form см. forms
    """

    if request.user.klapan == '' or request.user.klapan == None:
        if request.method == 'POST':
            if request.user.is_doctor:
                form = AboutUserDoctor(request.POST)
                if form.is_valid():
                    data = form.cleaned_data
                    id_data, created = Doctor.objects.update_or_create(id=request.user.id, defaults=data)
                    return redirect('profile')
            else:
                form = AboutUserPatient(request.POST)
                if form.is_valid():
                    data = form.cleaned_data
                    id_data, created = Doctor.objects.update_or_create(id=request.user.id, defaults=data)
                    return redirect('profile')
        else:
            if request.user.is_doctor:
                form = AboutUserDoctor()
            else:
                form = AboutUserPatient()
        return render(request, 'superapp/about_user_form.html', {'form': form})
    else:
        return redirect('profile')

#пациент добавляет доктора, а значит доктор может чекать привязанного пациента - все просто
def add_doctor(request):
    doctor_id = request.user.doctor_id
    if doctor_id == None:
        doctor = 'Отсутсвует'
        doctors = Doctor.objects.filter(is_doctor=True)
        patient_id = request.user.id
        patient = get_object_or_404(Doctor, id=patient_id)
    else:
        doctor = get_object_or_404(Doctor, id=doctor_id)
        doctors = Doctor.objects.filter(is_doctor=True)
        patient_id = request.user.id
        patient = get_object_or_404(Doctor, id=patient_id)

    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')
        doctor = get_object_or_404(Doctor, id=doctor_id)
        doctor_ident = doctor.id
        patient.doctor_id = doctor_ident
        patient.save()
        return redirect('profile')

    return render(request, 'superapp/add_doctor.html', {'patient': patient, 'doctors': doctors, 'doctor': doctor})

# измерения пациента пульс
def patient_metrics_pulse(request):
    pulse_list = request.user.heart_pulse
    pulse_metrics_date_list = request.user.pulse_metrics_date
    pulse_metrics_time_list = request.user.pulse_metrics_time
    if pulse_list == '' or pulse_metrics_date_list == '' or pulse_metrics_time_list == None:
        obj, created = Doctor.objects.update_or_create(id=request.user.id, defaults={"heart_pulse": "0,"})
        obj, created = Doctor.objects.update_or_create(id=request.user.id, defaults={"pulse_metrics_date": "0,"})
        obj, created = Doctor.objects.update_or_create(id=request.user.id, defaults={"pulse_metrics_time": "0,"})
        pulse_list, pulse_metrics_date_list, pulse_metrics_time_list = [], [], []
        average_value = 'Отсутствует'
        return redirect('pulse_metrics')
    else:
        pulse_list = pulse_list[:-1]
        pulse_metrics_date_list = pulse_metrics_date_list[:-1]
        pulse_metrics_time_list = pulse_metrics_time_list[:-1]
        pulse_list = [int(num) for num in pulse_list.split(',')]
        pulse_metrics_date_list = [num for num in pulse_metrics_date_list.split(',')]
        pulse_metrics_time_list = [num for num in pulse_metrics_time_list.split(',')]
        pulse_metrics_list = []
        a = min(len(pulse_metrics_date_list), len(pulse_metrics_time_list))
        for i in range(a):
            pulse_metrics_list.append(pulse_metrics_date_list[i]+' '+pulse_metrics_time_list[i])
        average_value = sum(pulse_list)/len(pulse_list)
    if request.method == 'POST':
        patient_id = request.user.id
        patient = get_object_or_404(Doctor, id=patient_id)
        data_heart_pulse = request.POST['heart_pulse']
        data_pulse_metrics_date = request.POST['heart_metrics_date']
        data_pulse_metrics_time = request.POST['heart_metrics_time']
        if data_pulse_metrics_time == '' or data_heart_pulse == '' or data_pulse_metrics_date == '':
            # add message pls
            pass
        else:
            data_heart_pulse += ','
            data_pulse_metrics_date += ','
            data_pulse_metrics_time += ','
            patient.heart_pulse += data_heart_pulse
            patient.pulse_metrics_date += data_pulse_metrics_date
            patient.pulse_metrics_time += data_pulse_metrics_time
            patient.save()
        return redirect('pulse_metrics')
    return render(request, 'superapp/tests.html', {'pulse_list': pulse_list, 'average_value': average_value, 'pulse_metrics_list': pulse_metrics_list})

# измерения пациента вес
def patient_metrics_weight(request):
    weight_list = request.user.weight
    weight_metrics_date_list = request.user.weight_metrics_date
    weight_metrics_time_list = request.user.weight_metrics_time
    if weight_list == '' or weight_metrics_date_list == '' or weight_metrics_time_list == None:
        weight_list, weight_metrics_date_list = [], []
        obj, created = Doctor.objects.update_or_create(id=request.user.id, defaults={"weight": "0,"})
        obj, created = Doctor.objects.update_or_create(id=request.user.id, defaults={"weight_metrics_date": "0,"})
        obj, created = Doctor.objects.update_or_create(id=request.user.id, defaults={"weight_metrics_time": "0,"})
        return redirect('weight_metrics')
    else:
        weight_list = weight_list[:-1]
        weight_metrics_date_list = weight_metrics_date_list[:-1]
        weight_metrics_time_list = weight_metrics_time_list[:-1]
        weight_list = [int(num) for num in weight_list.split(',')]
        weight_metrics_date_list = [num for num in weight_metrics_date_list.split(',')]
        weight_metrics_time_list = [num for num in weight_metrics_time_list.split(',')]
        weight_metrics_list = []
        a = min(len(weight_metrics_date_list), len(weight_metrics_time_list))
        for i in range(a):
            weight_metrics_list.append(weight_metrics_date_list[i]+' '+weight_metrics_time_list[i])
    if request.method == 'POST':
        patient_id = request.user.id
        patient = get_object_or_404(Doctor, id=patient_id)
        data_weight = request.POST['weight']
        data_weight_metrics_date = request.POST['weight_metrics_date']
        data_weight_metrics_time = request.POST['weight_metrics_time']
        if data_weight == '' or data_weight_metrics_date == '' or data_weight_metrics_time == '':
            data_weight, data_weight_metrics_date, data_weight_metrics_time = [], [], []
        else:
            data_weight += ','
            data_weight_metrics_date += ','
            data_weight_metrics_time += ','
            patient.weight += data_weight
            patient.weight_metrics_date += data_weight_metrics_date
            patient.weight_metrics_time += data_weight_metrics_time
            patient.save()
        return redirect('weight_metrics')
    return render(request, 'superapp/weight_metrics.html', {'weight_list': weight_list, 'weight_metrics_list': weight_metrics_list})

# измерения пациента артериалное и диастолическое давление
def patient_metrics_pressures(request):
    arteric_pressure_list = request.user.arteric_pressure
    diastolic_pressure_list = request.user.diastolic_pressure
    pressure_metrics_date_list = request.user.pressure_metrics_date
    pressure_metrics_time_list = request.user.pressure_metrics_time
    average_pressure_list = []
    if arteric_pressure_list == None or diastolic_pressure_list == None or pressure_metrics_date_list == None or pressure_metrics_time_list == None:
        obj, created = Doctor.objects.update_or_create(id=request.user.id, defaults={"pressure_metrics_date": "0,"})
        obj, created = Doctor.objects.update_or_create(id=request.user.id, defaults={"arteric_pressure": "0,"})
        obj, created = Doctor.objects.update_or_create(id=request.user.id, defaults={"diastolic_pressure": "0,"})
        obj, created = Doctor.objects.update_or_create(id=request.user.id, defaults={"pressure_metrics_time": "0,"})
        average_pressure_list = [0]
        return redirect('pressure_metrics')
    else:
        arteric_pressure_list = arteric_pressure_list[:-1]
        diastolic_pressure_list = diastolic_pressure_list[:-1]
        pressure_metrics_date_list = pressure_metrics_date_list[:-1]
        pressure_metrics_time_list = pressure_metrics_time_list[:-1]
        arteric_pressure_list = [int(num) for num in arteric_pressure_list.split(',')]
        diastolic_pressure_list = [int(num) for num in diastolic_pressure_list.split(',')]
        pressure_metrics_date_list = [num for num in pressure_metrics_date_list.split(',')]
        pressure_metrics_time_list = [num for num in pressure_metrics_time_list.split(',')]
        a = min(len(pressure_metrics_date_list), len(pressure_metrics_time_list))
        pressure_metrics_list = []
        average_pressure_list = []
        for i in range(a):
            pressure_metrics_list.append(pressure_metrics_date_list[i]+' '+pressure_metrics_time_list[i])
        average_value_arteric, average_value_diastolic = sum(arteric_pressure_list)/len(arteric_pressure_list), sum(diastolic_pressure_list)/len(diastolic_pressure_list)
        for k in range(len(diastolic_pressure_list)):
            average_pressure_list.append((arteric_pressure_list[k]-diastolic_pressure_list[k])/3+diastolic_pressure_list[k])
    if request.method == 'POST':
        patient_id = request.user.id
        patient = get_object_or_404(Doctor, id=patient_id)
        data_arteric = request.POST['arteric_pressure']
        data_diastolic = request.POST['diastolic_pressure']
        data_metrics_date = request.POST['pressure_metrics_date']
        data_metrics_time = request.POST['pressure_metrics_time']
        if data_arteric == '' or data_diastolic == '' or data_metrics_date == '' or data_metrics_time == '':
            data_arteric, data_diastolic, data_metrics_date, data_metrics_time = [], [], [], []
        else:
            data_arteric += ','
            data_diastolic += ','
            data_metrics_date += ','
            data_metrics_time += ','
            patient.arteric_pressure += data_arteric
            patient.diastolic_pressure += data_diastolic
            patient.pressure_metrics_date += data_metrics_date
            patient.pressure_metrics_time += data_metrics_time
            patient.save()
        return redirect('pressure_metrics')
    return render(request, 'superapp/pressures_metrics.html', {'arteric_pressure_list': arteric_pressure_list, 'diastolic_pressure_list': diastolic_pressure_list,
                                                               'average_value_diastolic': average_value_diastolic, 'average_value_arteric': average_value_arteric, 'pressure_metrics_list': pressure_metrics_list, 'average_pressure_list': average_pressure_list})
# измерение температуры
def patient_metrics_temperature(request):
    temperature_list = request.user.temperature
    temperature_metrics_date_list = request.user.temperature_metrics_date
    temperature_metrics_time_list = request.user.temperature_metrics_time
    temperature_metrics_list = []
    if temperature_list == None or temperature_metrics_date_list == None or temperature_metrics_time_list == None:
        weight_list, weight_metrics_date_list = [], []
        obj, created = Doctor.objects.update_or_create(id=request.user.id, defaults={"temperature": "0,"})
        obj, created = Doctor.objects.update_or_create(id=request.user.id, defaults={"temperature_metrics_date": "0,"})
        obj, created = Doctor.objects.update_or_create(id=request.user.id, defaults={"temperature_metrics_time": "0,"})
        return redirect('temperature_metrics')
    else:
        temperature_list = temperature_list[:-1]
        temperature_metrics_date_list = temperature_metrics_date_list[:-1]
        temperature_metrics_time_list = temperature_metrics_time_list[:-1]
        temperature_list = [float(num) for num in temperature_list.split(',')]
        temperature_metrics_date_list = [num for num in temperature_metrics_date_list.split(',')]
        temperature_metrics_time_list = [num for num in temperature_metrics_time_list.split(',')]
        temperature_metrics_list = []
        a = min(len(temperature_metrics_time_list), len(temperature_metrics_date_list))
        for i in range(a):
            temperature_metrics_list.append(temperature_metrics_date_list[i]+' '+temperature_metrics_time_list[i])
    if request.method == 'POST':
        patient_id = request.user.id
        patient = get_object_or_404(Doctor, id=patient_id)
        data_temperature = request.POST['temperature']
        data_temperature_metrics_date = request.POST['temperature_metrics_date']
        data_temperature_metrics_time = request.POST['temperature_metrics_time']
        if data_temperature == '' or data_temperature_metrics_date == '' or data_temperature_metrics_time == '':
            #Добавить messages
            data_weight, data_weight_metrics_date, data_temperature_metrics_time = [], [], []
        else:
            data_temperature += ','
            data_temperature_metrics_date += ','
            data_temperature_metrics_time += ','
            patient.temperature += data_temperature
            patient.temperature_metrics_date += data_temperature_metrics_date
            patient.temperature_metrics_time += data_temperature_metrics_time
            patient.save()
        return redirect('temperature_metrics')
    return render(request, 'superapp/temperature_metrics.html',
                  {'temperature_list': temperature_list, 'temperature_metrics_list': temperature_metrics_list})

# измерение сатурации
def patient_metrics_oxygen_blood(request):
    oxygen_blood_list = request.user.oxygen_blood
    oxygen_blood_date_list = request.user.oxygen_blood_date
    oxygen_blood_time_list = request.user.oxygen_blood_time
    if oxygen_blood_list == None or oxygen_blood_date_list == None or oxygen_blood_time_list == None:
        oxygen_blood_list, oxygen_blood_date_list, oxygen_blood_time_list = [], [], []
        obj, created = Doctor.objects.update_or_create(id=request.user.id, defaults={"oxygen_blood": "0,"})
        obj, created = Doctor.objects.update_or_create(id=request.user.id, defaults={"oxygen_blood_date": "0,"})
        obj, created = Doctor.objects.update_or_create(id=request.user.id, defaults={"oxygen_blood_time": "0,"})
        return redirect('oxygen_blood_metrics')
    else:
        oxygen_blood_list = oxygen_blood_list[:-1]
        oxygen_blood_date_list = oxygen_blood_date_list[:-1]
        oxygen_blood_time_list = oxygen_blood_time_list[:-1]
        oxygen_blood_list = [float(num) for num in oxygen_blood_list.split(',')]
        oxygen_blood_date_list = [num for num in oxygen_blood_date_list.split(',')]
        oxygen_blood_time_list = [num for num in oxygen_blood_time_list.split(',')]
        oxygen_blood_avg_list = []
        a = min(len(oxygen_blood_time_list), len(oxygen_blood_date_list))
        for i in range(a):
            oxygen_blood_avg_list.append(oxygen_blood_date_list[i]+' '+oxygen_blood_time_list[i])
    if request.method == 'POST':
        patient_id = request.user.id
        patient = get_object_or_404(Doctor, id=patient_id)
        data_oxygen_blood = request.POST['oxygen_blood']
        data_oxygen_blood_date = request.POST['oxygen_blood_date']
        data_oxygen_blood_time = request.POST['oxygen_blood_time']
        if data_oxygen_blood == '' or data_oxygen_blood_date == '' or data_oxygen_blood_time == '':
            #Добавить messages
            data_oxygen_blood, data_oxygen_blood_date, data_oxygen_blood_time = [], [], []
        else:
            data_oxygen_blood += ','
            data_oxygen_blood_date += ','
            data_oxygen_blood_time += ','
            patient.oxygen_blood += data_oxygen_blood
            patient.oxygen_blood_date += data_oxygen_blood_date
            patient.oxygen_blood_time += data_oxygen_blood_time
            patient.save()
        return redirect('oxygen_blood_metrics')
    return render(request, 'superapp/oxygen_blood_metrics.html',
                  {'oxygen_blood_list': oxygen_blood_list, 'oxygen_blood_avg_list': oxygen_blood_avg_list})


# доктор смотрит измерения пациента
def doctor_metrics(request):
    patients = Doctor.objects.filter(doctor_id=request.user.id)
    if request.method == 'POST':
        patient_id = request.POST['patient_id']
        patient = get_object_or_404(Doctor, id=patient_id)
        pulse_list = patient.heart_pulse
        pulse_metrics_date_list = patient.pulse_metrics_date
        pulse_metrics_time_list = patient.pulse_metrics_time
        arteric_pressure_list = patient.arteric_pressure
        diastolic_pressure_list = patient.diastolic_pressure
        pressure_metrics_date_list = patient.pressure_metrics_date
        pressure_metrics_time_list = patient.pressure_metrics_time
        weight_list = patient.weight
        weight_metrics_date_list = patient.weight_metrics_date
        weight_metrics_time_list = patient.weight_metrics_time
        temperature_list = patient.temperature
        temperature_metrics_date_list = patient.temperature_metrics_date
        temperature_metrics_time_list = patient.temperature_metrics_time
        oxygen_blood_list = patient.oxygen_blood
        oxygen_blood_date_list = patient.oxygen_blood_date
        oxygen_blood_time_list = patient.oxygen_blood_time
        pulse_metrics_list = []
        pressure_metrics_list = []
        weight_metrics_list = []
        temperature_metrics_list = []
        oxygen_blood_avg_list = []
        average_pressure_list = []
        if pulse_list == None or pulse_metrics_date_list == None:
            pulse_list, pulse_metrics_list = [], []
        else:
            pulse_list = pulse_list[:-1]
            pulse_metrics_date_list = pulse_metrics_date_list[:-1]
            pulse_metrics_time_list = pulse_metrics_time_list[:-1]
            pulse_list = [int(num) for num in pulse_list.split(',')]
            pulse_metrics_date_list = [num for num in pulse_metrics_date_list.split(',')]
            pulse_metrics_time_list = [num for num in pulse_metrics_time_list.split(',')]
            pulse_metrics_list = []
            a = min(len(pulse_metrics_date_list), len(pulse_metrics_time_list))
            for i in range(a):
                pulse_metrics_list.append(pulse_metrics_date_list[i] + ' ' + pulse_metrics_time_list[i])
        if arteric_pressure_list == None or diastolic_pressure_list == None or pressure_metrics_date_list == None:
            arteric_pressure_list, diastolic_pressure_list, pressure_metrics_date_list = [], [], []
        else:
            arteric_pressure_list = arteric_pressure_list[:-1]
            diastolic_pressure_list = diastolic_pressure_list[:-1]
            pressure_metrics_date_list = pressure_metrics_date_list[:-1]
            pressure_metrics_time_list = pressure_metrics_time_list[:-1]
            arteric_pressure_list = [int(num) for num in arteric_pressure_list.split(',')]
            diastolic_pressure_list = [int(num) for num in diastolic_pressure_list.split(',')]
            pressure_metrics_date_list = [num for num in pressure_metrics_date_list.split(',')]
            pressure_metrics_time_list = [num for num in pressure_metrics_time_list.split(',')]
            a = min(len(pressure_metrics_date_list), len(pressure_metrics_time_list))
            pressure_metrics_list = []
            for i in range(a):
                pressure_metrics_list.append(
                    pressure_metrics_date_list[i] + ' ' + pressure_metrics_time_list[i])
            for k in range(len(diastolic_pressure_list)):
                average_pressure_list.append(
                    (arteric_pressure_list[k] - diastolic_pressure_list[k]) / 3 + diastolic_pressure_list[k])
        if weight_list == None or weight_metrics_date_list == None:
            weight_list, weight_metrics_date_list, last_weight = [], [], 0
        else:
            weight_list = weight_list[:-1]
            weight_metrics_date_list = weight_metrics_date_list[:-1]
            weight_metrics_time_list = weight_metrics_time_list[:-1]
            weight_list = [int(num) for num in weight_list.split(',')]
            weight_metrics_date_list = [num for num in weight_metrics_date_list.split(',')]
            weight_metrics_time_list = [num for num in weight_metrics_time_list.split(',')]
            weight_metrics_list = []
            a = min(len(weight_metrics_date_list), len(weight_metrics_time_list))
            for i in range(a):
                weight_metrics_list.append(weight_metrics_date_list[i] + ' ' + weight_metrics_time_list[i])
            last_weight = str(weight_list[-1])+'кг'
        if temperature_list == None or temperature_metrics_date_list == None:
            temperature_list, temperature_metrics_date_list = [], []
        else:
            temperature_list = temperature_list[:-1]
            temperature_metrics_date_list = temperature_metrics_date_list[:-1]
            temperature_list = [float(num) for num in temperature_list.split(',')]
            temperature_metrics_date_list = [num for num in temperature_metrics_date_list.split(',')]
            temperature_metrics_list = []
            a = min(len(temperature_metrics_time_list), len(temperature_metrics_date_list))
            for i in range(a):
                temperature_metrics_list.append(
                    temperature_metrics_date_list[i] + ' ' + temperature_metrics_time_list[i])
        if oxygen_blood_list == None or oxygen_blood_date_list == None:
            oxygen_blood_list, oxygen_blood_date_list = [], []
        else:
            oxygen_blood_list = oxygen_blood_list[:-1]
            oxygen_blood_date_list = oxygen_blood_date_list[:-1]
            oxygen_blood_time_list = oxygen_blood_time_list[:-1]
            oxygen_blood_list = [float(num) for num in oxygen_blood_list.split(',')]
            oxygen_blood_date_list = [num for num in oxygen_blood_date_list.split(',')]
            oxygen_blood_time_list = [num for num in oxygen_blood_time_list.split(',')]
            oxygen_blood_avg_list = []
            a = min(len(oxygen_blood_time_list), len(oxygen_blood_date_list))
            for i in range(a):
                oxygen_blood_avg_list.append(
                    oxygen_blood_date_list[i] + ' ' + oxygen_blood_time_list[i])
        #Рендерим на сайт
        return render(request, 'superapp/doctor_metrics.html', {'pulse_list': pulse_list, 'pulse_metrics_date_list': pulse_metrics_list,
                                                                'patients': patients, 'arteric_pressure_list': arteric_pressure_list, 'diastolic_pressure_list': diastolic_pressure_list,
                                                                'pressure_metrics_date_list': pressure_metrics_list, 'weight_list': weight_list, 'weight_metrics_date_list': weight_metrics_list, 'patient': patient, 'temperature_list': temperature_list, 'temperature_metrics_list': temperature_metrics_list, 'oxygen_blood_avg_list': oxygen_blood_avg_list, 'oxygen_blood_list': oxygen_blood_list, 'average_pressure_list': average_pressure_list, 'last_weight': last_weight})
    else:
        return render(request, 'superapp/doctor_metrics.html', {'patients': patients})

# форма изменения данных
def change_form(request):
    if request.user.is_doctor:
        form = AboutUserDoctor(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            data = form.cleaned_data
            id_data, created = Doctor.objects.update_or_create(id=request.user.id, defaults=data)
            return redirect('profile')
        else:
            form = AboutUserDoctor()
    else:
        form = AboutUserPatient(request.POST or None)
        if request.method == 'POST' and form.is_valid():
                data = form.cleaned_data
                id_data, created = Doctor.objects.update_or_create(id=request.user.id, defaults=data)
                return redirect('profile')
        else:
            form = AboutUserPatient()
    return render(request, 'superapp/change.html', {'form': form})

# показывает, что пользователь ввел при первом/последующий заполнений анонимно-контактной инфы
def parameters(request):
    return render(request, 'superapp/parameters.html')

# Дневник
def dairy_view(request):
    """ Дневник """

    today = datetime.today().strftime('%Y-%m-%d')
    user = request.user
    if request.user.is_doctor:
        patient = Doctor.objects.get(id=user.last_id)
        patients = Doctor.objects.filter(doctor_id=user.id)
        all_records = ''
        if 'button' in request.POST:
            patient_id = request.POST['patient_id']
            user.last_id = patient_id
            user.save()
            all_records = Dairy.objects.filter(user_id=patient_id)
            last_date = request.POST.get('time_select', 0)
            print(last_date)
            if last_date == 0:
                pass
            else:
                user.last_date = last_date
                user.save()
            t = True
        if 'btn_select' in request.POST:
            last_date = request.POST.get('time_select', 0)
            print(last_date)
            if last_date == 0:
                pass
            else:
                user.last_date = last_date
                user.save()
            t = True
        try:
            if t:
                pass
        except UnboundLocalError:
            t = False
        try:
            records_date = Dairy.objects.filter(Q(time__icontains=user.last_date, user_id=patient.id))
        except ValueError:
            records_date = []
        counter = len(records_date)

        return render(request, 'superapp/dairy.html',
                      {'all_records': all_records, 'records_date': records_date, 'counter': counter, 'today': today,
                       'patient': patient, 'patients': patients, 't': t})

    else:
        all_records = Dairy.objects.filter(user_id=user.id)
        if request.method == 'POST':
            if 'btn_select' in request.POST:
                last_date = request.POST.get('time_select', 0)
                print(last_date)
                if last_date == 0:
                    pass
                else:
                    user.last_date = last_date
                    user.save()
            if 'button' in request.POST:
                content = request.POST['content']
                user_id = user.id
                Dairy.objects.create(content=content, user_id=user_id)

            try:
                records_date = Dairy.objects.filter(Q(time__icontains=user.last_date))
            except ValueError:
                records_date = []

            counter = len(records_date)
            return render(request, 'superapp/dairy.html', {'all_records': all_records, 'records_date': records_date, 'counter': counter, 'today': today})
        else:
            return render(request, 'superapp/dairy.html')

# Чат-комната для прямой связи с доктором
def chat(request):
    id = request.user.id
    user = Doctor.objects.get(id=id)
    if user.doctor_id is not None:
        doctor_name = Doctor.objects.get(id=user.doctor_id)
        doctor_name = doctor_name.surname + ' ' + doctor_name.name + ' ' + doctor_name.fathers_name
    else:
        doctor_name = ''
    if request.user.is_doctor:
        patients = Doctor.objects.filter(doctor_id=id)
        messages = []
        if request.method == 'POST':
            if 'button' in request.POST:
                patient_id = request.POST['patient_id']
                messages = Message.objects.filter(patient_id=patient_id, doctor_id=request.user.id).order_by('time')
                user.last_id = patient_id
                user.save()
                patient_klap = Doctor.objects.get(id=patient_id)
                patient_klap = patient_klap.klapan
            if 'send' in request.POST:
                patient_id = request.user.last_id
                messages = Message.objects.filter(patient_id=patient_id, doctor_id=request.user.id).order_by('time')
                sender = request.user.username
                content = request.POST['content']
                Message.objects.create(sender=sender, content=content, patient_id=patient_id, doctor_id=request.user.id)
                patient_klap = Doctor.objects.get(id=patient_id)
                patient_klap = patient_klap.klapan
        else:
            patient_klap = ''
        return render(request, 'superapp/room.html', {"messages": messages, 'patients': patients, 'patient_klap': patient_klap })
    else:
        if request.method == 'POST' and 'send' in request.POST:
            sender = request.user.username
            content = request.POST['content']
            Message.objects.create(sender=sender, content=content, patient_id=request.user.id, doctor_id=request.user.doctor_id)
            return redirect('chat')

        messages = Message.objects.filter(patient_id=request.user.id, doctor_id=request.user.doctor_id).order_by('time')
        return render(request, 'superapp/room.html', {"messages": messages, 'doctor_name': doctor_name})

# Изменение пароля
def change_password(request):
    if request.method == 'POST':
        if 'button' in request.POST:
            data_klapan = request.POST['klapan']
            t_user = get_object_or_404(Doctor, klapan=data_klapan)
            data_password = request.POST['password']
            t_user.password = data_password
            t_user.save()
            return redirect('profile')
    return render(request, 'superapp/change_password.html')

# коды доступа в случае утери пароля
def codes(request):
    codes = request.user.codes
    codes = codes[1:-1]
    codes = [i for i in codes.split(',')]
    return render(request, 'superapp/codes.html', {'codes': codes})