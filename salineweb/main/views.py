from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
from django.views.decorators.csrf import csrf_exempt
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
    room_data = [(i,all_rooms.count(i), patient.objects.filter(floor = floor_no , room = i , percentage__lte = 20).count() ) for i in unique(all_rooms)]
    return room_data

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


def ajaxroomdata(request):
	if request.method == 'GET':
		received_floor = request.GET.get('sent_floor')
		received_room = request.GET.get('sent_room')
		received_bed = request.GET.get('sent_bed')
		ajaxObject = patient.objects.get(floor = received_floor,room=received_room,bed_no=received_bed)
		return render(request=request,template_name="ajaxroomdata.html",
			context={"dynamicpercentage": ajaxObject.percentage,
					"critical_value":20 })

def ajaxhomeroomdata(request):
	if request.method == 'GET':
		return render(request=request,template_name="ajaxhomeroomdata.html",
					context={"patients":patient.objects.all,
				  	"floors":floors(),
				  	"critical_value":20})

@csrf_exempt
def receive(request):
	received_values = request.body.decode('utf-8').split(",")
	#The received_values list will be now like this [floor,room,bed_no,percentage] e.g. [1,2,3,90]
	floor=received_values[0]
	room=received_values[1]
	bed_no=received_values[2]
	percentage=received_values[3]

	if patient.objects.filter(floor=floor,room=room,bed_no=bed_no):
		received_ID= patient.objects.filter(floor=floor,room=room,bed_no=bed_no)
		received_ID.update(percentage=percentage)
		return HttpResponse('Data successfully updated')
	else:
		patient.objects.create(floor=floor,room=room,bed_no=bed_no,percentage=percentage)
		return HttpResponse('Data successfully created')
	
	



