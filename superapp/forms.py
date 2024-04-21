from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


#Ввод данных о себе для доктора
class AboutUserDoctor(forms.ModelForm):
    surname = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Иванов", "style": "background-color: #F1F1F1"}))
    name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Иван", "style": "background-color: #F1F1F1"}))
    fathers_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Иванович", "style": "background-color: #F1F1F1"}))
    t_number = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "+79001234567", "style": "background-color: #F1F1F1"}))
    workplace = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "ул. Пушкина, д.12, каб.100", "style": "background-color: #F1F1F1"}))
    position = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Кардиолог", "style": "background-color: #F1F1F1"}))
    class Meta:
        model = Doctor
        fields = ['surname', 'name', 'fathers_name', 't_number', 'workplace', 'position']

#Ввод данных о себе для пациента
class AboutUserPatient(forms.ModelForm):
    klapan = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "1234 5678910", "style": "background-color: #F1F1F1"}))
    sex_choices = [
        ('Мужской', 'Мужской'),
        ('Женский', 'Женский'),
    ]
    sex = forms.ChoiceField(choices=sex_choices)
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={"placeholder": "ГГГГ-ММ-ДД", "style": "background-color: #F1F1F1", "contenteditable": "true"}))
    date_of_operation = forms.DateField(
        widget=forms.DateInput(attrs={"placeholder": "ГГГГ-ММ-ДД", "style": "background-color: #F1F1F1"}))
    height = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "175", "style": "background-color: #F1F1F1"}))
    date_of_made_klapan = forms.DateField(
        widget=forms.DateInput(attrs={"placeholder": "ГГГГ-ММ-ДД", "style": "background-color: #F1F1F1"}))
    manufacturer = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "СКБ МТ", "style": "background-color: #F1F1F1"}))
    allergies = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Полленос", "style": "background-color: #F1F1F1"}))
    intolerant_drugs = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Амиксин", "style": "background-color: #F1F1F1"}))
    class Meta:
        model = Doctor
        fields = ['klapan', 'sex', 'date_of_birth',
                  'date_of_operation', 'height', 'date_of_made_klapan', 'manufacturer', 'allergies', 'intolerant_drugs']

#Регистрация пользователя
class RegisterFormDoctors(UserCreationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Никнейм",
                                                             "style": "background-color: #F1F1F1"}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Электронная почта",
                                                             "style": "background-color: #F1F1F1"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Пароль",
                                                                 "style": "background-color: #F1F1F1"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Подтвердите пароль",
                                                                 "style": "background-color: #F1F1F1"}))
    is_doctor = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={"id": "exampleCheck1"}))
    class Meta:
        model = Doctor
        fields = ['username', 'email', 'password1', 'password2', 'is_doctor']

#Авторизация и аутентификация пользователя
class DoctorLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "id": "InputLogin", "placeholder": "Никнейм",
                                                             "style": "background-color: #F1F1F1"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "id": "InputPassword", "placeholder": "Пароль",
                                                                 "style": "background-color: #F1F1F1"}))
    class Meta:
        model = Doctor
        fields = ['username', 'password']

#Комментарии, лекарства и болезни пациента - вводит врач
class Comments_for_patient(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['comments', 'drugs', 'illnesses']

#Измерения
class Patient_metrics(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['heart_pulse']