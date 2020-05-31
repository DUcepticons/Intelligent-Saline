# Intelligent-Saline

cmd>> ipconfig
See the server ip address (192.168.0.xxx)

Edit those two NodeMCU code lines:
const char *host = "192.168.0.xxx"; 
String Link = "http://192.168.0.xxx:8000/receive/";

Instruction to run server (USE IP OTHERWISE NODEMCU DATA WON'T BE RECEIVED): python manage.py runserver 192.168.0.xxx:8000
In a browser go to - 192.168.0.xxx:8000
Voilla!! Here you go....


Existing login: 
ducepticons
saline123

To Create a new user: python manage.py createsuperuser

django 3.0.3


To use database in command shell:
going to command shell>> python manage.py shell
>> from main.models import patient
>> object = patient.objects.all()