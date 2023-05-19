
#from django.views.generic import TemplateView, View
from django.shortcuts import redirect, render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Room,Topic,Messages,User,Profile
from .forms import RoomForm
from .forms import MessageForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages




def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''


    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )


    roomDisp = rooms.count()


    topics = Topic.objects.all()
    userProfile = Profile.objects.all()

    context = {
        'room': rooms,
        'topics': topics,
        'roomDisp': roomDisp,
        'userProfile': userProfile,
    } 


    return render(request,'pages/index.html', context)


def userProfile(request,pk):
    # rooms = User.room_set.all()
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    context = {'user':user, 'room':rooms}
    return render(request, 'pages/profile.html', context)




def details(request, pk):
    room = Room.objects.get(id=pk)
    messages = room.messages_set.all().order_by('-created')
    user_room = room.participants.all()
    context = {
        'room': room,
        'messages': messages,
        'user_room': user_room,
    }


    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save(request.user, room)
            return redirect('rooms', pk=room.id)
        else:
            form = MessageForm()    
    return render(request, 'pages/room.html',context)
    
@login_required
def create_room(request):
    form = RoomForm()
    
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            cleaned_data = form.clean()
            topic = cleaned_data.get('topic')
            name = cleaned_data.get('name')
            description = cleaned_data.get('description')
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            messages.success(request, 'Sala creada correctamente')

            return redirect(to='home')
        else:
            form = RoomForm()

    context={
        'form': form
    }

    return render(request, 'pages/room_form.html', context)



@login_required
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse("No estás validado aquí")


    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            cleaned_data = form.clean()
            host = cleaned_data.get('host')
            topic = cleaned_data.get('topic')
            name = cleaned_data.get('name')
            description = cleaned_data.get('description')
            form.save()
            messages.success(request, 'Sala modificada correctamente')

            return redirect(to='home')
        else:
            form = RoomForm()
    context = {'form': form}
    return render(request, 'pages/update_room.html', context)

@login_required
def deleteRoom(request,pk):
    
    room = get_object_or_404(Room, id=pk)
    room.delete()
    messages.success(request, 'Sala eliminada correctamente')
    return redirect(to="home")
     

@login_required
def deleteMessage(request,pk):

     
    message = get_object_or_404(Messages, id=pk)

    message.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))
# Create your views here.
