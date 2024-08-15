from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import SignUpForm


# Create your views here.
def frontpage(request):
    return render(request,'core/frontpage.html') 

@login_required
def signup(request):
    print()
    if request.method=='POST':

        form = SignUpForm(request.POST)

        if form.is_valid():

            user=form.save()

            login(request,user)

            print('valid')    
            return redirect('frontpage')

        print('valid')    
    else:
        print('notvalid')    
        if request.user.is_superuser:
            print('is super user')   
            form = SignUpForm()
            return render(request,'core/signup.html',{'form':form})
        else:
            print('is not super user')   

            return redirect('frontpage')
    
    return redirect('frontpage')
