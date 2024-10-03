from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import TutorRequest,TutorRegistration,Requestpost,Message,teacher_addcard, student_addcard
from django.core.mail import send_mail , message,EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
import random
from twilio.rest import Client
from urllib.parse import parse_qs

# Create your views here.
def mains(request):
    return render(request,"main.html")
def tutor_request(request):
    if request.method=="POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        location = request.POST.get("location")
        phone = request.POST.get("phone")
        w_number = request.POST.get("w_number")
        if TutorRequest.objects.filter(email=email).exists():
            return HttpResponse("Email already exists")
        else:
            c=random.randint(100, 1000)
            password=f'{name}@{c}'
            TutorRequest.objects.create(
                name=name,
                email=email,
                location=location,
                phone=phone,
                w_number=w_number,
            
                password=password
            )
            login={"name":name,"email":email,"password":password}
            html_template="email_verify.html"
            html_message=render_to_string(html_template,login)
        
            email_from=settings.EMAIL_HOST_USER
            r_list=[email]
            subject="Action required: Please confirm to post requirement"
            message=EmailMessage(subject,html_message,email_from,r_list)
            message.content_subtype='html'
            message.send()


            
            return render(request, 'mailceck.html')
        


        
        
        # Validate the data if necessary
        
        # Save the data to the database
       
    
    return render(request, 'request_tutor.html')

def addpost(request,email):
    student = TutorRequest.objects.filter(email=email).first()
    if request.method=="POST":
        dyr = request.POST.get("dyr")
        level = request.POST.get("level")
        subject = request.POST.get("subject")
        two_subject = request.POST.get("two_subject")
        three_subject = request.POST.get("three_subject")
        i_want = request.POST.get("i_want")
        meeting_option= request.POST.get("meeting_option")
        budget = request.POST.get("budget")
        budget_need = request.POST.get("budget_need")
        
        language = request.POST.get("language")
        tutor_want = request.POST.get("tutor_want")
        need = request.POST.get("need")
        message = request.POST.get("message")
        gender = request.POST.get("gender")
        l=TutorRequest.objects.filter(email=email).first()
        r=Requestpost.objects.create( 
            email=email,
            dyr=dyr,
            level=level,
            subject=subject,
            two_subject=two_subject,
            three_subject=three_subject,
            i_want=i_want,
            meeting_option=meeting_option,
         
            budget=budget,
            budget_need=budget_need,
            gender=gender,
            language=language,
            tutor_want=tutor_want,
            need=need,
            message=message,
            location=l.location
            )
 
        post = Requestpost.objects.filter(email=email).values
        student = TutorRequest.objects.filter(email=email).first()
        return render(request,"mypost.html",{"all":post,"post":student})

    return render(request,"addpost.html",{"name":student.name,"email":email})



def email_verify(request,email):
    
    return render(request, 'email_verifed.html',{"email":email})


#-----------------------my post-------------------------------------------------
def myposts(request,email):
      post = Requestpost.objects.filter(email=email).values
      student = TutorRequest.objects.filter(email=email).first()
      return render(request,"mypost.html",{"all":post,"post":student})



def delete_posst(request,id):
    post= Requestpost.objects.get(id=id)
    email=post.email
    post.delete()
    return redirect(myposts, email=email)
   





def stu_login(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
      
        if TutorRequest.objects.filter(email=email,password=password).exists():
            post = Requestpost.objects.filter(email=email).values
            student = TutorRequest.objects.filter(email=email).first()
            return render(request,"mypost.html",{"all":post,"post":student})
           
        else:
            return render(request,"login.html",{"msg":"your login detail is wong"})


    return render(request,"login.html")


def teacher_reg(request):
    if request.method == "POST":
       name = request.POST.get('name')
       email = request.POST.get('email')
       password = request.POST.get('password')
       confirm_password = request.POST.get('confirm_password')
       if TutorRegistration.objects.filter(email=email,password=password).exists():
           
          return render(request,"teacher_regs.html",{"msg":"your account  is already exist"})
       else:
           TutorRegistration.objects.create(
                name=name,
                email=email,
                password=password,
                confirm_password=confirm_password,
            )
           ds={"name":name,"email":email,"msg":"successfully registered  your account in learnersleaf"}

           return render(request, 'details.html', ds)
    
    return render(request, 'teacher_regs.html')
def details(request,email):
    print(email)
    if request.method == "POST":
        types = request.POST.get('types')
        strength = request.POST.get('strength')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('dates')
        location = request.POST.get('location')
        language = request.POST.get('lanquage')
        post_code = request.POST.get('post_code')

        #  # Example: using session to get the tutor id
        tutor = TutorRegistration.objects.filter(email=email).first()

        # Update the tutor details
        tutor.types = types
        tutor.strength = strength
        tutor.gender = gender
        tutor.date_of_birth = date_of_birth
        tutor.location = location
        tutor.language=language
        tutor.post_code = post_code
        tutor.save()
        msg="you personal detail has saved"
        ds={"name":tutor.name,"email":tutor.email,"msg":msg}
        return render(request, 'subject.html',ds)

  
  

#subject

def subject(request,email):
    if request.method == "POST":
        subject = request.POST.get('subject')
        level = request.POST.get('level')
        to_level = request.POST.get('to_level')
        #two
        two_subject = request.POST.get('two_subject')
        two_level = request.POST.get('two_level')
        two_to_level = request.POST.get('to_level')
        #three
        three_subject = request.POST.get('three_subject')
        three_level = request.POST.get('three_level')
        three_to_level = request.POST.get('three_to_level')
        #four
        four_subject = request.POST.get('four_subject')
        four_level = request.POST.get('four_level')
        four_to_level = request.POST.get('four_to_level')

        #five
        five_subject = request.POST.get('five_subject')
        five_level = request.POST.get('five_level')
        five_to_level = request.POST.get('five_to_level')
        tutor = TutorRegistration.objects.filter(email=email).first()
        if tutor:
            # Update the tutor details from the POST data
            tutor.subject = subject
            tutor.from_level=level
            tutor.to_level=to_level
            tutor.two_subject = two_subject
            tutor.two_from_level=two_level
            tutor.two_to_level=two_to_level
            tutor.three_subject = three_subject
            tutor.three_from_level=three_level
            tutor.three_to_level=three_to_level
            tutor.four_subject=four_subject
            tutor.four_from_level=four_level
            tutor.four_to_level=four_to_level
            tutor.five_subject=five_subject
            tutor.five_from_level=five_level
            tutor.five_to_level=five_to_level
           

            # Save the updated details
            tutor.save()

            # Prepare the data to be passed to the next template
            ds = {"name": tutor.name, "email": tutor.email}
            return render(request, 'eduction.html',ds)
# add ....subject

def addsubject(request,email):
    if request.method == "POST":
        subject = request.POST.get('subject')
        level = request.POST.get('level')
        to_level = request.POST.get('to_level')
        tutor = TutorRegistration.objects.filter(email=email).first()
        name = tutor.name
        email = tutor.email
        password = tutor.password
        TutorRegistration.objects.create(name=name,email=email,password=password,subject=subject,from_level=level,to_level=to_level)
        ds={"name":name,"email":email}
        return render(request,"eduction.html",ds)
    


#add cerficate

def certificate(request, email):
    tutor = TutorRegistration.objects.filter(email=email).first()
    ds={"name":tutor.name,"email":tutor.email,"msg":"your subject saves"}
    if request.method == "POST":
        # Get data from POST request
        institution_name = request.POST.get('institution_name')
        degree_type = request.POST.get('degree_type')
        degree_name = request.POST.get('degree_name')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        association = request.POST.get('association')

        # Fetch the tutor based on the email
        tutor = TutorRegistration.objects.filter(email=email).first()

        if tutor:
            # Update the tutor details
            tutor.institution_name = institution_name
            tutor.degree_type = degree_type
            tutor.degree_name = degree_name
            tutor.start_date = start_date
            tutor.end_date = end_date
            tutor.association = association
            tutor.save()

            ds={"name":tutor.name,"email":tutor.email,"msg":"your  Education saves"}

            # Redirect to a success page or another step
            return render(request, 'add_eduction.html', ds)
    return render(request,"eduction.html",ds)


    # If GET request, just render the form template

def addcertificate(request, email):
    tutor = TutorRegistration.objects.filter(email=email).first()
    name=tutor.name
    email=tutor.email
    password=tutor.password
    ds={"name":tutor.name,"email":tutor.email,"msg":"your  Education saves"}
    if request.method == "POST":
        # Get data from POST request
        institution_name = request.POST.get('institution_name')
        degree_type = request.POST.get('degree_type')
        degree_name = request.POST.get('degree_name')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        association = request.POST.get('association')

        # Fetch the tutor based on the email
        tutor = TutorRegistration.objects.filter(email=email).first()
        name=tutor.name
        email=tutor.email
        password=tutor.password
        TutorRegistration.objects.create(name=name,email=email,password=password,institution_name=institution_name,degree_type=degree_type,degree_name=degree_name,start_date=start_date,end_date=end_date,association=association)

        
          

        ds={"name":tutor.name,"email":tutor.email,"msg":"your  Education saves"}

            # Redirect to a success page or another step
        return render(request, 'company_emp.html', ds)   
    return render(request, 'company_emp.html', ds)

def company_emp(request,email):
    tutor = TutorRegistration.objects.filter(email=email).first()
    name=tutor.name
    email=tutor.email
    password=tutor.password
    ds={"name":tutor.name,"email":tutor.email,"msg":"your education is saved"}
    if request.method=="POST":
          company_name=request.POST.get('company_name')
          job_roll=request.POST.get('job_roll')
          start_date=request.POST.get('start_date')
          end_date=request.POST.get('end_date')
          job_description=request.POST.get('job_description')

          tutor = TutorRegistration.objects.filter(email=email).first()
          tutor.company_name=company_name
          tutor.job_roll=job_roll
          tutor.job_start_date=start_date
          if end_date:
              tutor.job_end_date=end_date
          tutor.save()
          ds={"name":tutor.name,"email":tutor.email}
          return render(request,'teaching_detail.html',ds)
    return render(request, 'company_emp.html', ds)

def teaching_detail(request, email):
    if request.method == "POST":
        # Retrieve the data from the POST request
        i_charge = request.POST.get('i_charge')
        min_fee = request.POST.get('min_fee')
        max_fee = request.POST.get('max_fee')
        total_experience = request.POST.get('total_experience')
        teaching_experience = request.POST.get('teaching_experience')
        online_experience = request.POST.get('online_experience')
        travel = request.POST.get('travel')
        online_teach = request.POST.get('online_teach')
        homework = request.POST.get('homework')
        full_time = request.POST.get('full_time')
        interested_in = request.POST.get('interested_in')

        # Fetch the tutor record based on the email
        tutor = TutorRegistration.objects.filter(email=email).first()

        if tutor:
            # Update the tutor's details with the form data
            tutor.i_charge = i_charge
            tutor.min_fee = min_fee
            tutor.max_fee = max_fee
            tutor.total_experience = total_experience
            tutor.teaching_experience = teaching_experience
            tutor.online_experience = online_experience
            tutor.willing_to_travel = travel
            tutor.available_for_online_teaching = online_teach
            tutor.help_with_homework  = homework
            tutor.full_time_teacher = full_time
            tutor.interested_in = interested_in
            tutor.save()
            ds={"name":tutor.name,"email":tutor.email}

            # Redirect to a success page or another view
            return render(request, 'personal_detail.html', {'email': email})  # Replace with actual page

    # If GET request, render the form template
    return render(request, 'teaching_detail_form.html', {'email': email})


def personal_detail(request,email):
    if request.method == "POST":
        profile_description = request.POST.get('profile_description')
        
        
        # Handle file uploads
        id_proof = request.FILES['id_proof']
        profile_photo = request.FILES['profile']
        number=request.POST.get("number")
        
        tutor = TutorRegistration.objects.filter(email=email).first()
        if tutor:
            tutor.profile_description = profile_description
            tutor.id_proof=id_proof
            tutor.profile_photo=profile_photo
            tutor.phone=number
            tutor.filename=f'images/{profile_photo}'
            print(tutor.filename)
            tutor.save()
            ds={"name":tutor.name,"email":tutor.email,"password":tutor.password,"number":tutor.phone,}
            html_template="teac_email_verfiy.html"
            html_message=render_to_string(html_template,ds)
       
            email_from=settings.EMAIL_HOST_USER
            r_list=[tutor.email]
            subject="Action required: Please confirm to account contact details"
            message=EmailMessage(subject,html_message,email_from,r_list)
            message.content_subtype='html'
            message.send()

            return render(request,"tech_email_sented.html",ds)
        return render(request,"personal_detail.html")
    return render(request,"personal_detail.html")
    
def teacher_email_verifed(request,email):
     tutor = TutorRegistration.objects.filter(email=email).first()
     ds={"name":tutor.name,"email":tutor.email}
     return render(request,"teacher_email_verifed.html",ds)

#teacher login
def teach_login(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')

        student = TutorRegistration.objects.filter(email=email,password=password).values
        print(student)
        if TutorRegistration.objects.filter(email=email,password=password).exists():
            name=TutorRegistration.objects.filter(password=password).first()
            return render(request,"teacher_dasboad.html",{"all":student,"name":name.name,"email":email})
        else:
            return render(request,"login.html",{"msg":"your login detail is wong"})
   


    return render(request,"login.html")

def teacher_dashboard(request,email):
    tutor = TutorRegistration.objects.filter(email=email).values()
    tutors = TutorRegistration.objects.filter(email=email).first()

    return render(request,"teacher_dasboad.html",{"all":tutor,"name":tutors.name,"email":tutors.email})


def myprofile(request,email):
    tutor = TutorRegistration.objects.filter(email=email).values()
    first=TutorRegistration.objects.filter(email=email).first()
    p={"all":tutor,"name":first.name,"roll":first.job_roll,"first":first}
    return render(request,"myprofile.html",p)

def search_teacher(request):
    l=[
                "Chennai, Tamil Nadu", "Coimbatore, Tamil Nadu", "Madurai, Tamil Nadu", "Salem, Tamil Nadu",
                "Tiruchirappalli, Tamil Nadu", "Tirunelveli, Tamil Nadu", "Vellore, Tamil Nadu", "Erode, Tamil Nadu",
                "Kanchipuram, Tamil Nadu", "Thanjavur, Tamil Nadu", "Tiruppur, Tamil Nadu", "Nagapattinam, Tamil Nadu",
                "Kumbakonam, Tamil Nadu", "Dharmapuri, Tamil Nadu", "Karur, Tamil Nadu", "Sivakasi, Tamil Nadu",
                "Dindigul, Tamil Nadu", "Ramanathapuram, Tamil Nadu", "Tuticorin, Tamil Nadu", "Cuddalore, Tamil Nadu",
                "Vellore, Tamil Nadu", "Ariyalur, Tamil Nadu", "Perambalur, Tamil Nadu", "Nagercoil, Tamil Nadu",
                "Theni, Tamil Nadu", "Kodaikanal, Tamil Nadu", "Pollachi, Tamil Nadu", "Pudukkottai, Tamil Nadu",
                "Tiruvallur, Tamil Nadu", "Tiruvannamalai, Tamil Nadu", "Chengalpattu, Tamil Nadu", "Tirupathur, Tamil Nadu",
                "Sankarankovil, Tamil Nadu", "Kovilpatti, Tamil Nadu", "Manapparai, Tamil Nadu", "Thiruthuraipoondi, Tamil Nadu",
                "Ramanathapuram, Tamil Nadu"
            ]
   
    if request.method=="POST":
        subject=request.POST.get('subject')
        location=request.POST.get('location')
        if TutorRegistration.objects.filter(subject=subject,location=location).exists():
          
            tutors = TutorRegistration.objects.filter(subject=subject,location=location).values()
           
        elif TutorRegistration.objects.filter(subject=subject).exists():
            tutors=TutorRegistration.objects.filter(subject=subject).values()
        elif TutorRegistration.objects.filter(location=location).exists():
            tutors=TutorRegistration.objects.filter(location=location).values()
        d={"tutors":tutors,"locations":l}
        return render(request,"all_teacher.html",d)
    all_tutor=TutorRegistration.objects.all()
    return render(request,"all_teacher.html",{"tutors":all_tutor,"locations":l})



#_______________________________________________________________________________________________________________________________________
from urllib.parse import unquote
def fliter_location(request,location):
    l=[
                "Chennai, Tamil Nadu", "Coimbatore, Tamil Nadu", "Madurai, Tamil Nadu", "Salem, Tamil Nadu",
                "Tiruchirappalli, Tamil Nadu", "Tirunelveli, Tamil Nadu", "Vellore, Tamil Nadu", "Erode, Tamil Nadu",
                "Kanchipuram, Tamil Nadu", "Thanjavur, Tamil Nadu", "Tiruppur, Tamil Nadu", "Nagapattinam, Tamil Nadu",
                "Kumbakonam, Tamil Nadu", "Dharmapuri, Tamil Nadu", "Karur, Tamil Nadu", "Sivakasi, Tamil Nadu",
                "Dindigul, Tamil Nadu", "Ramanathapuram, Tamil Nadu", "Tuticorin, Tamil Nadu", "Cuddalore, Tamil Nadu",
                "Vellore, Tamil Nadu", "Ariyalur, Tamil Nadu", "Perambalur, Tamil Nadu", "Nagercoil, Tamil Nadu",
                "Theni, Tamil Nadu", "Kodaikanal, Tamil Nadu", "Pollachi, Tamil Nadu", "Pudukkottai, Tamil Nadu",
                "Tiruvallur, Tamil Nadu", "Tiruvannamalai, Tamil Nadu", "Chengalpattu, Tamil Nadu", "Tirupathur, Tamil Nadu",
                "Sankarankovil, Tamil Nadu", "Kovilpatti, Tamil Nadu", "Manapparai, Tamil Nadu", "Thiruthuraipoondi, Tamil Nadu",
                "Ramanathapuram, Tamil Nadu"
            ]
    decoded_once = unquote(location)  # First level of decoding
    decoded_twice = unquote(decoded_once)   # Second level of decoding

    print(decoded_twice)
    if TutorRegistration.objects.filter(location=decoded_twice).exists():
        tutors=TutorRegistration.objects.filter(location=decoded_twice).values()
    else:
        tutors=TutorRegistration.objects.all().values()
    return render(request,"all_teacher.html",{"tutors":tutors,"locations":l,"heading":"All Tutors"})

#__________________________________________________________________________________
def online_tutor(request):
    l=[
                "Chennai, Tamil Nadu", "Coimbatore, Tamil Nadu", "Madurai, Tamil Nadu", "Salem, Tamil Nadu",
                "Tiruchirappalli, Tamil Nadu", "Tirunelveli, Tamil Nadu", "Vellore, Tamil Nadu", "Erode, Tamil Nadu",
                "Kanchipuram, Tamil Nadu", "Thanjavur, Tamil Nadu", "Tiruppur, Tamil Nadu", "Nagapattinam, Tamil Nadu",
                "Kumbakonam, Tamil Nadu", "Dharmapuri, Tamil Nadu", "Karur, Tamil Nadu", "Sivakasi, Tamil Nadu",
                "Dindigul, Tamil Nadu", "Ramanathapuram, Tamil Nadu", "Tuticorin, Tamil Nadu", "Cuddalore, Tamil Nadu",
                "Vellore, Tamil Nadu", "Ariyalur, Tamil Nadu", "Perambalur, Tamil Nadu", "Nagercoil, Tamil Nadu",
                "Theni, Tamil Nadu", "Kodaikanal, Tamil Nadu", "Pollachi, Tamil Nadu", "Pudukkottai, Tamil Nadu",
                "Tiruvallur, Tamil Nadu", "Tiruvannamalai, Tamil Nadu", "Chengalpattu, Tamil Nadu", "Tirupathur, Tamil Nadu",
                "Sankarankovil, Tamil Nadu", "Kovilpatti, Tamil Nadu", "Manapparai, Tamil Nadu", "Thiruthuraipoondi, Tamil Nadu",
                "Ramanathapuram, Tamil Nadu"
            ]
    all_tutor=TutorRegistration.objects.filter(available_for_online_teaching="yes")
    return render(request,"all_teacher.html",{"tutors":all_tutor,"locations":l,"heading":"Online Tutors"})

def home_tutor(request):
    l=[
                "Chennai, Tamil Nadu", "Coimbatore, Tamil Nadu", "Madurai, Tamil Nadu", "Salem, Tamil Nadu",
                "Tiruchirappalli, Tamil Nadu", "Tirunelveli, Tamil Nadu", "Vellore, Tamil Nadu", "Erode, Tamil Nadu",
                "Kanchipuram, Tamil Nadu", "Thanjavur, Tamil Nadu", "Tiruppur, Tamil Nadu", "Nagapattinam, Tamil Nadu",
                "Kumbakonam, Tamil Nadu", "Dharmapuri, Tamil Nadu", "Karur, Tamil Nadu", "Sivakasi, Tamil Nadu",
                "Dindigul, Tamil Nadu", "Ramanathapuram, Tamil Nadu", "Tuticorin, Tamil Nadu", "Cuddalore, Tamil Nadu",
                "Vellore, Tamil Nadu", "Ariyalur, Tamil Nadu", "Perambalur, Tamil Nadu", "Nagercoil, Tamil Nadu",
                "Theni, Tamil Nadu", "Kodaikanal, Tamil Nadu", "Pollachi, Tamil Nadu", "Pudukkottai, Tamil Nadu",
                "Tiruvallur, Tamil Nadu", "Tiruvannamalai, Tamil Nadu", "Chengalpattu, Tamil Nadu", "Tirupathur, Tamil Nadu",
                "Sankarankovil, Tamil Nadu", "Kovilpatti, Tamil Nadu", "Manapparai, Tamil Nadu", "Thiruthuraipoondi, Tamil Nadu",
                "Ramanathapuram, Tamil Nadu"
            ]
    all_tutor=TutorRegistration.objects.filter(willing_to_travel="yes")
    return render(request,"all_teacher.html",{"tutors":all_tutor,"locations":l,"heading":"Home Tutors"})

def search_teachers(request,email ):
    l=[
                "Chennai, Tamil Nadu", "Coimbatore, Tamil Nadu", "Madurai, Tamil Nadu", "Salem, Tamil Nadu",
                "Tiruchirappalli, Tamil Nadu", "Tirunelveli, Tamil Nadu", "Vellore, Tamil Nadu", "Erode, Tamil Nadu",
                "Kanchipuram, Tamil Nadu", "Thanjavur, Tamil Nadu", "Tiruppur, Tamil Nadu", "Nagapattinam, Tamil Nadu",
                "Kumbakonam, Tamil Nadu", "Dharmapuri, Tamil Nadu", "Karur, Tamil Nadu", "Sivakasi, Tamil Nadu",
                "Dindigul, Tamil Nadu", "Ramanathapuram, Tamil Nadu", "Tuticorin, Tamil Nadu", "Cuddalore, Tamil Nadu",
                "Vellore, Tamil Nadu", "Ariyalur, Tamil Nadu", "Perambalur, Tamil Nadu", "Nagercoil, Tamil Nadu",
                "Theni, Tamil Nadu", "Kodaikanal, Tamil Nadu", "Pollachi, Tamil Nadu", "Pudukkottai, Tamil Nadu",
                "Tiruvallur, Tamil Nadu", "Tiruvannamalai, Tamil Nadu", "Chengalpattu, Tamil Nadu", "Tirupathur, Tamil Nadu",
                "Sankarankovil, Tamil Nadu", "Kovilpatti, Tamil Nadu", "Manapparai, Tamil Nadu", "Thiruthuraipoondi, Tamil Nadu",
                "Ramanathapuram, Tamil Nadu"
            ]
    student=TutorRequest.objects.get(email=email)
    
    all_tutor=TutorRegistration.objects.all()
    account=Requestpost.objects.filter(email=email).first()
    accounts=TutorRequest.objects.filter(email=email).first()
    if request.method=="POST":
        
        subject=request.POST.get('subject')
        location=request.POST.get('location')
        if TutorRegistration.objects.filter(subject=subject,location=location).exists():
          
            tutors = TutorRegistration.objects.filter(subject=subject,location=location).values()
           
        elif TutorRegistration.objects.filter(subject=subject).exists():
            tutors=TutorRegistration.objects.filter(subject=subject).values()
        elif TutorRegistration.objects.filter(location=location).exists():
            tutors=TutorRegistration.objects.filter(location=location).values()
        d={"tutors":tutors,"locations":l,"account":account,"accounts":accounts}
        return render(request,"all_teacher.html",d)
   
    
    return render(request,"all_teacher.html",{"tutors":all_tutor,"locations":l,"name":student.name,"email":student.email,"account":account,"accounts":accounts})


def online_tutor(request,email):
    l=[
                "Chennai, Tamil Nadu", "Coimbatore, Tamil Nadu", "Madurai, Tamil Nadu", "Salem, Tamil Nadu",
                "Tiruchirappalli, Tamil Nadu", "Tirunelveli, Tamil Nadu", "Vellore, Tamil Nadu", "Erode, Tamil Nadu",
                "Kanchipuram, Tamil Nadu", "Thanjavur, Tamil Nadu", "Tiruppur, Tamil Nadu", "Nagapattinam, Tamil Nadu",
                "Kumbakonam, Tamil Nadu", "Dharmapuri, Tamil Nadu", "Karur, Tamil Nadu", "Sivakasi, Tamil Nadu",
                "Dindigul, Tamil Nadu", "Ramanathapuram, Tamil Nadu", "Tuticorin, Tamil Nadu", "Cuddalore, Tamil Nadu",
                "Vellore, Tamil Nadu", "Ariyalur, Tamil Nadu", "Perambalur, Tamil Nadu", "Nagercoil, Tamil Nadu",
                "Theni, Tamil Nadu", "Kodaikanal, Tamil Nadu", "Pollachi, Tamil Nadu", "Pudukkottai, Tamil Nadu",
                "Tiruvallur, Tamil Nadu", "Tiruvannamalai, Tamil Nadu", "Chengalpattu, Tamil Nadu", "Tirupathur, Tamil Nadu",
                "Sankarankovil, Tamil Nadu", "Kovilpatti, Tamil Nadu", "Manapparai, Tamil Nadu", "Thiruthuraipoondi, Tamil Nadu",
                "Ramanathapuram, Tamil Nadu"
            ]
    all_tutor=TutorRegistration.objects.filter(available_for_online_teaching="yes")
    student=TutorRequest.objects.get(email=email)
    account=Requestpost.objects.filter(email=email).first()
    accounts=TutorRequest.objects.filter(email=email).first()
    return render(request,"online_tutors.html",{"tutors":all_tutor,"locations":l,"heading":"Online Tutors","name":student.name,"email":student.email,"account":account,"accounts":accounts})

def home_tutor(request,email):
    l=[
                "Chennai, Tamil Nadu", "Coimbatore, Tamil Nadu", "Madurai, Tamil Nadu", "Salem, Tamil Nadu",
                "Tiruchirappalli, Tamil Nadu", "Tirunelveli, Tamil Nadu", "Vellore, Tamil Nadu", "Erode, Tamil Nadu",
                "Kanchipuram, Tamil Nadu", "Thanjavur, Tamil Nadu", "Tiruppur, Tamil Nadu", "Nagapattinam, Tamil Nadu",
                "Kumbakonam, Tamil Nadu", "Dharmapuri, Tamil Nadu", "Karur, Tamil Nadu", "Sivakasi, Tamil Nadu",
                "Dindigul, Tamil Nadu", "Ramanathapuram, Tamil Nadu", "Tuticorin, Tamil Nadu", "Cuddalore, Tamil Nadu",
                "Vellore, Tamil Nadu", "Ariyalur, Tamil Nadu", "Perambalur, Tamil Nadu", "Nagercoil, Tamil Nadu",
                "Theni, Tamil Nadu", "Kodaikanal, Tamil Nadu", "Pollachi, Tamil Nadu", "Pudukkottai, Tamil Nadu",
                "Tiruvallur, Tamil Nadu", "Tiruvannamalai, Tamil Nadu", "Chengalpattu, Tamil Nadu", "Tirupathur, Tamil Nadu",
                "Sankarankovil, Tamil Nadu", "Kovilpatti, Tamil Nadu", "Manapparai, Tamil Nadu", "Thiruthuraipoondi, Tamil Nadu",
                "Ramanathapuram, Tamil Nadu"
            ]
    student=TutorRequest.objects.get(email=email)
    all_tutor=TutorRegistration.objects.filter(willing_to_travel="yes")
    account=Requestpost.objects.filter(email=email).first()
    accounts=TutorRequest.objects.filter(email=email).first()
    return render(request,"home_tutor.html",{"tutors":all_tutor,"locations":l,"heading":"Online Tutors","name":student.name,"email":student.email,"account":account,"accounts":accounts})


def fliter_location(request,location,email):
    l=[
                "Chennai, Tamil Nadu", "Coimbatore, Tamil Nadu", "Madurai, Tamil Nadu", "Salem, Tamil Nadu",
                "Tiruchirappalli, Tamil Nadu", "Tirunelveli, Tamil Nadu", "Vellore, Tamil Nadu", "Erode, Tamil Nadu",
                "Kanchipuram, Tamil Nadu", "Thanjavur, Tamil Nadu", "Tiruppur, Tamil Nadu", "Nagapattinam, Tamil Nadu",
                "Kumbakonam, Tamil Nadu", "Dharmapuri, Tamil Nadu", "Karur, Tamil Nadu", "Sivakasi, Tamil Nadu",
                "Dindigul, Tamil Nadu", "Ramanathapuram, Tamil Nadu", "Tuticorin, Tamil Nadu", "Cuddalore, Tamil Nadu",
                "Vellore, Tamil Nadu", "Ariyalur, Tamil Nadu", "Perambalur, Tamil Nadu", "Nagercoil, Tamil Nadu",
                "Theni, Tamil Nadu", "Kodaikanal, Tamil Nadu", "Pollachi, Tamil Nadu", "Pudukkottai, Tamil Nadu",
                "Tiruvallur, Tamil Nadu", "Tiruvannamalai, Tamil Nadu", "Chengalpattu, Tamil Nadu", "Tirupathur, Tamil Nadu",
                "Sankarankovil, Tamil Nadu", "Kovilpatti, Tamil Nadu", "Manapparai, Tamil Nadu", "Thiruthuraipoondi, Tamil Nadu",
                "Ramanathapuram, Tamil Nadu"
            ]
    decoded_once = unquote(location)  # First level of decoding
    decoded_twice = unquote(decoded_once)   # Second level of decoding
    student=TutorRequest.objects.get(email=email)
    account=Requestpost.objects.filter(email=email).first()
    accounts=TutorRequest.objects.filter(email=email).first()
    print(decoded_twice)
    if TutorRegistration.objects.filter(location=decoded_twice).exists():
        tutors=TutorRegistration.objects.filter(location=decoded_twice).values()
    else:
        tutors=TutorRegistration.objects.all().values()
    return render(request,"all_teacher.html",{"tutors":tutors,"locations":l,"heading":"All Tutors","name":student.name,"email":student.email,"account":account,"accounts":accounts})






def  student_inbox(request,email):
    account=Requestpost.objects.filter(email=email).first()
    accounts=TutorRequest.objects.filter(email=email).first()

    print("hee",accounts.email)
    if Message.objects.filter( receiver_email=email).exists():
        account=Requestpost.objects.filter(email=email).first()
        accounts=TutorRequest.objects.filter(email=email).first()
        sm=Message.objects.filter( receiver_email=email).values
     
        return render(request,"inbox.html",{"msg":sm,"account":account,"accounts":accounts})
    
    return render(request,"inbox.html",{"account":account,"accounts":accounts})

def student_post(request,email,id):
    if TutorRequest.objects.filter(email=email).exists():
        s=TutorRequest.objects.get(email=email)
        sp=Requestpost.objects.get(id=id)
        d={"s":s,"sp":sp}
        return render(request,"student_post.html",d)
    return render( request,"student_post.html")
    




#___________________student settings_____________________________

def stu_settings(request,email):
    account=Requestpost.objects.filter(email=email).first()
    accounts=TutorRequest.objects.filter(email=email).first()
    return render(request,"stu_settings.html",{"account":account,"accounts":accounts})


def student_profile(request,email):
    
    if request.method=="POST":
         student=Requestpost.objects.filter(email=email).first()
         profile_photo = request.FILES['profile']
         if student:
            student.profile_photo=profile_photo

            student.filename=f'stu_images/{profile_photo}'
            student.save()
            
            
            
            return render(request,"stu_settings.html",{"msg":" your Profile Photo added","accounts":student})
         else:  
             return render(request,"stu_settings.html",{"msg":"your Profile Photo not added"})
    return render(request,"stu_settins.html")


def change_e(request,email):
    if request.method=="POST":
        emails=request.POST.get('email')

        Requestpost.objects.filter(email=email).update(email=emails)
        TutorRequest.objects.filter(email=email).update(email=emails)
        account=Requestpost.objects.filter(email=emails).first()
        accounts=TutorRequest.objects.filter(email=emails).first()
        return render(request,"stu_settings.html",{"msg":" update your mail","account":account,"accounts":accounts})
def change_ph(request,email):
    if request.method=="POST":
        phone=request.POST.get('phone')

        
        TutorRequest.objects.filter(email=email).update(phone=phone)
        account=Requestpost.objects.filter(email=email).first()
        accounts=TutorRequest.objects.filter(email=email).first()
        return render(request,"stu_settings.html",{"msg":" update your Contact Number","account":account,"accounts":accounts})




#basci detail edit
def t_basic(request,email):
    a=TutorRegistration.objects.filter(email=email).first()
    if request.method=="POST":
      
        strength = request.POST.get('strength')
        gender = request.POST.get('gender')
        location = request.POST.get('location')
        language = request.POST.get('lanquage')
        if strength:
            TutorRegistration.objects.filter(email=email).update(strength=strength)
        if gender:
            TutorRegistration.objects.filter(email=email).update(gender=gender)
        if location:
            TutorRegistration.objects.filter(email=email).update(location=location)
        if language:
            TutorRegistration.objects.filter(email=email).update(language=language)
        return render(request,"t_basic_detail.html",{"account":a,"msg":"succfully updated your deatils"})
    return render(request,"t_basic_detail.html",{"account":a})

def t_photo(request,email):
    a=TutorRegistration.objects.filter(email=email).first()
    if request.method=="POST":
        profile_photo = request.FILES['profile']
        filename=f'images/{profile_photo}'
        TutorRegistration.objects.filter(email=email).update(profile_photo=profile_photo)
        TutorRegistration.objects.filter(email=email).update(filename=filename)
        a=TutorRegistration.objects.filter(email=email).first()
        return render(request,"t_photo_change.html",{"account":a,"msg":"updated ! your photo"})

    return render(request,"t_photo_change.html",{"account":a})

def t_subject(request,email):
    a=TutorRegistration.objects.filter(email=email).first()
    if request.method=="POST":
        subject = request.POST.get('subject')
        level = request.POST.get('level')
        to_level = request.POST.get('to_level')
            #two
        two_subject = request.POST.get('two_subject')
        two_level = request.POST.get('two_level')
        two_to_level = request.POST.get('to_level')
            #three
        three_subject = request.POST.get('three_subject')
        three_level = request.POST.get('three_level')
        three_to_level = request.POST.get('three_to_level')
            #four
        four_subject = request.POST.get('four_subject')
        four_level = request.POST.get('four_level')
        four_to_level = request.POST.get('four_to_level')

            #five
        five_subject = request.POST.get('five_subject')
        five_level = request.POST.get('five_level')
        five_to_level = request.POST.get('five_to_level')
       
            # Update the tutor details from the POST data
        if subject:
            TutorRegistration.objects.filter(email=email).update(subject=subject)
            TutorRegistration.objects.filter(email=email).update(from_level=level)
            TutorRegistration.objects.filter(email=email).update(to_level=to_level)
            return render(request,"t_subject.html",{"account":a,"msg":"updated ! subject of one"})
        if two_subject:
            TutorRegistration.objects.filter(email=email).update(two_subject=two_subject)
            TutorRegistration.objects.filter(email=email).update(two_from_level=two_level)
            TutorRegistration.objects.filter(email=email).update(two_to_level=two_to_level)
            return render(request,"t_subject.html",{"account":a,"msg":"updated ! subject of two"})
        if three_subject:
            TutorRegistration.objects.filter(email=email).update(three_subject=three_subject)
            TutorRegistration.objects.filter(email=email).update(three_from_level=three_level)
            TutorRegistration.objects.filter(email=email).update(three_to_level=three_to_level)
            return render(request,"t_subject.html",{"account":a,"msg":"updated ! subject of three"})
        if four_subject:
           TutorRegistration.objects.filter(email=email).update(four_subject=four_subject)
           TutorRegistration.objects.filter(email=email).update(four_from_level=four_level)
           TutorRegistration.objects.filter(email=email).update(four_to_level=four_to_level)
           return render(request,"t_subject.html",{"account":a,"msg":"updated ! subject of four"})


        if five_subject:
            TutorRegistration.objects.filter(email=email).update(five_subject=five_subject)
            TutorRegistration.objects.filter(email=email).update(five_from_level=five_level)
            TutorRegistration.objects.filter(email=email).update(five_to_level=five_to_level)
            return render(request,"t_subject.html",{"account":a,"msg":"updated ! subject of five"})

        

            
            
           

            # Save the updated details
           
        return render(request,"t_subject.html",{"account":a,"msg":"updated ! your photo"})

    return render(request,"t_subject.html",{"account":a})

def change_p(request,email):
    a = TutorRegistration.objects.filter(email=email).first()
    login={"name":a.name,"email":a.email,"password":a.password}
    html_template="email_c_p.html"
    html_message=render_to_string(html_template,login)
    email_from=settings.EMAIL_HOST_USER
    r_list=[email]
    subject="Action required: your old password form  Learnersleaf"
    message=EmailMessage(subject,html_message,email_from,r_list)
    message.content_subtype='html'
    message.send()
    return render(request,"t_contact.html",{"account":a})

from django.contrib.auth.hashers import make_password, check_password

def t_contact(request, email):
    a = TutorRegistration.objects.filter(email=email).first()
    
    if request.method == "POST":
        new_email = request.POST.get('email')
        phone = request.POST.get('phone')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        
        # Update email
        if new_email and new_email != a.email:
            TutorRegistration.objects.filter(email=email).update(email=new_email)
            a = TutorRegistration.objects.filter(email=new_email).first()  # Re-fetch the updated instance
            return render(request, "t_contact.html", {"account": a, "msg": "Updated your email!"})
        
        # Update phone number
        if phone and phone != a.phone:
            TutorRegistration.objects.filter(email=email).update(phone=phone)
            return render(request, "t_contact.html", {"account": a, "msg": "Updated your phone number!"})
        
        # Update password
        if old_password and new_password:
            # Verify the old password
            if old_password== a.password:  # Ensure you use hashed passwords
                print("hello")
                TutorRegistration.objects.filter(email=email).update(password=new_password)
                print("hello")
                return render(request, "t_contact.html", {"account": a, "msg": "Updated your password!"})
            else:
                return render(request, "t_contact.html", {"account": a, "msg": "Old password is incorrect."})
    
    return render(request, "t_contact.html", {"account": a})

def t_teaching(request,email):
    a = TutorRegistration.objects.filter(email=email).first()
    if request.method == "POST":
        i_charge = request.POST.get('i_charge')
        min_fee = request.POST.get('min_fee')
        max_fee = request.POST.get('max_fee')
        total_experience = request.POST.get('total_experience')
        teaching_experience = request.POST.get('teaching_experience')
        online_experience = request.POST.get('online_experience')
        travel = request.POST.get('travel')
        online_teach = request.POST.get('online_teach')
        homework = request.POST.get('homework')
        full_time = request.POST.get('full_time')
        interested_in = request.POST.get('interested_in')

        # Fetch the tutor record based on the email
        tutor = TutorRegistration.objects.filter(email=email).first()

        if tutor:
            # Update the tutor's details with the form data
            
            tutor.i_charge = i_charge
            tutor.min_fee = min_fee
            tutor.max_fee = max_fee
            tutor.total_experience = total_experience
            tutor.teaching_experience = teaching_experience
            tutor.online_experience = online_experience
            tutor.willing_to_travel = travel
            tutor.available_for_online_teaching = online_teach
            tutor.help_with_homework  = homework
            tutor.full_time_teacher = full_time
            tutor.interested_in = interested_in
            tutor.save()
            a = TutorRegistration.objects.filter(email=email).first()
            return render(request, "t_teaching.html", {"account": a, "msg": "update you teaching details."})

    return render(request, "t_teaching.html", {"account": a})

def t_experience(request,email):
    a = TutorRegistration.objects.filter(email=email).first()
    if request.method=="POST":
          company_name=request.POST.get('company_name')
          job_roll=request.POST.get('job_roll')
          start_date=request.POST.get('start_date')
          end_date=request.POST.get('end_date')
          job_description=request.POST.get('job_description')

          tutor = TutorRegistration.objects.filter(email=email).first()
          tutor.company_name=company_name
          tutor.job_roll=job_roll
          tutor.job_start_date=start_date
          if end_date:
              tutor.job_end_date=end_date
          tutor.save()
          a = TutorRegistration.objects.filter(email=email).first()
          return render(request, "t_experience.html", {"account": a, "msg": "update you teaching details."})
    return render(request, "t_experience.html", {"account": a})
from django.db.models import Q  

# job search
def search_job(request):
  
    if request.method=="POST":
        subject=request.POST.get('subject')
        location=request.POST.get('location')
        if Requestpost.objects.filter( Q(subject=subject) | Q(two_subject=subject) | Q(three_subject=subject) | Q(four_subject=subject) | Q(five_subject=subject),location=location).exists():
          
            tutors = Requestpost.objects.filter( Q(subject=subject) | Q(two_subject=subject) | Q(three_subject=subject) | Q(four_subject=subject) | Q(five_subject=subject),location=location).values()
           
        elif Requestpost.objects.filter( Q(subject=subject) | Q(two_subject=subject) | Q(three_subject=subject) | Q(four_subject=subject) | Q(five_subject=subject)).exists():
            tutors=Requestpost.objects.filter( Q(subject=subject) | Q(two_subject=subject) | Q(three_subject=subject) | Q(four_subject=subject) | Q(five_subject=subject)).values()
        elif Requestpost.objects.filter(location=location).exists():
            tutors=Requestpost.objects.filter(location=location).values()
        d={"tutors":tutors}
        return render(request,"tutors_job.html",{"all":tutors})
    all_tutor=TutorRegistration.objects.all()
    return render(request,"tutors_job.html",{"all":all_tutor})

def tutors_job(request,email):
    a = TutorRegistration.objects.filter(email=email).first()
    all=Requestpost.objects.all()
    return render(request,"tutors_job.html",{"all":all,"account":a,"t":"All Job"})
def tutors_online_job(request,email):
    a = TutorRegistration.objects.filter(email=email).first()
    all=Requestpost.objects.all()
    return render(request,"tutors_job.html",{"all":all,"account":a,"t":"Online Job"})

def h_all_teachers(request ):
    l=[
                "Chennai, Tamil Nadu", "Coimbatore, Tamil Nadu", "Madurai, Tamil Nadu", "Salem, Tamil Nadu",
                "Tiruchirappalli, Tamil Nadu", "Tirunelveli, Tamil Nadu", "Vellore, Tamil Nadu", "Erode, Tamil Nadu",
                "Kanchipuram, Tamil Nadu", "Thanjavur, Tamil Nadu", "Tiruppur, Tamil Nadu", "Nagapattinam, Tamil Nadu",
                "Kumbakonam, Tamil Nadu", "Dharmapuri, Tamil Nadu", "Karur, Tamil Nadu", "Sivakasi, Tamil Nadu",
                "Dindigul, Tamil Nadu", "Ramanathapuram, Tamil Nadu", "Tuticorin, Tamil Nadu", "Cuddalore, Tamil Nadu",
                "Vellore, Tamil Nadu", "Ariyalur, Tamil Nadu", "Perambalur, Tamil Nadu", "Nagercoil, Tamil Nadu",
                "Theni, Tamil Nadu", "Kodaikanal, Tamil Nadu", "Pollachi, Tamil Nadu", "Pudukkottai, Tamil Nadu",
                "Tiruvallur, Tamil Nadu", "Tiruvannamalai, Tamil Nadu", "Chengalpattu, Tamil Nadu", "Tirupathur, Tamil Nadu",
                "Sankarankovil, Tamil Nadu", "Kovilpatti, Tamil Nadu", "Manapparai, Tamil Nadu", "Thiruthuraipoondi, Tamil Nadu",
                "Ramanathapuram, Tamil Nadu"
            ]
    
    
    all_tutor=TutorRegistration.objects.all()
    
    return render(request,"h_all_teacher.html",{"tutors":all_tutor,"locations":l,"heading":"All Tutors"})

def h_online_tutor(request):
    l=[
                "Chennai, Tamil Nadu", "Coimbatore, Tamil Nadu", "Madurai, Tamil Nadu", "Salem, Tamil Nadu",
                "Tiruchirappalli, Tamil Nadu", "Tirunelveli, Tamil Nadu", "Vellore, Tamil Nadu", "Erode, Tamil Nadu",
                "Kanchipuram, Tamil Nadu", "Thanjavur, Tamil Nadu", "Tiruppur, Tamil Nadu", "Nagapattinam, Tamil Nadu",
                "Kumbakonam, Tamil Nadu", "Dharmapuri, Tamil Nadu", "Karur, Tamil Nadu", "Sivakasi, Tamil Nadu",
                "Dindigul, Tamil Nadu", "Ramanathapuram, Tamil Nadu", "Tuticorin, Tamil Nadu", "Cuddalore, Tamil Nadu",
                "Vellore, Tamil Nadu", "Ariyalur, Tamil Nadu", "Perambalur, Tamil Nadu", "Nagercoil, Tamil Nadu",
                "Theni, Tamil Nadu", "Kodaikanal, Tamil Nadu", "Pollachi, Tamil Nadu", "Pudukkottai, Tamil Nadu",
                "Tiruvallur, Tamil Nadu", "Tiruvannamalai, Tamil Nadu", "Chengalpattu, Tamil Nadu", "Tirupathur, Tamil Nadu",
                "Sankarankovil, Tamil Nadu", "Kovilpatti, Tamil Nadu", "Manapparai, Tamil Nadu", "Thiruthuraipoondi, Tamil Nadu",
                "Ramanathapuram, Tamil Nadu"
            ]
    all_tutor=TutorRegistration.objects.filter(available_for_online_teaching="yes")
    
    return render(request,"h_all_teacher.html",{"tutors":all_tutor,"locations":l,"heading":"Online Tutors"})

def h_home_tutor(request):
    l=[
                "Chennai, Tamil Nadu", "Coimbatore, Tamil Nadu", "Madurai, Tamil Nadu", "Salem, Tamil Nadu",
                "Tiruchirappalli, Tamil Nadu", "Tirunelveli, Tamil Nadu", "Vellore, Tamil Nadu", "Erode, Tamil Nadu",
                "Kanchipuram, Tamil Nadu", "Thanjavur, Tamil Nadu", "Tiruppur, Tamil Nadu", "Nagapattinam, Tamil Nadu",
                "Kumbakonam, Tamil Nadu", "Dharmapuri, Tamil Nadu", "Karur, Tamil Nadu", "Sivakasi, Tamil Nadu",
                "Dindigul, Tamil Nadu", "Ramanathapuram, Tamil Nadu", "Tuticorin, Tamil Nadu", "Cuddalore, Tamil Nadu",
                "Vellore, Tamil Nadu", "Ariyalur, Tamil Nadu", "Perambalur, Tamil Nadu", "Nagercoil, Tamil Nadu",
                "Theni, Tamil Nadu", "Kodaikanal, Tamil Nadu", "Pollachi, Tamil Nadu", "Pudukkottai, Tamil Nadu",
                "Tiruvallur, Tamil Nadu", "Tiruvannamalai, Tamil Nadu", "Chengalpattu, Tamil Nadu", "Tirupathur, Tamil Nadu",
                "Sankarankovil, Tamil Nadu", "Kovilpatti, Tamil Nadu", "Manapparai, Tamil Nadu", "Thiruthuraipoondi, Tamil Nadu",
                "Ramanathapuram, Tamil Nadu"
            ]
   
    all_tutor=TutorRegistration.objects.filter(willing_to_travel="yes")
    return render(request,"h_all_teacher.html",{"tutors":all_tutor,"locations":l,"heading":"Home Tutors"})


def h_fliter_location(request,location):
    l=[
                "Chennai, Tamil Nadu", "Coimbatore, Tamil Nadu", "Madurai, Tamil Nadu", "Salem, Tamil Nadu",
                "Tiruchirappalli, Tamil Nadu", "Tirunelveli, Tamil Nadu", "Vellore, Tamil Nadu", "Erode, Tamil Nadu",
                "Kanchipuram, Tamil Nadu", "Thanjavur, Tamil Nadu", "Tiruppur, Tamil Nadu", "Nagapattinam, Tamil Nadu",
                "Kumbakonam, Tamil Nadu", "Dharmapuri, Tamil Nadu", "Karur, Tamil Nadu", "Sivakasi, Tamil Nadu",
                "Dindigul, Tamil Nadu", "Ramanathapuram, Tamil Nadu", "Tuticorin, Tamil Nadu", "Cuddalore, Tamil Nadu",
                "Vellore, Tamil Nadu", "Ariyalur, Tamil Nadu", "Perambalur, Tamil Nadu", "Nagercoil, Tamil Nadu",
                "Theni, Tamil Nadu", "Kodaikanal, Tamil Nadu", "Pollachi, Tamil Nadu", "Pudukkottai, Tamil Nadu",
                "Tiruvallur, Tamil Nadu", "Tiruvannamalai, Tamil Nadu", "Chengalpattu, Tamil Nadu", "Tirupathur, Tamil Nadu",
                "Sankarankovil, Tamil Nadu", "Kovilpatti, Tamil Nadu", "Manapparai, Tamil Nadu", "Thiruthuraipoondi, Tamil Nadu",
                "Ramanathapuram, Tamil Nadu"
            ]
    decoded_once = unquote(location)  # First level of decoding
    decoded_twice = unquote(decoded_once)   # Second level of decoding
    
    print(decoded_twice)
    if TutorRegistration.objects.filter(location=decoded_twice).exists():
        tutors=TutorRegistration.objects.filter(location=decoded_twice).values()
    else:
        tutors=TutorRegistration.objects.all().values()
    return render(request,"h_all_teacher.html",{"tutors":tutors,"locations":l,"heading":location})
 

def h_tutors_job(request):
  
    all=Requestpost.objects.all()
    return render(request,"h_job.html",{"all":all,"t":"All Job"})

def h_online_job(request):
    
    all=Requestpost.objects.filter(meeting_option="online").values
    return render(request,"h_job.html",{"all":all,"t":"Online Job"})

def h_home_job(request):
    
    all=Requestpost.objects.filter(meeting_option="my_place").values
    return render(request,"h_job.html",{"all":all,"t":"Home Teaching"})
def h_search_teacher(request):
    l=[
                "Chennai, Tamil Nadu", "Coimbatore, Tamil Nadu", "Madurai, Tamil Nadu", "Salem, Tamil Nadu",
                "Tiruchirappalli, Tamil Nadu", "Tirunelveli, Tamil Nadu", "Vellore, Tamil Nadu", "Erode, Tamil Nadu",
                "Kanchipuram, Tamil Nadu", "Thanjavur, Tamil Nadu", "Tiruppur, Tamil Nadu", "Nagapattinam, Tamil Nadu",
                "Kumbakonam, Tamil Nadu", "Dharmapuri, Tamil Nadu", "Karur, Tamil Nadu", "Sivakasi, Tamil Nadu",
                "Dindigul, Tamil Nadu", "Ramanathapuram, Tamil Nadu", "Tuticorin, Tamil Nadu", "Cuddalore, Tamil Nadu",
                "Vellore, Tamil Nadu", "Ariyalur, Tamil Nadu", "Perambalur, Tamil Nadu", "Nagercoil, Tamil Nadu",
                "Theni, Tamil Nadu", "Kodaikanal, Tamil Nadu", "Pollachi, Tamil Nadu", "Pudukkottai, Tamil Nadu",
                "Tiruvallur, Tamil Nadu", "Tiruvannamalai, Tamil Nadu", "Chengalpattu, Tamil Nadu", "Tirupathur, Tamil Nadu",
                "Sankarankovil, Tamil Nadu", "Kovilpatti, Tamil Nadu", "Manapparai, Tamil Nadu", "Thiruthuraipoondi, Tamil Nadu",
                "Ramanathapuram, Tamil Nadu"
            ]
    if request.method=="POST":
        subject=request.POST.get('subject')
        location=request.POST.get('location')
        if TutorRegistration.objects.filter(subject=subject,location=location).exists():
          
            tutors = TutorRegistration.objects.filter(subject=subject,location=location).values()
           
        elif TutorRegistration.objects.filter(subject=subject).exists():
            tutors=TutorRegistration.objects.filter(subject=subject).values()
        elif TutorRegistration.objects.filter(location=location).exists():
            tutors=TutorRegistration.objects.filter(location=location).values()
        d={"tutors":tutors,"locations":l}
        return render(request,"h_all_teacher.html",d)
    all_tutor=TutorRegistration.objects.all()
    return render(request,"h_all_teacher.html",{"tutors":all_tutor,"locations":l})

def  buy_coin_stu(request,email,coins):
    c=TutorRequest.objects.filter(email=email).first()
    print(c.coin)
    if c.coin:
        c.coin=c.coin+coins
        c.save()
    else:
        c.coin=coins
        c.save()
    return render(request,"s_wallet.html",{"account":c,"msg":"coins where add"})
   
def  s_wallet(request,email):
    c=TutorRequest.objects.filter(email=email).first()
    return render(request,"s_wallet.html",{"account":c})


def  t_wallet(request,email):
    c=TutorRegistration.objects.filter(email=email).first()

    return render(request,"t_wallet.html",{"account":c})
def  buy_coin_teach(request,email,coins):
    print(coins)
   
    c=TutorRegistration.objects.filter(email=email).first()
    if c.coin:
        c.coin=c.coin+coins
        c.save()
    else:
        c.coin=coins
        c.save()

    
    return render(request,"t_wallet.html",{"account":c,"msg":"coins where add"})

def view_post_teach(request,a_email,email,id):
    print(email)
    if teacher_addcard.objects.filter(email=a_email,cid=id).exists():
        s=TutorRequest.objects.filter(email=email).first()
        sp=Requestpost.objects.get(id=id)
        c=TutorRegistration.objects.filter(email=a_email).first()
        d={"s":s,"sp":sp,"account":c}
        return render(request,"v_full_student_post.html",d)
    else:
        s=TutorRequest.objects.filter(email=email).first()
        sp=Requestpost.objects.get(id=id)
        c=TutorRegistration.objects.filter(email=a_email).first()
        d={"s":s,"sp":sp,"account":c}
       
        return render(request,"v_student_post.html",d)
def use_coin_teach(request,a_email,email,id):
    c=TutorRegistration.objects.filter(email=a_email).first()
    print(c.coin)
    if c.coin:
        print(c.coin)
        if c.coin>=100:
            c.coin=c.coin-100
            c.save()
            teacher_addcard.objects.create(email=a_email,cid=id)
            s=TutorRequest.objects.filter(email=email).first()
            sp=Requestpost.objects.get(id=id)
            c=TutorRegistration.objects.filter(email=a_email).first()
            d={"s":s,"sp":sp,"account":c}
            return render(request,"v_full_student_post.html",d)
        else:
            c=TutorRegistration.objects.filter(email=a_email).first()
            return render(request,"t_wallet.html",{"account":c,"msg":"your as Insufficient Balance coin  so! buy coin "})
        
    else:
      c=TutorRegistration.objects.filter(email=a_email).first()
      return render(request,"t_wallet.html",{"account":c,"msg":"your as Insufficient Balance coin  so! buy coin "})
    
def t_message_to(request,s_email,r_email):
    teacher=TutorRegistration.objects.filter(email=s_email).first()
    if request.method=="POST":
        subject=request.POST.get('subject')
        message =request.POST.get('message')
        receiver_email=r_email
        sender_email=s_email
        Message.objects.create(sender_name=teacher.name,sender_email=sender_email,receiver_email=receiver_email,subject=subject,body=message)

        return render(request,"message.html",{"msg":"message is sented","name":teacher.name,"account":teacher})


        
    
    return render(request,"message.html",{"name":teacher.name,"s_email":s_email,"r_email":r_email, "account":teacher})   

def  teacher_inbox(request,email):
    c=TutorRegistration.objects.filter(email=email).first()
    if Message.objects.filter( receiver_email=email).exists():
        sm=Message.objects.filter( receiver_email=email).values

     
        return render(request,"t_inbox.html",{"msg":sm,"account":c})
    
    return render(request,"t_inbox.html",{"account":c})

def student_update(request,email,id):
    post = Requestpost.objects.get(id=id)
    student = TutorRequest.objects.filter(email=email).first()
    if request.method=="POST":
        dyr = request.POST.get("dyr")
        level = request.POST.get("level")
        subject = request.POST.get("subject")
        two_subject = request.POST.get("two_subject")
        three_subject = request.POST.get("three_subject")
        i_want = request.POST.get("i_want")
        meeting_option= request.POST.get("meeting_option")
        budget = request.POST.get("budget")
        budget_need = request.POST.get("budget_need")
        
        language = request.POST.get("language")
        tutor_want = request.POST.get("tutor_want")
        need = request.POST.get("need")
        message = request.POST.get("message")
        gender = request.POST.get("gender")
        l=TutorRequest.objects.filter(email=email).first()
        r=Requestpost.objects.filter(id=id).update(
            email=email,
            dyr=dyr,
            level=level,
            subject=subject,
            two_subject=two_subject,
            three_subject=three_subject,
            i_want=i_want,
            meeting_option=meeting_option,
         
            budget=budget,
            budget_need=budget_need,
            gender=gender,
            language=language,
            tutor_want=tutor_want,
            need=need,
            message=message,
            location=l.location
            )
 
        post = Requestpost.objects.filter(email=email).values
        student = TutorRequest.objects.filter(email=email).first()
        return render(request,"mypost.html",{"all":post,"post":student,"msg":"updated values"})

    return render(request,"stu_edit.html",{"all":post,"post":student})


def s_myprofile(request,email,s_email):
    tutor = TutorRegistration.objects.filter(email=email).values()
    first=TutorRegistration.objects.filter(email=email).first()
    p={"all":tutor,"name":first.name,"roll":first.job_roll,"first":first,"s_email":s_email}
    return render(request,"myprofile.html",p)

def view_message_stu(request,a_email,email,id):
    print(email)
    c=TutorRequest.objects.filter(email=a_email).first()
    if  student_addcard.objects.filter(email=a_email,cid=id).exists():
       return redirect('t_message_to', s_email=a_email, r_email=email)
  
    elif c.coin:
        print(c.coin)
        if c.coin>=100:
            c.coin=c.coin-100
            c.save()
            student_addcard.objects.create(email=a_email,cid=id)
            return redirect('t_message_to', s_email=a_email, r_email=email)

    else:
        c=TutorRequest.objects.filter(email=a_email).first()
        return render(request,"s_wallet.html",{"account":c})
def view_contant_stu(request,a_email,email,id):
    print(email)
    c=TutorRequest.objects.filter(email=a_email).first()
    if  student_addcard.objects.filter(email=a_email,cid=id).exists():
        tutor = TutorRegistration.objects.filter(email=email).values()
        first=TutorRegistration.objects.filter(email=email).first()
        p={"all":tutor,"name":first.name,"roll":first.job_roll,"first":first,"s_email":a_email,"phone":first.phone,"email":first.email}
        return render(request,"myprofile.html",p)
  
    elif c.coin:
        print(c.coin)
        if c.coin>=100:
            c.coin=c.coin-100
            c.save()
            student_addcard.objects.create(email=a_email,cid=id)
            tutor = TutorRegistration.objects.filter(email=email).values()
            first=TutorRegistration.objects.filter(email=email).first()
            p={"all":tutor,"name":first.name,"roll":first.job_roll,"first":first,"s_email":a_email,"phone":first.phone,"email":first.email}
            return render(request,"myprofile.html",p)
    else:
        c=TutorRequest.objects.filter(email=a_email).first()
        return render(request,"s_wallet.html",{"account":c})
    

def home(request):
    return render(request,"home.html")
    


      

      












    
    






       


    


                           





    
 

    

    





          


    













    
