from datetime import date
import requests
import json

resp = json.loads(requests.get('https://www.cbr-xml-daily.ru/daily_json.js').text)
usd = resp.get('Valute').get('USD').get('Value')

class Patient:
    def __init__(self, full_name, address, phone_number, extra_contact):
        self._full_name = full_name
        self._address = address
        self._phone_number = phone_number
        self._extra_contact = extra_contact

    def get_full_name(self):
        return self._full_name
    
    def set_full_name(self, a):
        self._full_name = a

    def get_address(self):
        return self._address
    
    def set_address(self, b):
        self._address = b

    def get_phone_number(self):
        return self._phone_number
    
    def set_phone_number(self, c):
        self._phone_number = c

    def get_extra_contact(self):
        return self._extra_contact
    
    def set_extra_contact(self, d):
        self._extra_contact = d

class Doctor:
    def __init__(self, full_name, specialization, cabinet_number, phone_number):
        self._full_name = full_name
        self._specialization = specialization
        self._cabinet_number = cabinet_number
        self._phone_number = phone_number

    def get_full_name(self):
        return self._full_name
    
    def set_full_name(self, a):
        self._full_name = a

    def get_specialization(self):
        return self._specialization
    
    def set_specialization(self, b):
        self._specialization = b

    def get_cabinet_number(self):
        return self._cabinet_number
    
    def set_cabinet_number(self, c):
        self._cabinet_number = c

    def get_phone_number(self):
        return self._phone_number
    
    def set_phone_number(self, d):
        self._phone_number = d

    
class Procedure:
    def __init__(self, procedure_name, date, doctor, cost):
        self._procedure_name = procedure_name
        self._date = date
        self._doctor = doctor
        self._cost = cost
        
    def get_procedure_name(self):
        return self._procedure_name
    
    def set_procedure_name(self, a):
        self._procedure_name = a

    def get_date(self):
        return self._date
    
    def set_date(self, b):
        self._date = b

    def get_doctor(self):
        return self._doctor
    
    def set_doctor(self, c):
        self._doctor = c

    def get_cost(self):
        return self._cost
    
    def set_cost(self, d):
        self._cost = d

    def __add__(self, other):
        all_cost = (self._cost + other._cost)
        return all_cost
    
    def __str__(self):
        return f"Название: {self._procedure_name}; Дата: {self._date}; Доктор: {self._doctor}; Стоимость в рублях: {self._cost}; Стоимость в долларах: {round(self._cost / usd, 2)} "




Procedure1 = Procedure("Врачебный осмотр", date.today(), "Ирвин", 250)
Procedure2 = Procedure("Рентгеноскопия", date.today(), "Джемисон", 500)
Procedure3 = Procedure("Анализ крови", date.today(), "Смит", 200)
House = Doctor("Доктор Хаус", "Хирург", 203, 899999999) 






