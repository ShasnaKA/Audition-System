from django.contrib import admin

# Register your models here.
from .models import tbl_Login,tbl_Contact,tbl_ProductionMaster,tbl_Artist,tbl_CastingTeam
from .models import tbl_CastingTeamProductions,tbl_CastingCall,tbl_Plot,tbl_CastingApplication,tbl_VideoUpload

admin.site.register(tbl_Login)
admin.site.register(tbl_Contact)
admin.site.register(tbl_ProductionMaster)
admin.site.register(tbl_Artist)
admin.site.register(tbl_CastingTeam)
admin.site.register(tbl_CastingTeamProductions)
admin.site.register(tbl_CastingCall)
admin.site.register(tbl_Plot)
admin.site.register(tbl_CastingApplication)
admin.site.register(tbl_VideoUpload)