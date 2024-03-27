from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import Login_Form, Create_Account_Form, Notes
from .models import UserData
from django.db import transaction


login_form = Login_Form()
sign_up = Create_Account_Form()
notes = Notes()
# delete_notes = DeleteNotes()
data = {'login': login_form, 'signup': sign_up, 'notes':notes, 'message': ""}


def encrypt(text, s):
    result = ""
    for i in range(len(text)):
        letter = text[i]
        result += chr(ord(letter) + s * 10 % 26 + 65)
    return result

def decrept(enc_pass, s):
    result = ""
    for i in range(len(enc_pass)):
        letter = enc_pass[i]
        result += chr(ord(letter) - s * 10 % 26 - 65)
    return result



def home_page(request):
    my_cookie_value = request.COOKIES.get('jnl')
    data['mkc'] = my_cookie_value

    if my_cookie_value:
        email = decrept(my_cookie_value, 69)

        user_data = UserData.objects.filter(email = email).first()

        if user_data:
            all_notes = user_data.all_notes
            fav_notes = user_data.favourite_notes

            data['all_notes'] = all_notes
            data['fav_notes'] = fav_notes



    return render(request, 'Index.html', data)


def login(request):
    message = ""
    if request.method == "POST":
        login_form = Login_Form(request.POST)

        if login_form.is_valid():
            user_data = login_form.cleaned_data

            mysql_entry = UserData.objects.filter(email=user_data['email']).first()
            if mysql_entry:
                if mysql_entry.password == user_data['password'] and mysql_entry.email == user_data['email']:
                    mail = encrypt(user_data['email'], 69)
                    message = "Logged In"
                    response = HttpResponseRedirect(reverse('home'))
                    response.set_cookie('jnl', mail)
                    data['message'] = message
                    return response

                else:
                    message = "Invalid Credentials"

            else:
                message = "No user found with this email. Please Signup"

        else:
            message = "Invalid form submission"

    else:
        message = "404 Network Error"

    data['message'] = message
    return redirect(reverse('home'))

def signup(request):
    message = ""
    if (request.method == "POST"):
        signup_form = Create_Account_Form(request.POST)

        if signup_form.is_valid():
            user_data = signup_form.cleaned_data
            email = user_data.get('email')

            if UserData.objects.filter(email=email).exists():
                message = "Email Already Exist"

            else:
                with transaction.atomic():
                    user = UserData.objects.create(
                    user_name = user_data.get("name"),
                    email = user_data.get("email"),
                    password = user_data.get("password")
                )
                    user.save()
                    message = "Account created please login"
        else:
            message = "Invalid form submission"
    else:
        message = "404 Network Error"

    data['message'] = message
    return redirect(reverse('home'))

def logout(request):
    response = HttpResponseRedirect(reverse('home'))
    response.delete_cookie('jnl')
    data['message'] = "Logged Out"
    return response

def save(request):
    message = ""
    my_cookie_value = request.COOKIES.get('jnl')
    if my_cookie_value:
        my_cookie_value = decrept(my_cookie_value, 69)
    else:
        message = "Please Login"

    if (request.method == "POST"):
        note = Notes(request.POST)

        if note.is_valid():
            title = note.cleaned_data['title']
            note_contant = note.cleaned_data['note']

            if note_contant:
                if not title:
                    title = ' '.join(note_contant.split()[:2])

                user_data = get_object_or_404(UserData, email=my_cookie_value)
                user_data.all_notes[title] = note_contant

                user_data.save()

                message = "Note Saved"

            else:
                message = "Note not saved !!"

        else:
            message = "Note not saved !!"


    else:
        message = "404 Network Error"

    data ['message'] = message
    return redirect(reverse('home'))


def delete(request):
    if request.method == 'POST':
        title = request.POST.get('project')
        note = request.POST.get('note')

        email = decrept(request.COOKIES.get('jnl'), 69)
        user_data = UserData.objects.filter(email=email).first()

        if user_data:
            all_notes = user_data.all_notes
            fav_notes = user_data.favourite_notes

            if title in all_notes:
                del all_notes[title]
                data['message'] = "Note deleted"
            if title in fav_notes:
                del fav_notes[title]
                data['message'] = "Note deleted"

            user_data.save()

    return redirect(reverse('home'))



