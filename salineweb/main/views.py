from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
from .models import patient
from numpy import unique

def floors():                         #for nav bar floors
	all_floors = []
	for p in patient.objects.all():
		all_floors.append(p.floor)
	return unique(all_floors)

def rooms_under_Floor(floor_no):        #for floor page
    all_rooms = []
    for p in patient.objects.filter(floor=floor_no):
        all_rooms.append(p.room)
    return unique(all_rooms)

def beds_under_Room(floor_no,room_no):        #for floor page
	all_beds = []
	for p in patient.objects.all(room=room_no,floor=floor_no):
			all_beds.append(p.bed_no)
	return all_beds



def homepage(request):
	#return HttpResponse('<h1>Hi Akash</h1>')
	#a= patient(floor='1',room='1',bed_no='8',percentage='45')
	return render(request=request,template_name="index.html",
				  context={"patients":patient.objects.all,
				  "floors":floors(),
				  "critical_value":20})

def floor(request , floor_no=1):

	return render(request=request,template_name="floor.html",
				  context={"patients":patient.objects.all,
				  "floors":floors(),
				  "floor_no":floor_no,
				  #"room_no":room_no,
				  "rooms_under_Floor":rooms_under_Floor(floor_no),
				  "patient_count":patient.objects.filter(floor = floor_no).count()})


def room(request ,floor_no=1, room_no=1):

	return render(request=request,template_name="room.html",
				  context={"patients":patient.objects.all,
				  "floors":floors(),
				  "floor_no":floor_no,
				  "room_no":room_no})
'''
def room2(request):
	#return HttpResponse('<h1>Hi Akash</h1>')
	return render(request,"room2.html")
'''