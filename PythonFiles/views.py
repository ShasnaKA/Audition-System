from django.shortcuts import render
# Create your views here.

from django.db.models import Max ## Foreign key usage

def index(request):
    return render(request, './myapp/index.html')


def about(request):
    return render(request, './myapp/about.html')

from .models import tbl_Contact

def contact(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        msg = request.POST.get('msg')
        contact_list = tbl_Contact(email=email, contact=contact, msg=msg)
        contact_list.save()
        return render(request, './myapp/contact.html')
    else:
        return render(request, './myapp/contact.html')


from .models import tbl_Login

def admin_login(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        pswd = request.POST.get('pswd')
        #query to select a record based on a condition
        ul = tbl_Login.objects.filter(uname=uname, pswd=pswd, utype='admin')

        if len(ul) == 1:
            request.session['user_id'] = ul[0].id
            request.session['user_name'] = ul[0].uname
            return render(request,'./myapp/admin_home.html')
        else:
            msg = '<section style="background-color:  #f6916d  "><br><h6 style="color: #362c4f "><b>Invalid Credentials !!</b></h6><br></section>'
            context ={'msg':msg }
            return render(request, './myapp/admin_login.html',context)
    else:
        return render(request, './myapp/admin_login.html')


def admin_home(request):
    try:
        uname = request.session['user_name']
    except:
        return render(request,'./myapp/admin_login.html')
    return render(request,'./myapp/admin_home.html')


def admin_logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
    except:
        return index(request)
    else:
        return index(request)  # return render(request,'./myapp/index.html')


def admin_changepassword(request):
    if request.method == 'POST':
        oldpswd = request.POST.get('oldpswd')
        newpswd = request.POST.get('newpswd')
        cnfpswd = request.POST.get('cnfpswd')
        uname = request.session['user_name']
        try:
            ul = tbl_Login.objects.get(uname=uname, pswd=oldpswd, utype='admin')
            if ul is not None:
                if newpswd == cnfpswd:
                    ul.pswd = newpswd
                    ul.save()
                    context = {'msg': '<h6 style="color:green">Password Changed Successfully</h6>'}
                    return render(request, './myapp/admin_changepassword.html', context)
                else:
                    context = {'msg': '<h6 style="color:red">New Password Doesnt Match ! Confirm Your Password </h6>'}
                    return render(request, './myapp/admin_changepassword.html', context)
        except tbl_Login.DoesNotExist:
            context = {'msg': '<h6 style="color:red">Incorrect Password !! </h6>'}
            return render(request, './myapp/admin_changepassword.html', context)
    else:
        return render(request, './myapp/admin_changepassword.html',)


def admin_view_castingteam_new(request):
    cst_login_list = tbl_Login.objects.filter(status='0',utype='castingteam')
    castingteam_list = tbl_CastingTeam.objects.all()
    context = {'cst_login_list':cst_login_list, 'castingteam_list':castingteam_list}
    if len(cst_login_list)==0:
        context={'empty_msg':'<h4 style="color:red">List is Empty ! </h4>'}
    return render(request,'./myapp/admin_view_castingteam_new.html',context)


def admin_view_castingteam_accepted(request):
    cst_login_list = tbl_Login.objects.filter(status='1',utype='castingteam')
    castingteam_list = tbl_CastingTeam.objects.all()
    context = {'cst_login_list':cst_login_list, 'castingteam_list':castingteam_list}
    if len(cst_login_list)==0:
        context={'empty_msg':'<h4 style="color:red">List is Empty ! </h4>'}
    return render(request,'./myapp/admin_view_castingteam_accepted.html',context)


def admin_view_castingteam_rejected(request):
    cst_login_list = tbl_Login.objects.filter(status='-1',utype='castingteam')
    castingteam_list = tbl_CastingTeam.objects.all()
    context = {'cst_login_list':cst_login_list, 'castingteam_list':castingteam_list}
    if len(cst_login_list)==0:
        context={'empty_msg':'<h4 style="color:red">List is Empty ! </h4>'}
    return render(request,'./myapp/admin_view_castingteam_rejected.html',context)


def admin_approvals_castingteam(request):
    login_id = int(request.GET.get('login_id'))
    status = request.GET.get('status')
    page = request.GET.get('page')

    login_list = tbl_Login.objects.get(id=int(login_id))
    login_list.status = status
    login_list.save()
    if page == '1':
        return admin_view_castingteam_new(request)
    elif page == '2':
        return admin_view_castingteam_accepted(request)
    else:
        return admin_view_castingteam_rejected(request)



from .models import tbl_ProductionMaster

def admin_add_prod_master(request):
    if request.method == "POST":
        prod_categ = request.POST.get('prod_categ')
        emotion_capture = request.POST.get('emotion_capture')
        prod_master_list = tbl_ProductionMaster(prod_categ=prod_categ,emotion_capture=emotion_capture)
        prod_master_list.save()
        context={'msg':'<i><h5 style="color:green">Production Type Added Successfully</h5></i> <a href="admin_view_prod_master">Tap To View</a>'}
        return render(request,'./myapp/admin_add_prod_master.html',context)
    else:
        return render(request,'./myapp/admin_add_prod_master.html')


def admin_view_prod_master(request):
    prod_master_list = tbl_ProductionMaster.objects.all()
    if len(prod_master_list) == 0:
        empty_context={'empty_msg': '<h5 style="color:red">List is Empty !</h5>'}
        return render(request, './myapp/admin_view_prod_master.html', empty_context)
    try:
        msg=request.session['msg']
        context = {'prod_master_list': prod_master_list,'msg':msg}
        return render(request, './myapp/admin_view_prod_master.html', context)
    except:
        context = {'prod_master_list': prod_master_list}
        return render(request,'./myapp/admin_view_prod_master.html',context)


def admin_delete_prod_master(request):
    try:
        id = request.GET.get('id')
        prod_master_to_del = tbl_ProductionMaster.objects.get(id=int(id))
        prod_master_to_del.delete()
        prod_master_list = tbl_ProductionMaster.objects.all()
        if len(prod_master_list)==0:
            empty_context = {'empty_msg': '<h5 style="color:red">List is Empty !</h5>'}
            return render(request, './myapp/admin_view_prod_master.html', empty_context)
        context = {'prod_master_list': prod_master_list}
        return render(request,'./myapp/admin_view_prod_master.html',context)
    except tbl_ProductionMaster.DoesNotExist:
        prod_master_list = tbl_ProductionMaster.objects.all()
        if len(prod_master_list)==0:
            empty_context = {'empty_msg': '<h5 style="color:red">List is Empty !</h5>'}
            return render(request, './myapp/admin_view_prod_master.html', empty_context)
        else:
            context = {'prod_master_list': prod_master_list}
            return render(request, './myapp/admin_view_prod_master.html', context)


def admin_edit_prod_master(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        prod_categ = request.POST.get('prod_categ')
        emotion_capture = request.POST.get('emotion_capture')
        pd = tbl_ProductionMaster.objects.get(id=int(id))
        pd.prod_categ = prod_categ
        pd.emotion_capture = emotion_capture
        pd.save()
        request.session['msg']= '<div style="color:green">One Record Updated Successfully</div>'
        return admin_view_prod_master(request)
    else:
        try:
            id= request.GET.get('id')
            prod_master_list = tbl_ProductionMaster.objects.get(id=int(id))
            context = {'prod_master_list': prod_master_list}
            return render(request,'./myapp/admin_edit_prod_master.html',context)
        except tbl_ProductionMaster.DoesNotExist:
            prod_master_list - tbl_ProductionMaster.objects.all()
            context = {'prod_master_list': prod_master_list}
            return render(request,'./myapp/admin_view_prod_master.html',context)



####################  Casting Team  #############

from .models import tbl_CastingTeam
from .gmail_test import send_mail

def castingteam_reg(request):
    if request.method == 'POST':
        company= request.POST.get('company')
        producer = request.POST.get('producer')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        pin = request.POST.get('pin')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        uname = request.POST.get('uname')
        pswd = request.POST.get('pswd')
        cnfpswd = request.POST.get('cnfpswd')
        status = 0

        ul = tbl_Login(uname=uname, pswd=pswd, utype='castingteam', status=status)
        ul.save()
        user_login_id = tbl_Login.objects.all().aggregate(Max('id'))['id__max']

        castingteam_list = tbl_CastingTeam(castingteam_login_id=user_login_id, castingteam_company=company, castingteam_producer=producer , castingteam_address=address,
                              castingteam_city=city, castingteam_state=state,
                              castingteam_country=country, castingteam_pincode=pin, castingteam_contact=contact, castingteam_email=email)
        castingteam_list.save()

        context = {
            'msg': '<section style="background-color: #d3c4c1"><br><h6 style="color: #362c4f "><b>Thank You For Being a <span style="color:green">Cast <i>\'N\'</i> Play </span>Crew Member</b></h6><a href="#" style="text-decoration:none;color: #4116a6 ">Click To Login</a><br><br></section>'}
        #send_mail("Cast 'N' Play-Sign Up", "Welcome User , Thank you for registering with Cast 'N' Play", email)
        return render(request, './myapp/castingteam_reg.html', context)
    else:
        return render(request, './myapp/castingteam_reg.html')


def castingteam_login(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        pswd = request.POST.get('pswd')
        #query to select a record based on a condition
        ul = tbl_Login.objects.filter(uname=uname, pswd=pswd, utype='castingteam',status=1)
        #st= ul[0].status

        if len(ul) == 1:
            request.session['user_id'] = ul[0].id
            request.session['user_name'] = ul[0].uname
            return render(request,'./myapp/castingteam_home.html')
        else:
            msg = '<section style="background-color:  #f6916d  "><br><h6 style="color: #362c4f "><b>Invalid Credentials or Need Admin Approval!!</b></h6><br></section>'
            context ={'msg':msg }
            return render(request, './myapp/castingteam_login.html',context)
    else:
        return render(request, './myapp/castingteam_login.html')


def castingteam_home(request):
    try:
        context = {'uname':request.session['user_name']}
    except:
        return render(request,'./myapp/castingteam_login.html')
    return render(request,'./myapp/castingteam_home.html',context)



def castingteam_update_profile(request):
    if request.method == 'POST':
        castingteam_login_id = request.session['user_id']
        up = tbl_CastingTeam.objects.get(castingteam_login_id=int(castingteam_login_id))
        lg = tbl_Login.objects.get(id=int(castingteam_login_id))

        castingteam_company = request.POST.get('company')
        castingteam_producer = request.POST.get('producer')
        castingteam_address = request.POST.get('address')
        castingteam_city = request.POST.get('city')
        castingteam_state = request.POST.get('state')
        castingteam_country = request.POST.get('country')
        castingteam_pincode = request.POST.get('pin')
        castingteam_contact = request.POST.get('contact')
        castingteam_email = request.POST.get('email')
        uname = request.POST.get('uname')

        up.castingteam_company = castingteam_company
        up.castingteam_producer = castingteam_producer
        up.castingteam_address = castingteam_address
        up.castingteam_city = castingteam_city
        up.castingteam_state = castingteam_state
        up.castingteam_country = castingteam_country
        up.castingteam_pincode = castingteam_pincode
        up.castingteam_contact = castingteam_contact
        up.castingteam_email = castingteam_email
        lg.uname = uname

        up.save()
        lg.save()

        context = {'msg': '<h5 style="color: #64ca40 ">Company Details Updated</h5>','up':up,'lg':lg}
        return render(request, 'myapp/castingteam_update_profile.html',context)

    else:
        castingteam_login_id = request.session['user_id']
        up = tbl_CastingTeam.objects.get(castingteam_login_id=int(castingteam_login_id))
        lg = tbl_Login.objects.get(id=int(castingteam_login_id))
        context={'up':up,'lg':lg}
        return render(request, 'myapp/castingteam_update_profile.html',context)



def castingteam_changepassword(request):
    if request.method == 'POST':
        oldpswd = request.POST.get('oldpswd')
        newpswd = request.POST.get('newpswd')
        cnfpswd = request.POST.get('cnfpswd')
        uname = request.session['user_name']
        try:
            ul = tbl_Login.objects.get(uname=uname, pswd=oldpswd, utype='castingteam')
            if ul is not None:
                if newpswd == cnfpswd:
                    ul.pswd = newpswd
                    ul.save()
                    context = {'msg': '<h6 style="color:green">Password Changed Successfully</h6>'}
                    return render(request, './myapp/castingteam_changepassword.html', context)
                else:
                    context = {'msg': '<h6 style="color:red">New Password Doesnt Match ! Confirm Your Password </h6>'}
                    return render(request, './myapp/castingteam_changepassword.html', context)
        except tbl_Login.DoesNotExist:
            context = {'msg': '<h6 style="color:red">Incorrect Password !! </h6>'}
            return render(request, './myapp/castingteam_changepassword.html', context)
    else:
        return render(request, './myapp/castingteam_changepassword.html',)


import string
import random
def get_password():
    S = 10
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))
    print("The randomly generated string is : " + str(ran))  # print the random data
    return ran


def castingteam_forgot_password(request):
    if request.method == "POST":
        funame = request.POST.get('uname')
        newpswd=get_password()
        reg_list=tbl_CastingTeam.objects.filter(castingteam_email=funame)
        if len(reg_list) == 0:
            context={'msg': '<section style="background-color:#b1b4bf   "> <br> <h5 style="color:red">Invalid Mail Id <br> <br></section>'}
            return render(request, './myapp/castingteam_forgot_password.html', context)
        else:
            login_list = tbl_Login.objects.get(id=reg_list[0].castingteam_login_id)
            login_list.pswd = newpswd
            login_list.save()
            send_mail("Cast 'N' Play-Forgot Password", "Hello Casting Team,\n\n\nYour New Password : -  "+newpswd+" \n Please Login with your new credentials.  \n \nWith Regards,\n Cast 'n' Play", funame)
            context={'msg':'<section style="background-color:#b1b4bf    "><br>New Password Send to '+funame+'<br><br></section>'}
            return render(request,'./myapp/castingteam_forgot_password.html',context)
    else:
        return render(request, './myapp/castingteam_forgot_password.html')


def castingteam_logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
    except:
        return index(request)
    else:
        return index(request)



from .models import tbl_CastingTeamProductions

def castingteam_prods_add(request):
    if request.method == 'POST':
        prod_categ_id = request.POST.get('prod_categ_id')
        try:
            castingteam_id = request.session['user_id']
        except:
            return render(request, './myapp/castingteam_login.html')
        if prod_categ_id == "none":
            prod_list = tbl_ProductionMaster.objects.all()
            context = {'msg': '<h6 style="color:red">Select a Production to Add</h4>',
                       'prod_list': prod_list}
            return render(request, './myapp/castingteam_prods_add.html', context)
        else:
            my_prod_list = tbl_CastingTeamProductions(castingteam_id=castingteam_id, castingteam_prod_categid=prod_categ_id)
            my_prod_list.save()
            prod_list = tbl_ProductionMaster.objects.all()
            context = {'msg': '<h6 style="color:green">Successfully Registered with new Production Type</h4>', 'prod_list': prod_list}
            return render(request,'./myapp/castingteam_prods_add.html',context)
    else:
        prod_list = tbl_ProductionMaster.objects.all()
        context = {'prod_list': prod_list}
        return render(request,'./myapp/castingteam_prods_add.html',context)



def castingteam_prods_view(request):
    try:
        castingteam_id= request.session['user_id']
    except:
        return render(request, './myapp/castingteam_login.html')
    castingteam_prods_list = tbl_CastingTeamProductions.objects.filter(castingteam_id=castingteam_id)
    prod_master_list = tbl_ProductionMaster.objects.all()
    if len(castingteam_prods_list) == 0:
        context={'empty_msg': '<h5 style="color:red">List is Empty !<br><br><span style="color:grey">You are not Registered with any Production Type</h5>','castingteam_prods_list': castingteam_prods_list,'prod_master_list':prod_master_list}
        return render(request, './myapp/castingteam_prods_view.html', context)
    else:
        context={'castingteam_prods_list': castingteam_prods_list,'prod_master_list':prod_master_list}
        return render(request, './myapp/castingteam_prods_view.html', context)


def castingteam_prods_delete(request):
    try:
        id = request.GET.get('id')
        try:
            prod_to_del = tbl_CastingTeamProductions.objects.get(id=int(id))
            prod_to_del.delete()
        except:
            castingteam_prods_list = tbl_CastingTeamProductions.objects.filter(castingteam_id=castingteam_id)
            prod_master_list = tbl_ProductionMaster.objects.all()
            if len(castingteam_prods_list) == 0:
                context = {'empty_msg': '<h5 style="color:red">List is Empty !<br><br><span style="color:grey">You are not Registered with any Production Type</h5>'}
                return render(request, './myapp/castingteam_prods_view.html', context)
            else:
                context = {'prod_master_list': prod_master_list, 'castingteam_prods_list': castingteam_prods_list}
                return render(request, './myapp/castingteam_prods_view.html', context)
        try:
            castingteam_id = request.session['user_id']
        except:
            return render(request, './myapp/castingteam_login.html')

        castingteam_prods_list = tbl_CastingTeamProductions.objects.filter(castingteam_id=castingteam_id)
        prod_master_list = tbl_ProductionMaster.objects.all()
        if len(castingteam_prods_list) == 0:
            context = {'empty_msg': '<h5 style="color:red">List is Empty !<br><br><span style="color:grey">You are not Registered with any Production Type</h5>'}
            return render(request, './myapp/castingteam_prods_view.html', context)
        else:
            context = {'prod_master_list': prod_master_list , 'castingteam_prods_list' : castingteam_prods_list}
            return render(request,'./myapp/castingteam_prods_view.html',context)

    except tbl_ProductionMaster.DoesNotExist:
        try:
            castingteam_id = request.session['user_id']
        except:
            return render(request, './myapp/castingteam_login.html')

        prod_master_list = tbl_ProductionMaster.objects.all()
        castingteam_prods_list = tbl_CastingTeamProductions.objects.filter(castingteam_id=castingteam_id)

        if len(castingteam_prods_list)==0:
            context = {'empty_msg': '<h5 style="color:red">List is Empty !<br><br><span style="color:grey">You are not Registered with any Production Type</h5>'}
            return render(request, './myapp/castingteam_prods_view.html', context)
        else:
            context = {'prod_master_list': prod_master_list, 'castingteam_prods_list' : castingteam_prods_list}
            return render(request, './myapp/castingteam_prods_view.html', context)


from .models import tbl_Artist

def castingteam_view_artist(request):
    login_list = tbl_Login.objects.filter(utype='artist', status=1)
    arl_list = tbl_Artist.objects.all()

    """for i in login_list:
        arl_list = tbl_Artist.objects.filter(art_login_id=login_list[i].id)"""
    context={'arl_list': arl_list, 'login_list' : login_list}
    return render(request,'./myapp/castingteam_view_artist.html',context)


from .models import tbl_CastingCall
from datetime import datetime

def casting_call_add(request):
    if request.method == 'POST':
        posted_date = datetime.today().strftime('%Y-%m-%d')
        posted_time = datetime.today().strftime('%H:%M:%S')
        character = request.POST.get('character')
        role_desc = request.POST.get('role_desc')
        gender = request.POST.get('gender')
        age_from = int(request.POST.get('age_from'))
        age_to = int(request.POST.get('age_to'))
        castingteam_prod_categid = request.POST.get('castingteam_prod_categid')
        call_expiry = request.POST.get('call_expiry')
        job_duration = request.POST.get('job_duration')

        try:
            castingteam_id = request.session['user_id']
        except:
            return render(request, './myapp/castingteam_login.html')

        if castingteam_prod_categid == "none": ## none
            prod_master_list = tbl_ProductionMaster.objects.all()
            castingteam_prods_list = tbl_CastingTeamProductions.objects.filter(castingteam_id=castingteam_id)
            context = {'castingteam_prods_list': castingteam_prods_list, 'prod_master_list': prod_master_list,'msg':'<h6 style="color:red">Select a Production Type for Casting Call !!</h6>'}
            return render(request,'./myapp/casting_call_add.html',context)
        else:
            call_list = tbl_CastingCall(posted_date=posted_date,posted_time=posted_time,
                                 character=character,role_desc=role_desc,
                                 gender=gender,age_from=age_from,
                                 age_to=age_to,castingteam_prod_categid=castingteam_prod_categid,
                                 call_expiry=call_expiry,job_duration=job_duration,
                                 castingteam_id=castingteam_id)
            call_list.save()
            max_call_id = tbl_CastingCall.objects.all().aggregate(Max('id'))['id__max']

            plot_check_list= tbl_ProductionMaster.objects.filter(id=int(castingteam_prod_categid))
            if plot_check_list[0].emotion_capture == 1:
                
                request.session['max_call_id'] = max_call_id
                return render(request, './myapp/castingteam_add_plot.html') # pass var b/w views
            else:
                prod_master_list = tbl_ProductionMaster.objects.all()
                castingteam_prods_list = tbl_CastingTeamProductions.objects.filter(castingteam_id=castingteam_id)
                context = {'castingteam_prods_list':castingteam_prods_list, 'prod_master_list':prod_master_list,'msg':'<h6 style="color:blue">Casting Call Addded Successfully</h6>'}
                return render(request, './myapp/casting_call_add.html',context)
    else:
        try:
            castingteam_id = request.session['user_id']
        except:
            return render(request, './myapp/castingteam_login.html')
        prod_master_list = tbl_ProductionMaster.objects.all()
        castingteam_prods_list = tbl_CastingTeamProductions.objects.filter(castingteam_id=castingteam_id)
        context = {'castingteam_prods_list':castingteam_prods_list, 'prod_master_list':prod_master_list}
        return render(request, './myapp/casting_call_add.html',context)


def casting_call_view(request):
    try:
        castingteam_id = request.session['user_id']
    except:
        return render(request,'./myapp/castingteam_login.html')

    call_list = tbl_CastingCall.objects.filter(castingteam_id=int(castingteam_id))
    prod_list = tbl_ProductionMaster.objects.all()
    plot_list = tbl_Plot.objects.all()
    if len(plot_list) == 0:
        plot_list = [{'id':0}]
    if len(call_list) == 0:
        context={'empty_msg': '<h5 style="color:red">List is Empty !<br><br><span style="color:grey">You haven\'t Added any Casting Calls</h5>'}
        return render(request, './myapp/casting_call_view.html', context)
    else:
        context = {'prod_list': prod_list, 'call_list': call_list, 'plot_list':plot_list}
        return render(request, './myapp/casting_call_view.html', context)


def casting_call_delete(request):
    id = request.GET.get('id')

    call_list = tbl_CastingCall.objects.get(id=int(id))
    plot_list = tbl_Plot.objects.filter(plot_castingcall_id=int(id))
    if len(plot_list) == 0:
        call_list.delete()
    else:
        call_list.delete()
        plot_list.delete()
    try:
        castingteam_id = request.session['user_id']
    except:
        return render(request,'./myapp/castingteam_login.html')

    call_list = tbl_CastingCall.objects.filter(castingteam_id=int(castingteam_id))
    prod_list = tbl_ProductionMaster.objects.all()
    plot_list = tbl_Plot.objects.all()

    if len(call_list) == 0:
        context={'empty_msg': '<h5 style="color:red">List is Empty !<br><br><span style="color:grey">You haven\'t Added any Casting Calls</h5>'}
        return render(request, './myapp/casting_call_view.html', context)
    else:
        context = {'prod_list': prod_list, 'call_list': call_list, 'plot_list':plot_list}
        return render(request, './myapp/casting_call_view.html', context)


def casting_call_edit(request):
    if request.method == 'POST':
        character = request.POST.get('character')
        role_desc = request.POST.get('role_desc')
        gender = request.POST.get('gender')
        age_from = int(request.POST.get('age_from'))
        age_to = int(request.POST.get('age_to'))
        castingteam_prod_categid = request.POST.get('castingteam_prod_categid')
        call_expiry = request.POST.get('call_expiry')
        job_duration = request.POST.get('job_duration')
        posted_date = datetime.today().strftime('%Y-%m-%d')
        posted_time = datetime.today().strftime('%H:%M:%S')
        id = request.POST.get('id')
        try:
            castingteam_id = request.session['user_id']
        except:
            return render(request, './myapp/castingteam_login.html')
        call = tbl_CastingCall.objects.get(id=int(id))
        call.character = character
        call.role_desc = role_desc
        call.gender = gender
        call.age_from = age_from
        call.age_to = age_to
        call.castingteam_prod_categid = castingteam_prod_categid
        call.call_expiry = call_expiry
        call.job_duration = job_duration
        call.posted_date = posted_date
        call.posted_time = posted_time
        call.save()
        print('<script>alert("One Record Updated Successfull")</script>')
        return casting_call_view(request)
    else:
        id=request.GET.get('id')
        call = tbl_CastingCall.objects.get(id=int(id))
        try:
            castingteam_id = request.session['user_id']
        except:
            return render(request, './myapp/castingteam_login.html')
        prod_master_list = tbl_ProductionMaster.objects.all()
        castingteam_prods_list = tbl_CastingTeamProductions.objects.filter(castingteam_id=castingteam_id)
        context = {'castingteam_prods_list':castingteam_prods_list, 'prod_master_list':prod_master_list,'call':call}
        return render(request, './myapp/casting_call_edit.html',context)


from .models import tbl_Plot

def castingteam_add_plot(request):
    if request.method == 'POST':
        plot_castingcall_id = request.session['max_call_id']
        plot_emotion = request.POST.get('plot_emotion')
        plot_desc = request.POST.get('plot_desc')
        plot_video_duration = request.POST.get('plot_video_duration')
        plot_list = tbl_Plot(plot_castingcall_id=plot_castingcall_id,plot_emotion=plot_emotion, plot_desc=plot_desc,plot_video_duration = plot_video_duration )
        plot_list.save()
        try:
            castingteam_id = request.session['user_id']
        except:
            return render(request, './myapp/castingteam_login.html')

        prod_master_list = tbl_ProductionMaster.objects.all()
        castingteam_prods_list = tbl_CastingTeamProductions.objects.filter(castingteam_id=castingteam_id)
        context = {'castingteam_prods_list':castingteam_prods_list, 'prod_master_list':prod_master_list,'msg':'<h6 style="color:blue">Casting Call and Plot Added Successfully</h6>'}
        return render(request, './myapp/casting_call_add.html',context)
    else:
        return render(request,'./myapp/castingteam_add_plot.html', call_id_dict)


def castingteam_view_plot(request):
    try:
        plot_castingcall_id = request.GET.get('plot_castingcall_id')
    except:
        plot_castingcall_id = request.session['plot_castingcall_id']
    #castingteam_id = request.session['user_id']

    pm_l = tbl_Plot.objects.filter(plot_castingcall_id=int(plot_castingcall_id))

    context = {'plot_castingcall_id':plot_castingcall_id,'plot_list': pm_l, 'msg': ''}
    return render(request, './myapp/castingteam_view_plot.html', context)


def castingteam_edit_plot(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        plot_emotion = request.POST.get('plot_emotion')
        plot_desc = request.POST.get('plot_desc')
        plot_video_duration = request.POST.get('plot_video_duration')

        plot_list = tbl_Plot.objects.get(id=int(id))
        plot_list.plot_emotion = plot_emotion
        plot_list.plot_desc = plot_desc
        plot_list.plot_video_duration = plot_video_duration
        plot_list.save()

        plot_castingcall_id = plot_list.plot_castingcall_id
        request.session['plot_castingcall_id'] = plot_castingcall_id
        print("<script>alert('Plot Updated Successfully')</script>")
        return castingteam_view_plot(request)
    else:
        id = request.GET.get('id')
        plot_list = tbl_Plot.objects.get(id=int(id))
        context={'plot_list':plot_list}
        return render(request,'./myapp/castingteam_edit_plot.html',context)



from .models import tbl_Artist,tbl_CastingApplication,tbl_VideoUpload

def casting_application_view(request):
    castingcall_id = int(request.GET.get('castingcall_id'))
    #castingteam_id = request.session['user_id']

    art_list = tbl_Artist.objects.all()
    video_list = tbl_VideoUpload.objects.all()
    appl_list = tbl_CastingApplication.objects.filter(appl_castingcall_id=int(castingcall_id))
    casting_call = tbl_CastingCall.objects.get(id=castingcall_id)
    char = casting_call.character

    if len(video_list) == 0:
        video_list =[{'id':0}]

    if len(appl_list) == 0:
        context={'empty_msg': '<h5 style="color:red">List is Empty !<br><br></h5>'}
        return render(request, 'myapp/casting_application_view.html', context)
    else:
        context = {'art_list':art_list,'char':char,'appl_list': appl_list, 'video_list':video_list}
        return render(request, 'myapp/casting_application_view.html', context)


def castingteam_accept_reject_appl(request):
    appl_id = request.GET.get('appl_id')
    status = request.GET.get('status')
    try:
        appl_list = tbl_CastingApplication.objects.get(id=appl_id)
        status_name = appl_list.application_result
        if status =='1':
            status_name = 'Accepted'
        else:
            status_name = 'Rejected'
        appl_list.application_result = status_name
        appl_list.save()
    except:
        return casting_call_view(request)
    return casting_call_view(request)


######################    Artist  #############

from .models import tbl_Artist

from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.db.models import Max    # Foreign Key Usage

def artist_reg(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        uname = request.POST.get('uname')
        pswd = request.POST.get('pswd')
        cnfpswd = request.POST.get('cnfpswd')
        dob = request.POST.get('dob')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        pin = request.POST.get('pin')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        work_title = request.POST.get('work_title')
        #headphoto = request.FILES['headphoto']
        art_headphoto_file = request.FILES['headphoto']

        compensation = request.POST.get('compensation')
        bio = request.POST.get('bio')
        status='1'

        fs = FileSystemStorage()
        file_path = fs.save(art_headphoto_file.name, art_headphoto_file)

        ul = tbl_Login(uname=uname, pswd=pswd, utype='artist', status=status)
        ul.save()
        user_login_id = tbl_Login.objects.all().aggregate(Max('id'))['id__max']

        art_list = tbl_Artist(art_login_id=user_login_id,art_fname=fname,art_lname=lname,art_DOB=dob,art_age=age,
        art_gender=gender,art_address=address,art_city=city,art_state=state,
        art_country=country,art_pin=pin,art_contact=contact,art_email=email,
        art_work_title=work_title,art_headphoto=file_path,art_bio=bio,art_compensation=compensation)
        art_list.save()

        context={'msg':'<section style="background-color: #d3c4c1"><br><h6 style="color: #362c4f "><b>Thank You For Being a <span style="color:green">Cast <i>\'N\'</i> Play </span>Crew Member</b></h6><a href="#" style="text-decoration:none;color: #4116a6 ">Click To Login</a><br><br></section>'}
        send_mail("Cast 'N' Play-Sign Up", "Welcome User , Thank you for registering with Cast 'N' Play", email)
        return render(request,'./myapp/artist_reg.html',context)
    else:
        return render(request,'./myapp/artist_reg.html')


def artist_login(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        pswd = request.POST.get('pswd')

        ul = tbl_Login.objects.filter(uname=uname, pswd=pswd,utype='artist',status=1)
        if len(ul) == 1:
            request.session['user_id'] = ul[0].id
            request.session['user_name'] = ul[0].uname
            context = {'uname': request.session['user_name']}
            return render(request, './myapp/artist_home.html',context)
        else:
            msg = '<section style="background-color:  #f6916d  "><br><h6 style="color: #362c4f "><b>Invalid Credentials !!</b></h6><br></section>'
            context = {'msg': msg}
            return render(request, './myapp/artist_login.html',context)
    else:
        return render(request, './myapp/artist_login.html')


def artist_home(request):
    try:
        context = {'uname':request.session['user_name']}
        return render(request,'./myapp/artist_home.html',context)
    except:
        return render(request,'./myapp/artist_login.html')


def artist_logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
    except:
        return index(request)
    else:
        return index(request)


def artist_details_update(request):
    if request.method == 'POST':
        art_login_id = request.session['user_id']
        up = tbl_Artist.objects.get(art_login_id=int(art_login_id))

        art_fname = request.POST.get('fname')
        art_lname = request.POST.get('lname')
        art_DOB = request.POST.get('dob')
        art_age = request.POST.get('age')
        art_gender = request.POST.get('gender')
        art_address = request.POST.get('address')
        art_city = request.POST.get('city')
        art_state = request.POST.get('state')
        art_country = request.POST.get('country')
        art_pincode = request.POST.get('pin')
        art_contact = request.POST.get('contact')
        art_email = request.POST.get('email')
        art_work_title = request.POST.get('work_title')
        art_compensation = request.POST.get('compensation')
        art_bio = request.POST.get('bio')

        up.art_fname = art_fname
        up.art_lname = art_lname
        up.art_DOB = art_DOB
        up.art_age = art_age
        up.art_gender = art_gender
        up.art_address = art_address
        up.art_city = art_city
        up.art_state = art_state
        up.art_country = art_country
        up.art_pincode = art_pincode
        up.art_contact = art_contact
        up.art_email = art_email
        up.art_work_title = art_work_title
        up.art_compensation = art_compensation
        up.art_bio = art_bio

        up.save()

        context = {'msg': '<section style="background-color: #a4ef84 "><br><h5 style="color: green ">Artist Details Updated</h5><br></section>','up':up}
        return render(request, 'myapp/artist_details_update.html',context)

    else:
        art_login_id = request.session['user_id']
        up = tbl_Artist.objects.get(art_login_id=int(art_login_id))
        context={'up':up}
        return render(request, 'myapp/artist_details_update.html',context)


def artist_photo_update(request):
    if request.method == 'POST':
        art_login_id = request.session['user_id']
        up = tbl_Artist.objects.get(art_login_id=int(art_login_id))

        u_file = request.FILES['photo']
        fs = FileSystemStorage()
        art_headphoto = fs.save(u_file.name, u_file)
        up.art_headphoto = art_headphoto
        up.save()
        #print(user_id)
        context = {'msg': '<h5 style="color:#fff">Profile Picture Changed Successfully</h5>','pic_path': up.art_headphoto}
        return render(request, 'myapp/artist_photo_update.html',context)
    else:
        art_login_id = request.session['user_id']
        up = tbl_Artist.objects.get(art_login_id=int(art_login_id))
        context = {'pic_path': up.art_headphoto}
        return render(request, 'myapp/artist_photo_update.html',context)


def artist_changepassword(request):
    if request.method == 'POST':
        oldpswd = request.POST.get('oldpswd')
        newpswd = request.POST.get('newpswd')
        cnfpswd = request.POST.get('cnfpswd')
        uname = request.session['user_name']
        try:
            ul = tbl_Login.objects.get(uname=uname, pswd=oldpswd, utype='artist')
            if ul is not None:
                if newpswd == cnfpswd:
                    ul.pswd = newpswd
                    ul.save()
                    context = {'msg': '<h6 style="color:green">Password Changed Successfully</h6>'}
                    return render(request, './myapp/artist_changepassword.html', context)
                else:
                    context = {'msg': '<h6 style="color:red">New Password Doesnt Match ! Confirm Your Password </h6>'}
                    return render(request, './myapp/artist_changepassword.html', context)
        except tbl_Login.DoesNotExist:
            context = {'msg': '<h6 style="color:red">Incorrect Password !! </h6>'}
            return render(request, './myapp/artist_changepassword.html', context)
    else:
        return render(request, './myapp/artist_changepassword.html',)


def artist_forgot_password(request):
    if request.method == "POST":
        funame = request.POST.get('uname')
        newpswd=get_password()
        reg_list=tbl_Artist.objects.filter(art_email=funame)
        if len(reg_list) == 0:
            context={'msg': '<section style="background-color:#b1b4bf   "> <br> <h5 style="color:red">Invalid Mail Id <br> <br></section>'}
            return render(request, './myapp/artist_forgot_password.html', context)
        else:
            login_list = tbl_Login.objects.get(id=reg_list[0].art_login_id)
            login_list.pswd = newpswd
            login_list.save()
            send_mail("Cast 'N' Play-Forgot Password", "Hello Artist,\n\n\nYour New Password : - "+newpswd+" \n Please Login with your new credentials.  \n \nWith Regards,\n Cast 'n' Play", funame)
            context={'msg':'<section style="background-color:#b1b4bf    "><br>New Password Send to '+funame+'<br><br></section>'}
            return render(request,'./myapp/artist_forgot_password.html',context)
    else:
        return render(request, './myapp/artist_forgot_password.html')



def artist_casting_call_view(request):
    call_list = tbl_CastingCall.objects.all()
    prod_list = tbl_ProductionMaster.objects.all()
    castingteam_list = tbl_CastingTeam.objects.all()
    plot_list = tbl_Plot.objects.all()
    appl_list = tbl_CastingApplication.objects.all()
    #if len(plot_list)==0:
        #plot_list = [{'id':0}]
    context = {'prod_list': prod_list,'castingteam_list': castingteam_list, 'call_list': call_list,'plot_list':plot_list,'appl_list':appl_list}
    return render(request, 'myapp/artist_casting_call_view.html', context)


def artist_view_castingteam(request):
    castingteam_list = tbl_CastingTeam.objects.all()
    context = {'castingteam_list':castingteam_list}
    return render(request,'./myapp/artist_view_castingteam.html',context)

def artist_casting_search(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        ct_l = tbl_CastingTeam.objects.filter(castingteam_company__contains=query)

        pm_l = []
        for ct in ct_l:
            cc_l = tbl_CastingCall.objects.filter(castingteam_id=ct.castingteam_login_id)
            for cc in cc_l:
                pm_l.append(cc)

        scm_l = tbl_ProductionMaster.objects.all()
        ct_l = tbl_CastingTeam.objects.all()
        plot_list = tbl_Plot.objects.all()
        appl_list = tbl_CastingApplication.objects.all()
        context = {'prod_list': scm_l,'castingteam_list': ct_l, 'call_list': pm_l,'plot_list':plot_list,'appl_list':appl_list}
        return render(request, 'myapp/artist_casting_call_view.html', context)
    else:
        return render(request, 'myapp/artist_casting_search.html')


def artist_view_plot(request):
    plot_castingcall_id = int(request.GET.get('plot_castingcall_id'))
    #castingteam_id = request.session['user_id']
    pm_l = tbl_Plot.objects.filter(plot_castingcall_id=int(plot_castingcall_id))
    context = {'plot_castingcall_id': plot_castingcall_id, 'plot_list': pm_l}
    return render(request, 'myapp/artist_view_plot.html', context)



import shutil
import os
from . import mp4
from . import extract
from . import Testing
from plotly.offline import plot
from plotly.graph_objs import Bar
from project.settings import BASE_DIR
from datetime import datetime

from .models import tbl_VideoUpload

def artist_casting_application_add(request):
    if request.method == 'POST':
        u_file = request.FILES['video_file']
        fs = FileSystemStorage()
        video_file = fs.save(u_file.name, u_file)
        appl_castingcall_id = int(request.POST.get('appl_castingcall_id'))
        appl_art_id = request.session['user_id']
        video_yes_no = 'Yes'
        application_status = 1
        application_result = 'Unchecked'
        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')
        result = 'result'


        ######################################################
        extracted_file_path = os.path.join(BASE_DIR, 'data\\extracted')
        face_file_path = os.path.join(BASE_DIR, f'myapp\\static\\myapp\\media\\face')

        bat_file_path = os.path.join(BASE_DIR, 'data\\r.bat')

        shutil.rmtree(extracted_file_path, ignore_errors=True)
        os.mkdir(extracted_file_path);
        shutil.rmtree(face_file_path, ignore_errors=True)
        os.mkdir(face_file_path);

        video_file_path = os.path.join(BASE_DIR, f'myapp\\static\\myapp\\media\\{video_file}')
        mp4.convert(bat_file_path, video_file_path, extracted_file_path)

        listOfFiles = list()
        for (dirpath, dirnames, filenames) in os.walk(extracted_file_path):
            listOfFiles += [os.path.join(dirpath, file) for file in filenames]
        pos = 0
        for elem in listOfFiles:
            print(elem)
            obj = extract.Extract()
            obj.method_extract(elem, face_file_path, pos)
            pos = pos + 1

        listOfFaces = list()
        for (dirpath, dirnames, filenames) in os.walk(face_file_path):
            listOfFaces += [os.path.join(dirpath, file) for file in filenames]

        str_template = ''
        sentiment_count = dict()
        action_dict = {0: 'anger', 1: 'disgust', 2: 'fear',  3: 'happy', 4: 'sad'}
        sentiment_count['anger'] = 0
        sentiment_count['disgust'] = 0
        sentiment_count['fear'] = 0
        sentiment_count['happy'] = 0
        sentiment_count['sad'] = 0

        model = Testing.start_predicting(BASE_DIR)

        for elem in listOfFaces:
            print(elem)
            filename = elem

            result = Testing.predict(filename, model)
            # print(action_dict[result])
            s = action_dict[result]
            cnt = sentiment_count[s]
            cnt = cnt + 1
            sentiment_count[s] = cnt

        str_template = str_template + f"anger: {sentiment_count['anger']} , disgust: {sentiment_count['disgust']}, fear: {sentiment_count['fear']}, happy: {sentiment_count['happy']}, sad: {sentiment_count['sad']} "
        result = str_template
        ###############

        #######################################################


        ud = tbl_CastingApplication(appl_castingcall_id=appl_castingcall_id,
                                    appl_art_id=int(appl_art_id),
                                    application_status=application_status,
                                    application_result=application_result,dt=dt,tm=tm,video_yes_no=video_yes_no,
                                    result=result)
        ud.save()
        appl_id = tbl_CastingApplication.objects.all().aggregate(Max('id'))['id__max']

        vd = tbl_VideoUpload(application_id=appl_id, video_file=video_file)
        vd.save()

        plot_list = tbl_Plot.objects.filter(plot_castingcall_id=appl_castingcall_id)
        context = {'msg':'<h5 style="color:green">Application Registered</h5>', 'appl_castingcall_id': appl_castingcall_id, 'plot_list': plot_list}
        return render(request, './myapp/artist_casting_application_add.html', context)

    else:
        appl_castingcall_id = int(request.GET.get('appl_castingcall_id'))
        call_list = tbl_CastingCall.objects.filter(id=appl_castingcall_id)
        prod_id = call_list[0].castingteam_prod_categid

        prod_list = tbl_ProductionMaster.objects.filter(id=prod_id)
        if prod_list[0].emotion_capture == 1:
            plot_list = tbl_Plot.objects.filter(plot_castingcall_id = appl_castingcall_id)
            context = {'msg': '','appl_castingcall_id':appl_castingcall_id, 'plot_list':plot_list}
            return render(request, './myapp/artist_casting_application_add.html',context)
        else:
            try:
                appl_art_id = request.session['user_id']
            except:
                return render(request,'./myapp/artist_login.html')
            video_yes_no ='No'
            application_status = 1
            application_result = 'Unchecked'
            dt = datetime.today().strftime('%Y-%m-%d')
            tm = datetime.today().strftime('%H:%M:%S')
            result = "Not Required"

            appl_list = tbl_CastingApplication(appl_castingcall_id=appl_castingcall_id,appl_art_id=appl_art_id,video_yes_no=video_yes_no,
                                               application_status=application_status,application_result=application_result,dt=dt,tm=tm,
                                               result=result)
            appl_list.save()

            call_list = tbl_CastingCall.objects.all()
            prod_list = tbl_ProductionMaster.objects.all()
            castingteam_list = tbl_CastingTeam.objects.all()
            plot_list = tbl_Plot.objects.all()
            if len(plot_list) == 0:
                plot_list = [{'id': 0}]
            context = {'prod_list': prod_list, 'castingteam_list': castingteam_list, 'call_list': call_list,
                       'plot_list': plot_list}
            return render(request, 'myapp/artist_casting_call_view.html', context)


def artist_casting_application_view(request):
    castingcall_id = request.GET.get('castingcall_id')
    appl_list = tbl_CastingApplication.objects.filter(appl_art_id=int(request.session['user_id']),appl_castingcall_id=castingcall_id)
    try:
        appl_id = appl_list[0].id
    except:
        appl_id = 0
    prod_list = tbl_ProductionMaster.objects.all()
    video_list = tbl_VideoUpload.objects.filter(application_id=appl_id)
    casting_call = tbl_CastingCall.objects.get(id=castingcall_id)
    char = casting_call.character
    if len(video_list) == 0:
        video_list = [{'id':0}]
    if len(appl_list) == 0:
        context = {'prod_list': prod_list,
                   'appl_list': appl_list, 'video_list': video_list,'empty_msg':'<h5 style="color:red">List is Empty !<br><br><span style="color:grey">You haven\'t Applied</h5>','char':char}
    else:
        context = {'prod_list': prod_list,'appl_list': appl_list, 'video_list':video_list,'char':char}
    return render(request, 'myapp/artist_casting_application_view.html', context)


def artist_casting_application_del(request):
    appl_id = request.GET.get('appl_id')
    appl_list = tbl_CastingApplication.objects.get(id=appl_id)
    appl_list.delete()
    try:
        video_list = tbl_VideoUpload.objects.get(application_id=appl_id)
        video_list.delete()
    except:
        pass
    return artist_casting_call_view(request)
