from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import Context, loader
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
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

def all_rooms():
	all_floors = floors()
	rooms = {}
	for floor in all_floors:
		rooms[floor] = rooms_under_Floor(floor)
	return rooms

@login_required
def homepage(request):
	patients = patient.objects.all().order_by('percentage')
	lowest_level = 100
	if(len(patients)):
		lowest_level = patients[0].percentage

	return render(request=request,template_name="index.html",
				  context={"lowest_level":lowest_level,
				  "floors":floors(),
				  "rooms":all_rooms(),
				  "critical_value":20})
@login_required
def criticalpatient(request):
	return render(request=request,template_name="criticalpatient.html",
				  context={"patients":patient.objects.all,
				  "floors":floors(),
				  "rooms":all_rooms(),
				  "critical_value":20})

@login_required
def dangerpatient(request):
	#return HttpResponse('<h1>Hi Akash</h1>')
	#a= patient(floor='1',room='1',bed_no='8',percentage='45')
	return render(request=request,template_name="dangerpatient.html",
				  context={"patients":patient.objects.all,
				  "floors":floors(),
				  "rooms":all_rooms(),
				  "critical_value":10})

@login_required
def floor(request , floor_no=1):

	return render(request=request,template_name="floorhome.html",
				  context={"patients":patient.objects.all,
				  "floors":floors(),
				  "floor_no":floor_no,
				  "rooms":all_rooms(),
				  "rooms_under_Floor":rooms_under_Floor(floor_no),
				  "percentage":100,
				  "patient_count":patient.objects.filter(floor = floor_no).count()})

@login_required
def floorquery(request , floor_no=1,percentage = 100):
	if request.method == 'POST':
		percentage_value = int(request.POST.get('percentage_value',''))
	return render(request=request,template_name="floorhome.html",
				  context={"patients":patient.objects.all,
				  "floors":floors(),
				  "floor_no":floor_no,
				  "rooms":all_rooms(),
				  "rooms_under_Floor":rooms_under_Floor(floor_no),
				  "percentage":percentage_value,
				  "patient_count":patient.objects.filter(floor = floor_no).count()})

@login_required
def roomquery(request , floor_no=1, room_no=1, percentage = 100):
	if request.method == 'POST':
		percentage_value = int(request.POST.get('percentage_value',''))
	return render(request=request,template_name="room.html",
				  context={"patients":patient.objects.all,
				  "floors":floors(),
				  "floor_no":floor_no,
				  "rooms_under_Floor":rooms_under_Floor(floor_no),
				  "rooms":all_rooms(),
				  "percentage":percentage_value,
				  "room_no":room_no})

@login_required
def room(request ,floor_no=1, room_no=1, percentage = 100):
	
	return render(request=request,template_name="room.html",
				  context={"patients":patient.objects.all,
				  "floors":floors(),
				  "floor_no":floor_no,
				  "rooms_under_Floor":rooms_under_Floor(floor_no),
				  "rooms":all_rooms(),
				  "percentage":100,
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
			context={"dynamicpercentage": ajaxObject.percentage, "bed_ajax": ajaxObject.bed_no,
					"critical_value":20, 'danger_value':10 })


def ajaxhomeroomdata(request):
	if request.method == 'GET':
		return render(request=request,template_name="ajaxhomeroomdata.html",
					context={"patients": patient.objects.all().order_by('percentage'),
				  	"floors":floors(),
				  	"danger_value":10, "critical_value":20})

def ajaxcriticalroomdata(request):
	if request.method == 'GET':
		return render(request=request,template_name="ajaxcriticalroomdata.html",
					context={"patients":patient.objects.all,
				  	"floors":floors(),
				  	"critical_value":20, "danger_value":10})

def ajaxdangerroomdata(request):
	if request.method == 'GET':
		return render(request=request,template_name="ajaxdangerroomdata.html",
					context={"patients":patient.objects.all,
				  	"floors":floors(),
				  	"danger_value":10})

def ajaxstatus(request):
	if request.method == 'GET':
		received_device = request.GET.get('sent_device')
		received_status = request.GET.get('sent_status')

		received_ID= patient.objects.filter(device_id=received_device)
		received_ID.update(status=received_status)


@login_required
def devices(request):
	if request.method == 'POST':
		new_device_id = request.POST.get('device_id','')
		new_patient_id = request.POST.get('patient_id','')
		new_floor = request.POST.get('floor','')
		new_room = request.POST.get('room','')
		new_bed_no = request.POST.get('bed_no','')

		device_to_delete = request.POST.get('delete','')

		if new_device_id != "" and new_floor != "" and new_room != "" and new_bed_no != "" and new_patient_id != "": #update or create will work only if all fields are filled

			if patient.objects.filter(device_id=new_device_id):
				received_ID= patient.objects.filter(device_id=new_device_id)
				received_ID.update(floor=new_floor,room=new_room,bed_no=new_bed_no, patient_id=new_patient_id)
				#return HttpResponse('Data successfully updated')
			else:
				patient.objects.create(device_id=new_device_id, patient_id=new_patient_id, floor=new_floor,room=new_room,bed_no=new_bed_no)
				#return HttpResponse('Data successfully created')
		elif device_to_delete !="": #Delete operation block
			patient.objects.filter(device_id=device_to_delete).delete()

	return render(request, template_name='devices.html',
				context={"patients":patient.objects.all})


@csrf_exempt
def receive(request):#receive percentage from device and send status
	received_values = request.body.decode('utf-8').split(",")
	#The received_values list will be now like this [devive_id,percentage] e.g. [pat0001,90]
	device_id=received_values[0]
	percentage=received_values[1]

	STATUS = []
	STATUS = [patient.objects.get(device_id=device_id).buzzer_status, patient.objects.get(device_id=device_id).status] #buzzer_status and staus taken to STATUS variable
	received_ID= patient.objects.filter(device_id=device_id)
	received_ID.update(buzzer_status = 5)	#again setting up buzzer_status to default(5)

	if patient.objects.filter(device_id=device_id):
		received_ID= patient.objects.filter(device_id=device_id)
		received_ID.update(percentage=percentage)
		return HttpResponse(STATUS)
	else:
		return HttpResponse('This Device is not in Database!!!')
	
@csrf_exempt
def mute(request, device_id = 'DEV00001'):
	
	new_device_id = request.POST.get('device_id','')
	received_ID= patient.objects.filter(device_id=device_id)
	received_ID.update(buzzer_status = 6)#updating buzzer_status when pressed mute button
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))