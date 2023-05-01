from django.contrib import admin
from .models import *
from django.urls import reverse
from django.utils.html import format_html
from .models import Job_Providers
from django.utils.safestring import mark_safe
from django.contrib.admin import AdminSite

from django.contrib.auth.models import Group, User

# Unregister the Group and User models from the admin site
# admin.site.unregister(Group)
# admin.site.unregister(User)



class Job_SeekersAdmin(admin.ModelAdmin):
    list_display = ('display_photo', 'name', 'dob', 'contact', 'skill', 'email')

    def display_photo(self, obj):
        return format_html('<img src="{}" width="50" height="50" />'.format(obj.photo.url))

    display_photo.short_description = 'Profile Photo'



class JobProvidersAdmin(admin.ModelAdmin):
    list_display = ('display_photo','cname', 'ceo', 'is_verified', 'view_license_button')
    search_fields = ('cname', 'ceo', 'category', 'phone', 'website', 'des')

    def view_license_button(self, obj):
        url = reverse('view_license', args=[obj.pk])
        return format_html('<b><a class="button" href="{}">View License</a></b>', url)

    def display_photo(self, obj):
        return format_html('<img src="{}" width="50" height="50" />'.format(obj.photo.url))

    display_photo.short_description = 'logo'
    view_license_button.short_description = ''

    def verify_license(self, request, queryset):
        for provider in queryset:
            provider.status = 'Verified'
            provider.is_verified = True
            provider.save()

    verify_license.short_description = "Verify selected providers' licenses"

    actions = [verify_license]

admin.site.register(Job_Providers, JobProvidersAdmin)

class PostJobAdmin(admin.ModelAdmin):
    list_display = ('company_logo','title', 'type', 'location', 'cname', 'status', 'timestamp', 'salary')
    def company_logo(self, obj):
        return mark_safe(f'<img src="{obj.cname.photo.url}" width="50px" height="50px" />')

admin.site.register(Post_Job, PostJobAdmin)

from django.contrib import admin
from .models import Apply


class ApplyAdmin(admin.ModelAdmin):
    list_display = ('name', 'cname', 'title', 'status', 'timestamp')
    # list_filter = ('status', 'timestamp', 'type')
    search_fields = ('name', 'cname', 'title', 'email')
    # Add custom headings for the columns
    # list_display_links = None

    def name(self, obj):
        return obj.name.upper()

    name.admin_order_field = 'name'
    name.short_description = 'Applicant Name'

    def cname(self, obj):
        return obj.cname.upper()

    cname.admin_order_field = 'cname'
    cname.short_description = 'Company Name'

    def title(self, obj):
        return obj.title.upper()

    title.admin_order_field = 'title'
    title.short_description = 'Job Title'

    def status(self, obj):
        return obj.status.upper()

    status.admin_order_field = 'status'
    status.short_description = 'Application Status'

    def timestamp(self, obj):
        return obj.timestamp.strftime('%Y-%m-%d %H:%M:%S')

    timestamp.admin_order_field = 'timestamp'
    timestamp.short_description = 'Application Time'

admin.site.register(Job_Seekers, Job_SeekersAdmin)
admin.site.register(Apply, ApplyAdmin)

from django.contrib import admin
from django.utils.html import format_html
from .models import Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('get_user_image', 'short_title', 'get_user_details', 'get_combined_rating', 'created_at')

    def get_user_image(self, obj):
        if obj.usertype == 'Job Seeker':
            image_url = obj.seeker.photo.url if obj.seeker.photo else ''
        elif obj.usertype == 'Provider':
            image_url = obj.provider.photo.url if obj.provider.photo else ''
        else:
            image_url = ''
        return format_html('<img src="{}" width="50" height="50">', image_url)

    get_user_image.short_description = 'Image'

    def get_user_details(self, obj):
        if obj.usertype == 'Job Seeker':
            user_details = f'{obj.seeker.name}'
        elif obj.usertype == 'Provider':
            user_details = f'{obj.provider.cname}'
        else:
            user_details = ''
        return format_html(user_details)

    get_user_details.short_description = 'Name'
    get_user_details.allow_tags = True

    def short_title(self, obj):
        return ' '.join(obj.title.split()[:3]) + '...' if len(obj.title.split()) > 3 else obj.title

    short_title.short_description = 'Review'

    def get_combined_rating(self, obj):
        stars_html = ''
        for i in range(obj.stars):
            stars_html += '<i class="fas fa-star" style="color: gold;"></i>'
        return format_html(f'{obj.stars} {stars_html}/5')

    get_combined_rating.short_description = 'Rating'

admin.site.register(Review, ReviewAdmin)


