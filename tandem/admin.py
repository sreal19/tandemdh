from django.contrib import admin

# Register your models here.
from tandem.models import Project

#class FilesInline(admin.TabularInline):
#     model = Infile
#     extra = 3



#class ProjectAdmin(admin.ModelAdmin):
  #  fields = ['create_date', 'project_name', 'input_folder' ]
#   fieldsets = [
#        (None,                  {'fields': ['project_name']}),
#        ('Date Information',    {'fields': ['create_date'], 'classes': ['collapse']}),
##     ]
#    inlines = [FilesInline]
 #   list_display = ('project_name', 'create_date', 'was_created_recently')
  #  list_filter = ['create_date']
   # search_fields = ['project_name']

admin.site.register(Project)