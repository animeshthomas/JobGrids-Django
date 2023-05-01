from django.db import models
from datetime import date
from django.urls import reverse
#Admin

#Job Seekers Database
class Job_Seekers(models.Model):
    sid=models.IntegerField(primary_key=True)
    #Personal
    name=models.CharField('Your Name',max_length=50)
    address=models.CharField('Your Address',max_length=250)
    dob=models.DateField('Date Of Birth',default=date.today)
    contact=models.IntegerField('Phone Number')
    photo=models.ImageField('Your Image in jpg/png Format',upload_to='seekers/')
    resume=models.FileField(upload_to='resume/')
    skill=models.CharField('Skills',max_length=150,blank=True)
    email=models.EmailField('Email')
    password=models.CharField(max_length=20)
    usertype=models.CharField(max_length=20,default='Seeker')

    def __str__(self):
        return self.name

    def get_resume_download_url(self):
        return reverse('resume_download', args=[str(self.sid)])

    class Meta:
        verbose_name = 'View Job Seeker Profile'
#JobProviders DataBase
class Job_Providers(models.Model):
    #Company Information
    pid=models.IntegerField(primary_key=True)
    cname=models.CharField('Company',max_length=50)
    ceo=models.CharField('CEO Name',max_length=50)
    tagline=models.CharField('Company Tagline',max_length=100)
    category=models.CharField('Company Category',max_length=25)
    des=models.CharField('Company Description',max_length=500)
    phone=models.IntegerField('Company Phone Number')
    website=models.CharField('Company Website',max_length=100)
    empno=models.IntegerField('No Of Employees')
    started=models.DateField('Started Rate')
    photo = models.ImageField('Company Image in jpg/png Format', upload_to='company/')
    license=models.FileField('Company Licence in pdf Format', upload_to='license/')
    status=models.CharField('Current Status',max_length=20,default='Not Verified')
    is_verified = models.BooleanField('Verification Status', default=False)
    # Login Credentials
    email = models.EmailField('Email')
    password = models.CharField(max_length=20)
    usertype = models.CharField(max_length=20, default='Provider')
    def __str__(self):
        return self.cname
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('view_license/<int:provider_id>/', self.admin_site.admin_view(self.view_license), name='view_license'),
        ]
        return my_urls + urls
    class Meta:
        verbose_name = 'Verify Company Profile'

class Post_Job(models.Model):
    #basic
    jid=models.IntegerField(primary_key=True)
    title=models.CharField('Job Title',max_length=75)
    type=models.CharField('Job Type',max_length=60)
    location=models.CharField('Job Location',max_length=50)
    des=models.CharField('Job Description',max_length=500)
    reqirement=models.CharField('Job Requirements',max_length=300)
    # Company Information
    pid = models.CharField("Company Id",default=1,max_length=50)
    cname = models.ForeignKey(Job_Providers,on_delete=models.CASCADE)
    category = models.CharField('Company Category', max_length=250)#autofillusingsession
    status = models.CharField(max_length=25, default='Open')
    category=models.CharField(max_length=25,default='Not Selected')
    timestamp = models.DateTimeField(auto_now=True)
    salary=models.TextField('Salary Package',default='NOT DISCLOSED')
    deadline=models.DateField(null=True,blank=True)

    def __str__(self):
        return f"{self.title} By {self.cname}"
    class Meta:
        verbose_name = 'View Posted Job'


class Apply(models.Model):
    sid = models.IntegerField('User ID',default=0)
    name = models.CharField('User Name',max_length=55, default=0,blank=True)
    pid = models.IntegerField('Comapany Id',default=0)
    cname = models.CharField('Company Name',max_length=55,default=0)
    jid = models.IntegerField()
    title = models.CharField('Job Title', max_length=55,default=0)
    type = models.CharField(max_length=55,default=0)
    email = models.EmailField(default=0)
    timestamp = models.DateTimeField(auto_now=True)
    status = models.CharField('Application Status',max_length=25,default='NOT SELECTED')
    def __str__(self):
        return f"{self.name} Applied the For Job: {self.title}"
    class Meta:
        verbose_name = 'View Applicant Detail'

class Review(models.Model):
    seeker = models.ForeignKey(Job_Seekers,on_delete=models.CASCADE,blank=True)
    provider = models.ForeignKey(Job_Providers, on_delete=models.CASCADE, blank=True)
    title = models.CharField('Review',max_length=300)
    stars = models.IntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now=True)
    usertype = models.CharField(max_length=20, default='Unknown')
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'View Testimonial'