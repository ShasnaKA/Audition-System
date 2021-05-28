
# Create your models here.
from django.db import models

# Create your models here.

class tbl_Login(models.Model):
    uname = models.CharField(max_length=50)
    pswd = models.CharField(max_length=20)
    utype = models.CharField(max_length=20)
    status = models.IntegerField()
    def __str__(self):
        return self.uname + ', utype= ' + self.utype

class tbl_Contact(models.Model):
    email = models.CharField(max_length=15)
    contact = models.CharField(max_length=20)
    msg = models.CharField(max_length=500)

class tbl_ProductionMaster(models.Model):
    prod_categ = models.CharField(max_length=150)
    emotion_capture = models.IntegerField()
    def __str__(self):
        return self.prod_categ



class tbl_Artist(models.Model):
    art_login_id = models.IntegerField()
    art_fname = models.CharField(max_length=150)
    art_lname = models.CharField(max_length=150)
    art_DOB = models.CharField(max_length=10)
    art_age = models.IntegerField()
    art_gender = models.CharField(max_length=10)
    art_address = models.CharField(max_length=250)
    art_city = models.CharField(max_length=150)
    art_state = models.CharField(max_length=100)
    art_country = models.CharField(max_length=100)
    art_pin = models.CharField(max_length=20)
    art_contact = models.CharField(max_length=20)
    art_email = models.CharField(max_length=250)
    art_work_title = models.CharField(max_length=250)
    art_compensation = models.CharField(max_length=50)
    art_bio = models.CharField(max_length=300)
    art_headphoto = models.CharField(max_length=500)
    def __str__(self):
        return self.art_fname


class tbl_CastingTeam(models.Model):
    castingteam_login_id = models.IntegerField()
    castingteam_company = models.CharField(max_length=250)
    castingteam_producer = models.CharField(max_length=150)
    castingteam_address = models.CharField(max_length=250)
    castingteam_city = models.CharField(max_length=150)
    castingteam_state = models.CharField(max_length=150)
    castingteam_country = models.CharField(max_length=150)
    castingteam_pincode = models.CharField(max_length=50)
    castingteam_contact = models.CharField(max_length=20)
    castingteam_email = models.CharField(max_length=150)
    def __str__(self):
        return self.castingteam_company


class tbl_CastingTeamProductions(models.Model):
    castingteam_id = models.IntegerField()
    castingteam_prod_categid = models.IntegerField()

class tbl_CastingCall(models.Model):
    castingteam_id = models.IntegerField()
    posted_date = models.CharField(max_length=50)
    posted_time = models.CharField(max_length=50)
    character = models.CharField(max_length=150)
    role_desc = models.CharField(max_length=500)
    gender = models.CharField(max_length=50)
    age_from = models.IntegerField()
    age_to = models.IntegerField()
    castingteam_prod_categid = models.IntegerField()
    call_expiry = models.CharField(max_length=50)
    job_duration = models.CharField(max_length=50)
    #castingcall_status = models.IntegerField()
    #castingcall_video_needed = models.IntegerField()
    def __str__(self):
        return self.character


class tbl_Plot(models.Model):
    plot_castingcall_id = models.IntegerField()
    plot_desc = models.CharField(max_length=500)
    plot_emotion = models.CharField(max_length=20)
    plot_video_duration = models.CharField(max_length=50)
    def __str__(self):
        return self.plot_desc


class tbl_CastingApplication(models.Model):
    appl_castingcall_id = models.IntegerField()
    appl_art_id = models.IntegerField()
    video_yes_no = models.CharField(max_length=350)
    application_status = models.IntegerField()
    application_result = models.CharField(max_length=20)
    dt = models.CharField(max_length=10)
    tm = models.CharField(max_length=10)
    result = models.CharField(max_length=350)


class tbl_VideoUpload(models.Model):
    application_id = models.IntegerField()
    video_file = models.CharField(max_length=500)



