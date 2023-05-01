import os
from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Q
from .models import *
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from datetime import date
from django.contrib.auth import logout



def resume(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        dob = request.POST.get('dob')
        contact = request.POST.get('contact')
        photo = request.FILES.get('photo')
        resume = request.FILES.get('resume')
        skill = request.POST.get('skill')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if Job_Seekers.objects.filter(email=email).exists():
            msg='User Already Exists'
            return render(request, 'seekera/create-resume.html',{'msg':msg})
        seeker = Job_Seekers(name=name, address=address, dob=dob, contact=contact,
                            photo=photo, resume=resume, skill=skill, email=email,
                            password=password)

            # Save the object to the database
        seeker.save()

            # Redirect to a success page
        return redirect('/login2')

    return render(request, 'seekera/create-resume.html')

def company(request):
    if request.method == 'POST':
        cname = request.POST.get('cname')
        ceo = request.POST.get('ceo')
        tagline = request.POST.get('tagline')
        des = request.POST.get('des')
        phone = request.POST.get('phone')
        website = request.POST.get('website')
        category = request.POST.get('category')

        empno = request.POST.get('empno')
        started = request.POST.get('started')
        email = request.POST.get('email')
        password = request.POST.get('password')
        photo=request.FILES.get('photo')
        license=request.FILES.get('license')
        # Check if email already exists
        if Job_Providers.objects.filter(email=email).exists():
            msg = 'User Already Exists'
            return render(request, 'seekera/create-company.html',{'msg':msg})

        # Create Job_Providers object and save to database
        Job_Providers.objects.create(
            cname=cname,
            ceo=ceo,
            tagline=tagline,
            category=category,
            des=des,
            phone=phone,
            website=website,
            empno=empno,
            started=started,
            email=email,
            password=password,
            license=license,
            photo=photo
        )

        # Redirect to login page
        return redirect('/login2')

    return render(request, 'seekera/create-company.html')
def contact(request):
    return render(request, 'seekera/contact-us.html')
def login(request):
    if request.method == "POST":

        email = request.POST.get('email')
        password = request.POST.get('password')
        obj1 = Job_Providers.objects.filter(email=email, password=password)
        obj2 = Job_Seekers.objects.filter(email=email, password=password)
        if obj1.filter(email=email, password=password).exists():
            for i in obj1:
                pid = i.pid
                z = i.status
                cname=i.cname
                request.session['email'] = email
                request.session['password'] = password
                request.session['pid'] = pid
                request.session['status'] = z
                request.session['cname']=cname
            # context ={'a': obj }
            if z == 'Verified':
                a = Post_Job.objects.filter(pid=pid)
                b = Job_Providers.objects.filter(pid=pid)
                noti=Apply.objects.filter(pid=pid).order_by('-timestamp')[:10]
                all = {
                    'a': a,
                    'b': b,
                    'noti':noti,
                }
                return render(request, 'seekera/jobproviderhome.html', all)
            else:
                msg='Your Account Verification Is Under Processing'
                return render(request, 'seekera/login.html',{'msg2':msg})
        elif obj2.filter(email=email, password=password).exists():
            for i in obj2:
                sid = i.sid
                name = i.name
                request.session['name'] = name
                request.session['email'] = email
                request.session['password'] = password
                request.session['sid'] = sid
                b = Job_Seekers.objects.filter(sid=sid)
                a = Post_Job.objects.filter(status='Open').order_by('-timestamp')
                noti = Post_Job.objects.filter(status='Open').order_by('-timestamp')[:3]
                noti2 = Apply.objects.filter(sid=sid).order_by('-timestamp')[:3]
                all = {
                    'a': a,
                    'b': b,
                    'noti':noti,
                    'noti2':noti2,
                }
            return render(request, 'seekera/jobseekerhome.html', all)

        else:
            context = {'msg': 'Invalid Credentials'}
            return render(request,'seekera/login.html',context)
    return render(request, 'seekera/login.html')

def editseeker(request):
    if request.method == 'POST':
        sid = request.session['sid']
        b = Job_Seekers.objects.filter(sid=sid)
        up = Job_Seekers.objects.get(sid=sid)
        name = request.POST.get('name')
        address = request.POST.get('address')
        contact = request.POST.get('contact')
        skill = request.POST.get('skill')
        email = request.POST.get('email')
        if request.FILES:
            image_file = request.FILES.get('photo')
            resume_file = request.FILES.get('resume')

            if image_file:
                up.photo = image_file

            if resume_file:
                up.resume = resume_file

            up.save()




        up.name = name
        up.address = address
        up.contact = contact
        up.skill = skill
        up.email = email

        up.save()
        ud = Job_Seekers.objects.filter(email=request.session['email'])
        context = {'details': ud,
                   'b': b,
                   'msg':'Profile Details Updated'}

        return render(request, 'seekera/editprofile-seeker.html', context)


    else:
        id = request.GET.get('sid')
        sid = request.session['sid']
        up = Job_Seekers.objects.filter(sid=id)
        b = Job_Seekers.objects.filter(sid=sid)
        noti = Post_Job.objects.filter(status='Open').order_by('-timestamp')[:3]
        noti2 = Apply.objects.filter(sid=sid).order_by('-timestamp')[:3]
        all = {
            'b': b,
            'details': up,
            'noti':noti,
            'noti2':noti2
        }
        return render(request, 'seekera/editprofile-seeker.html',all)


def alljobs(request):
    today = date.today()
    a = Post_Job.objects.filter(
        Q(status='Open') & Q(deadline__gte=today)
    ).order_by('-timestamp')
    return render(request,'seekera/alljobs.html',{"a":a})



def home_view(request):
    if request.method == "POST":

        email = request.POST.get('email')
        password = request.POST.get('password')
        obj1 = Job_Providers.objects.filter(email=email,password=password)
        obj2 = Job_Seekers.objects.filter(email=email,password=password)
        if obj1.filter(email=email, password=password).exists():
            for i in obj1:
                pid = i.pid
                z= i.status
                cname=i.cname
                request.session['email'] = email
                request.session['password'] = password
                request.session['status'] = z
                request.session['pid'] = pid
                request.session['cname']=cname
            # context ={'a': obj }
            if z == 'Verified':
                a=Post_Job.objects.filter(pid=pid)
                b = Job_Providers.objects.filter(pid=pid)
                noti = Apply.objects.filter(pid=pid).order_by('-timestamp')[:10]
                all = {
                    'a': a,
                    'b': b,
                    'noti':noti
                }
                return render(request, 'seekera/jobproviderhome.html', all)
            else:
                return redirect('/login2')
        elif obj2.filter(email=email, password=password).exists():
            for i in obj2:
                sid = i.sid
                name = i.name
                request.session['name'] = name
                request.session['email'] = email
                request.session['password'] = password
                request.session['sid'] = sid
                b=Job_Seekers.objects.filter(sid=sid)
                noti=Post_Job.objects.filter(status='Open').order_by('-timestamp')[:3]
                noti2=Apply.objects.filter(sid=sid).order_by('-timestamp')[:3]
                a = Post_Job.objects.filter(status='Open').order_by('-timestamp')
                all={
                    'a':a,
                    'b':b,
                    'noti':noti,
                    'noti2':noti2,
                }
            return render(request, 'seekera/jobseekerhome.html',all)

        else:
            context = {'msg': 'Invalid Credentials'}
            return redirect('/login2')

    else:
        a = Post_Job.objects.filter(status='Open').order_by('-timestamp')[:3]
        total_candidates = Job_Seekers.objects.all().count()
        total_companies = Job_Providers.objects.all().count()
        b=Review.objects.order_by('-created_at')[:3]
        context = {
            'total_companies': total_companies,
            'total_candidates': total_candidates,
            'a': a,
            'b': b
        }
        print('ok')
        return render(request, 'seekera/index.html', context)
def single_job_view(request,jid,category):
    a=Post_Job.objects.filter(jid=jid)
    c=Post_Job.objects.filter(category=category).exclude(jid=jid)
    all={
        'a':a,
        'c':c
    }
    return render(request, 'seekera/job-single.html',all)
def single_job_view_seeker(request,jid):
    sid=request.session['sid']
    c=Apply.objects.filter(jid=jid)
    a=Post_Job.objects.filter(jid=jid)
    b = Job_Seekers.objects.filter(sid=sid)
    noti = Post_Job.objects.filter(status='Open').order_by('-timestamp')[:3]
    noti2 = Apply.objects.filter(sid=sid).order_by('-timestamp')[:3]
    all = {
        'a': a,
        'b': b,
        'c':c,
        'noti':noti,
        'noti2':noti2
    }
    if Apply.objects.filter(sid=sid, jid=jid).exists():
        return render(request, 'seekera/already_single-seeker.html', all)
    else:
        return render(request, 'seekera/single-seeker.html',all)

def jobs_by_category(request,id):
    sid = request.session['sid']
    today = date.today
    a=Post_Job.objects.filter(category=id).order_by('-timestamp')
    b = Job_Seekers.objects.filter(sid=sid)
    noti = Post_Job.objects.filter(status='Open').order_by('-timestamp')[:3]
    noti2 = Apply.objects.filter(sid=sid).order_by('-timestamp')[:3]
    all = {
        'a': a,
        'b': b,
        'noti':noti,
        'noti2':noti2
    }
    return render(request, 'seekera/category.html',all)

def company_job_view(request):
    try:
        pid = request.session['pid']
        print(pid)
        a = Post_Job.objects.filter(pid=pid).order_by('-timestamp')
        return render(request,'seekera/companyview.html',{"a":a})
    except:
        return login(request)


def apply(request,jid):
    try:
        ab = request.session['sid']
        print(ab)
        name = request.session['name']
        email = request.session['email']
        obj = Post_Job.objects.filter(jid=jid)
        for i in obj:
            y = i.jid
            x = i.pid
            cname = i.cname
            title = i.title
            type = i.type
            request.session['jid'] = y
            request.session['pid'] = x
            if Apply.objects.filter(sid=ab,jid=y).exists():
                today = date.today()
                a = Post_Job.objects.filter(
                    Q(status='Open') & Q(deadline__gte=today)
                ).order_by('-timestamp')
                b = Job_Seekers.objects.filter(sid=ab)
                noti = Post_Job.objects.filter(status='Open').order_by('-timestamp')[:3]
                noti2 = Apply.objects.filter(sid=ab).order_by('-timestamp')[:3]
                context = {
                    'msg': '<h6>You are already applied for this job!!</h6>',
                    'a':a,
                    'b':b,
                    'noti':noti,
                    'noti2':noti2
                }
                return render(request, "seekera/jobseekerhome.html",context)
            else:
                va = Apply(sid=ab,name=name,pid=x,jid=y,cname=cname,title=title,type=type,email=email,status='NOT SELECTED')
                va.save()
                return redirect('http://127.0.0.1:8000/applied')
    except:
        return login(request)


def appliedjobs(request):
    try:
        sid = request.session['sid']
        print(sid)
        a = Apply.objects.filter(sid=sid)
        # c = Apply.objects.filter(sid=sid)
        b=Job_Seekers.objects.filter(sid=sid)
        noti = Post_Job.objects.filter(status='Open').order_by('-timestamp')[:3]
        noti2 = Apply.objects.filter(sid=sid).order_by('-timestamp')[:3]

        all = {
            'a': a,
            'b': b,
            'noti':noti,
            'noti2':noti2,
            # 'c': c
        }
        return render(request, "seekera/applied.html", all)
    except:
        return login(request)

def deleteappliedjob(request,id):
    a = Apply.objects.get(id=id)
    a.delete()
    return redirect("http://127.0.0.1:8000/applied")
def alljobs_seeker(request):
    try:
        sid = request.session['sid']
        print(sid)
        today = date.today()
        a = Post_Job.objects.filter(
            Q(status='Open') & Q(deadline__gte=today)
        ).order_by('-timestamp')

        b = Job_Seekers.objects.filter(sid=sid)
        noti = Post_Job.objects.filter(status='Open').order_by('-timestamp')[:3]
        noti2 = Apply.objects.filter(sid=sid).order_by('-timestamp')[:3]
        all = {
            'a': a,
            'b': b,
            'noti':noti,
            'noti2':noti2
        }
        return render(request,'seekera/alljobs-seeker.html',all)
    except:
        return login(request)

def logout_view(request):
    logout(request)
    print('Logout Succesfully!')
    return redirect('/thankyou')
def search_seeker(request):
    try:
        sid = request.session['sid']
        print(sid)
        b = Job_Seekers.objects.filter(sid=sid)
        noti = Post_Job.objects.filter(status='Open').order_by('-timestamp')[:3]
        noti2 = Apply.objects.filter(sid=sid).order_by('-timestamp')[:3]
        all = {
            'b': b,
            'noti':noti,
            'noti2':noti2
        }
        return render(request,'seekera/search.html',all)
    except:
        return login(request)
def category(request,id):
    a = a=Post_Job.objects.filter(category=id).order_by('-timestamp')
    all = {
        'a': a,
    }
    return render(request, 'seekera/category2.html',all)


def search_results(request):
    title = request.GET.get('title')
    location = request.GET.get('location')
    if title and location:
        results = Post_Job.objects.filter(title__icontains=title, location__iexact=location)
    elif title:
        results = Post_Job.objects.filter(title__icontains=title)
    elif location:
        results = Post_Job.objects.filter(location__iexact=location)
    else:
        results = Post_Job.objects.none()

    return render(request, 'seekera/search_resultshome.html', {'results': results})

def get_suggestions(request):
    term = request.GET.get('term')
    suggestions = Post_Job.objects.filter(title__icontains=term).values_list('title', flat=True)
    return JsonResponse(list(suggestions), safe=False)

def search_results_seeker(request):
    try:
        sid = request.session['sid']
        print(sid)
        b = Job_Seekers.objects.filter(sid=sid)
        noti = Post_Job.objects.filter(status='Open').order_by('-timestamp')[:3]
        noti2 = Apply.objects.filter(sid=sid).order_by('-timestamp')[:3]
        title = request.GET.get('title')
        location = request.GET.get('location')

        if title and location:
            results = Post_Job.objects.filter(title__icontains=title, location__iexact=location)
        elif title:
            results = Post_Job.objects.filter(title__icontains=title)
        elif location:
            results = Post_Job.objects.filter(location__iexact=location)
        else:
            results = Post_Job.objects.none()
        all = {
            'b': b,
            'results': results,
            'noti':noti,
            'noti2':noti2
        }
        return render(request, 'seekera/search_results-seeker.html',all)
    except:
        return login(request)

def viewprofile_seeker(request):
    try:
        sid = request.session['sid']
        print(sid)
        b = Job_Seekers.objects.filter(sid=sid)
        noti = Post_Job.objects.filter(status='Open').order_by('-timestamp')[:3]
        noti2 = Apply.objects.filter(sid=sid).order_by('-timestamp')[:3]
        all = {
            'b': b,
            'noti2':noti2,
            'noti':noti
        }
        return render(request, 'seekera/view_profile_seeker.html', all)
    except:
        return login(request)
def changepassword_seeker(request):
    sid = request.session['sid']
    print(sid)
    b = Job_Seekers.objects.filter(sid=sid)
    noti = Post_Job.objects.filter(status='Open').order_by('-timestamp')[:3]
    noti2 = Apply.objects.filter(sid=sid).order_by('-timestamp')[:3]
    all = {
        'b': b,
        'noti':noti,
        'noti2':noti2
    }
    if request.method == 'POST':
        email = request.session['email']
        new_password = request.POST.get('new_password')
        current_password = request.POST.get('current_password')
        print('Email Is:' + email)
        print("Current_password" + str(current_password))
        try:

            ul = Job_Seekers.objects.get(email=email, password=current_password)

            if ul is not None:
                ul.password = new_password  # change field
                ul.save()
                context = {'msg': 'Password Changed Successfully'}
                all = {
                    'b': b,
                    'msg':context
                }
                return render(request, 'seekera/change_password_seeker.html', all)
            else:
                context = {'msg': 'Your Old Password is Wrong'}
                all = {
                    'b': b,
                    'msg': context
                }
                return render(request, 'seekera/change_password_seeker.html', all)

        except Job_Seekers.DoesNotExist:
            context = {'msg': 'Your Old Password is Wrong'}
            all = {
                'b': b,
                'msg': context
            }
            return render(request, 'seekera/change_password_seeker.html', all)
    else:
        return render(request, 'seekera/change_password_seeker.html',all)


def application_status(request):

    sid = request.session['sid']
    print(sid)
    a = Apply.objects.filter(sid=sid)
        # c = Apply.objects.filter(sid=sid)
    b=Job_Seekers.objects.filter(sid=sid)
    noti = Post_Job.objects.filter(status='Open').order_by('-timestamp')[:3]
    noti2 = Apply.objects.filter(sid=sid).order_by('-timestamp')[:3]
    all = {
        'a': a,
        'b': b,
        'noti':noti,
        'noti2':noti2
        # 'c': c
    }
    return render(request, "seekera/application_status.html", all)

def single_job_view_provider(request,jid):
    pid=request.session['pid']
    a=Post_Job.objects.filter(jid=jid)
    b = Job_Providers.objects.filter(pid=pid)
    noti = Apply.objects.filter(pid=pid).order_by('-timestamp')[:10]
    all = {
        'a': a,
        'b': b,
        'noti':noti
    }
    return render(request, 'seekera/single-provider.html',all)

def deletejob(request,jid):
    pid = request.session['pid']
    a = Post_Job.objects.get(jid=jid)
    b = Job_Providers.objects.filter(pid=pid)
    all = {
        'a': a,
        'b': b
    }
    a.delete()
    return redirect('http://127.0.0.1:8000/managejob')

def managejobs(request):
    pid = request.session['pid']
    a = Post_Job.objects.filter(pid=pid)
    b = Job_Providers.objects.filter(pid=pid)
    noti = Apply.objects.filter(pid=pid).order_by('-timestamp')[:10]
    all = {
        'a': a,
        'b': b,
        'noti':noti,
    }
    return render(request, 'seekera/managejobs.html', all)

def postedjobs(request):
    pid = request.session['pid']
    a = Post_Job.objects.filter(pid=pid)
    b = Job_Providers.objects.filter(pid=pid)
    noti = Apply.objects.filter(pid=pid).order_by('-timestamp')[:10]
    all = {
        'a': a,
        'b': b,
        'noti':noti
    }
    return render(request, 'seekera/jobproviderhome.html', all)

def manage_job_view_provider(request,jid):
    pid=request.session['pid']
    a=Post_Job.objects.filter(jid=jid)
    b = Job_Providers.objects.filter(pid=pid)
    noti = Apply.objects.filter(pid=pid).order_by('-timestamp')[:10]
    all = {
        'a': a,
        'b': b,
        'noti':noti
    }
    return render(request, 'seekera/manage-provider.html',all)

def changeapplicationstatus(request,jid):
    Post_Job.objects.filter(jid=jid).update(status='Closed')
    url = f"/singleee/{jid}"
    return redirect(url)
def startapplicationstatus(request,jid):
    Post_Job.objects.filter(jid=jid).update(status='Open')
    url = f"/singleee/{jid}"
    return redirect(url)


def viewprofile_provider(request):
    try:
        pid = request.session['pid']
        print(pid)
        b = Job_Providers.objects.filter(pid=pid)
        noti = Apply.objects.filter(pid=pid).order_by('-timestamp')[:10]
        all = {
            'b': b,
            'noti':noti
        }
        return render(request, 'seekera/view_profile_provider.html', all)
    except:
        return login(request)

def viewcompanydeatils(request,pid):
    try:
        sid = request.session['sid']
        print(sid)
        a=Job_Providers.objects.filter(pid=pid)
        b = Job_Seekers.objects.filter(sid=sid)
        all = {
            'a': a,
            'b': b,
        }
        return render(request, 'seekera/view_company_details.html', all)
    except:
        return login(request)

def viewappicants(request,jid):
    a = Apply.objects.filter(jid=jid)
    pid = request.session['pid']
    print(pid)
    b = Job_Providers.objects.filter(pid=pid)
    noti = Apply.objects.filter(pid=pid).order_by('-timestamp')[:10]
    for i in a:
        x = i.jid
        y = i.pid
        request.session['jid'] = x
        request.session['pid'] = y
    all = {
        'a':a,
        'b': b,
        'noti':noti
    }
    return render(request,'seekera/viewapplicants.html',all)

def viewapplicantdetails(request,sid):
    a=Job_Seekers.objects.filter(sid=sid)
    pid = request.session['pid']
    print(pid)
    noti = Apply.objects.filter(pid=pid).order_by('-timestamp')[:10]
    b = Job_Providers.objects.filter(pid=pid)
    all = {
        'a': a,
        'b': b,
        'noti':noti
    }
    return render(request,"seekera/viewapplicantdetails.html",all)

def selectcandidate(request,sid):
    jid = request.session['jid']
    Apply.objects.filter(sid=sid,jid=jid).update(status='Selected')
    return redirect('http://127.0.0.1:8000/selectedcandidate')

def selectedcandidates(request):
    pid = request.session['pid']
    print(pid)
    a= Apply.objects.filter(pid=pid,status='Selected')
    b = Job_Providers.objects.filter(pid=pid)
    noti = Apply.objects.filter(pid=pid).order_by('-timestamp')[:10]
    all = {
        'a': a,
        'b': b,
        'noti':noti
    }
    return render(request, "seekera/selectedcandidates.html", all)

    # today = date.today()
    # a = Post_Job.objects.filter(
    #     Q(status='Open') & Q(deadline__gte=today)
    # ).order_by('-timestamp')
def post_job(request):
    if request.method == 'POST':
        title = request.POST['title']
        job_type = request.POST['type']
        location = request.POST['location']
        des = request.POST['des']
        requirement = request.POST['requirement']
        deadline = request.POST['deadline']
        pid = request.session['pid']
        cname = Job_Providers.objects.get(cname=request.session['cname'])
        category = request.POST['category']
        salary = request.POST.get('salary', 'NOT DISCLOSED')

        # create a new instance of Post_Job model with the data
        job_post = Post_Job(title=title, type=job_type, location=location, des=des,
                            reqirement=requirement, pid=pid,
                            cname=cname,category=category, salary=salary,deadline=deadline)
        job_post.save()  # save the new job posting

        messages.success(request, 'Job posted successfully')
        return redirect('http://127.0.0.1:8000/postedjob')
    else:
        pid = request.session['pid']
        print(pid)
        b = Job_Providers.objects.filter(pid=pid)
        noti = Apply.objects.filter(pid=pid).order_by('-timestamp')[:10]
        all = {
            'b': b,
            'noti':noti
        }

        return render(request, 'seekera/postjob.html',all)

def rejectcandidate(request,sid):
    jid = request.session['jid']
    Apply.objects.filter(sid=sid,jid=jid).update(status='Rejected')
    return redirect('http://127.0.0.1:8000/selectedcandidate')

def view_license(request, provider_id):
    provider = get_object_or_404(Job_Providers, pk=provider_id)
    with open(provider.license.path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename={provider.cname}_license.pdf'
        return response

def editprovider(request):
    if request.method == 'POST':
        pid = request.session['pid']
        b = Job_Providers.objects.filter(pid=pid)
        up = Job_Providers.objects.get(pid=pid)
        cname = request.POST.get('cname')
        ceo = request.POST.get('ceo')
        phone=request.POST.get('phone')
        empno = request.POST.get('empno')
        email =request.POST.get('email')
        if request.FILES:
            photo = request.FILES.get('photo')
            license_file = request.FILES.get('license')

            if photo:
                up.photo = photo

            if license_file:
                up.license = license_file

            up.save()




        up.cname = cname
        up.ceo = ceo
        up.empno = empno
        up.email = email
        up.phone = phone

        up.save()
        ud = Job_Providers.objects.filter(email=request.session['email'])
        context = {'details': ud,
                   'b': b,
                   'msg':'Profile Details Updated'}

        return render(request, 'seekera/editprofile-provider.html', context)


    else:
        pid = request.GET.get('pid')
        pid = request.session['pid']
        up = Job_Providers.objects.filter(pid=pid)
        b = Job_Providers.objects.filter(pid=pid)
        noti = Apply.objects.filter(pid=pid).order_by('-timestamp')[:10]
        all = {
            'b': b,
            'details': up,
            'noti':noti
        }
        return render(request, 'seekera/editprofile-provider.html',all)

def changepassword_provider(request):
    pid = request.session['pid']
    print(pid)
    b = Job_Providers.objects.filter(pid=pid)
    noti = Apply.objects.filter(pid=pid).order_by('-timestamp')[:10]
    all = {
        'b': b,
        'noti':noti
    }
    if request.method == 'POST':
        email = request.session['email']
        new_password = request.POST.get('new_password')
        current_password = request.POST.get('current_password')
        print('Email Is:' + email)
        print("Current_password" + str(current_password))
        try:

            ul = Job_Providers.objects.get(email=email, password=current_password)

            if ul is not None:
                ul.password = new_password  # change field
                ul.save()
                context = {'msg': 'Password Changed Successfully'}
                all = {
                    'b': b,
                    'msg':context
                }
                return render(request, 'seekera/change_password_provider.html', all)
            else:
                context = {'msg': 'Your Old Password is Wrong'}
                all = {
                    'b': b,
                    'msg': context
                }
                return render(request, 'seekera/change_password_provider.html', all)

        except Job_Seekers.DoesNotExist:
            context = {'msg': 'Your Old Password is Wrong'}
            all = {
                'b': b,
                'msg': context
            }
            return render(request, 'seekera/change_password_provider.html', all)
    else:
        return render(request, 'seekera/change_password_provider.html',all)

def viewalltestimonials(request):
    review=Review.objects.all().order_by('-created_at')
    return render(request,'seekera/testimonials.html',{'b':review})


def add_review(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        stars = request.POST.get('stars')
        seeker_id = request.session['sid']
        seeker = Job_Seekers.objects.get(sid=seeker_id)
        provider = Job_Providers.objects.get(pid=1)
        review = Review.objects.create(seeker=seeker, title=title, stars=stars,provider=provider,usertype='Job Seeker')
        review.save()
        return render(request,'seekera/thankyou.html')
    else:
        sid=request.session['sid']
        noti = Post_Job.objects.filter(status='Open').order_by('-timestamp')[:3]
        noti2 = Apply.objects.filter(sid=sid).order_by('-timestamp')[:3]
        b=Job_Seekers.objects.filter(sid=sid)
        all={'noti':noti,
             'noti2':noti2,
             'b':b
             }
        return render(request, 'seekera/add_review.html',all)

def add_review_provider(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        stars = request.POST.get('stars')
        provider_id = request.session['pid']
        seeker = Job_Seekers.objects.get(sid=1)
        provider = Job_Providers.objects.get(pid=provider_id)
        review = Review.objects.create(seeker=seeker, title=title, stars=stars,provider=provider,usertype='Provider')
        review.save()
        return render(request,'seekera/thankyou3.html')
    else:
        pid=request.session['pid']
        noti = Apply.objects.filter(pid=pid).order_by('-timestamp')[:10]
        b=Job_Providers.objects.filter(pid=pid)
        all={'noti':noti,
             'b': b
        }
        return render(request, 'seekera/add_review2.html',all)

def thankyou(request):
    return render(request,'seekera/thankyou2.html')

def resume_download(request, sid):
    seeker = get_object_or_404(Job_Seekers, sid=sid)
    file_path = seeker.resume.path
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read())
        response['Content-Type'] = 'application/pdf'
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        return response


