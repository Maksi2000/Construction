
# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class UserModel(UserAdmin):
    ordering = ('email',)


admin.site.register(CustomUser)
admin.site.register(Architect)
admin.site.register(Engineer)
admin.site.register(Client)
admin.site.register(ConstructionProjects)
admin.site.register(ArchitectTask)
admin.site.register(EngineerTask)
admin.site.register(FeedbackArchitect)
admin.site.register(NotificationArchitect)
admin.site.register(FeedbackEngineer)
admin.site.register(NotificationEngineer)