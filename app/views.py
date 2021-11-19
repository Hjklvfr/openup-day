from django.shortcuts import render, redirect


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        room_name = request.POST['room_name']

        if not username or len(username) < 2:
            return render(request, 'app/login.html')

        request.session['username'] = username
        return render(request, 'app/chat.html', {
            'username': username,
            'room_name': room_name,
        })
    return render(request, 'app/login.html')


def chat(request, room_name):
    try:
        username = request.session['username']
    except KeyError:
        return redirect('login')
    return render(request, 'app/chat.html', {
        'username': username,
        'room_name': room_name,
    })
