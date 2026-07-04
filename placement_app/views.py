from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from .models import Resume, Job
from django.contrib.auth import logout
from django.http import JsonResponse
import fitz


def home(request):
    return render(request, "home.html")

def register(request):

    if request.method == "POST":

        fullname = request.POST["fullname"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered.Please Login")
            return redirect("login")

        User.objects.create_user(
            username=email,
            first_name=fullname,
            email=email,
            password=password
        )

        messages.success(request, "Registration successful. Please login.")
        return redirect("login")

    return render(request, "register.html")

def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        # username=email என்று மாற்றவும்
        user = authenticate(request, username=email, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            # இவை சரியாக இடதுபுறம் தள்ளி இருக்க வேண்டும்
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")

@login_required
def dashboard(request):
    return render(request, "dashboard.html")


@login_required
def profile(request):
    return render(request, "profile.html")

@login_required
def resume(request):

    analysis = None

    if request.method == "POST":

        resume_file = request.FILES.get("resume")

        resume_text = ""

        if resume_file:

            pdf = fitz.open(stream=resume_file.read(), filetype="pdf")

            for page in pdf:
                resume_text += page.get_text()

            pdf.close()

            Resume.objects.create(
                user=request.user,
                resume=resume_file
            )

            score = 0
            skills = []

            keywords = [
                "python",
                "django",
                "sql",
                "html",
                "css",
                "javascript",
                "java",
                "communication"
            ]

            for word in keywords:
                if word.lower() in resume_text.lower():
                    skills.append(word)
                    score += 12

            if score > 100:
                score = 100

            analysis = {
                "score": score,
                "skills": skills,
            }

            messages.success(request, "Resume uploaded successfully!")

    return render(
        request,
        "resume.html",
        {"analysis": analysis}
    )

@login_required
def analyzer(request):

    analysis = None

    if request.method == "POST":

        skills = request.POST.get("skills", "").lower()

        score = 0
        suggestions = []

        if "python" in skills:
            score += 20
        else:
            suggestions.append("Add Python skill.")

        if "django" in skills:
            score += 20
        else:
            suggestions.append("Add Django skill.")

        if "sql" in skills:
            score += 20
        else:
            suggestions.append("Add SQL skill.")

        if "html" in skills:
            score += 20
        else:
            suggestions.append("Add HTML/CSS skill.")

        if "communication" in skills:
            score += 20
        else:
            suggestions.append("Improve Communication Skills.")

        analysis = {
            "score": score,
            "suggestions": suggestions,
        }

    return render(
        request,
        "analyzer.html",
        {"analysis": analysis}
    )

@login_required
def career(request):

    career = None

    if request.method == "POST":

        interest = request.POST.get("interest")

        recommendations = {

            "AI": {
                "career": "Machine Learning Engineer",
                "skills": "Python, TensorFlow, Deep Learning",
                "companies": "Google, Microsoft, OpenAI"
            },

            "Web": {
                "career": "Full Stack Developer",
                "skills": "HTML, CSS, JavaScript, Django",
                "companies": "TCS, Infosys, Zoho"
            },

            "Cyber": {
                "career": "Cyber Security Analyst",
                "skills": "Networking, Linux, Ethical Hacking",
                "companies": "IBM, Accenture, Deloitte"
            },

            "Cloud": {
                "career": "Cloud Engineer",
                "skills": "AWS, Azure, Docker",
                "companies": "Amazon, Google Cloud, Oracle"
            },

            "Data": {
                "career": "Data Scientist",
                "skills": "Python, SQL, Pandas, Machine Learning",
                "companies": "Amazon, Flipkart, TCS"
            },
        }

        career = recommendations.get(interest)

    return render(
        request,
        "career.html",
        {"career": career}
    )

@login_required
def prediction(request):

    result = None

    if request.method == "POST":

        cgpa = float(request.POST.get("cgpa"))
        communication = request.POST.get("communication")

        if cgpa >= 8.5 and communication == "Excellent":
            result = "🎉 Excellent! You have a High Placement Chance."

        elif cgpa >= 7.0:
            result = "👍 Good! You have a Moderate Placement Chance."

        else:
            result = "📚 Improve your skills, projects, and communication to increase your placement chances."

    return render(request, "prediction.html", {"result": result})

@login_required
def interview(request):
    return render(request, "interview.html")

@login_required
def logout_view(request):
    logout(request)
    return redirect("home")

@login_required
def assessment(request):

    score = None

    if request.method == "POST":

        score = 0

        if request.POST.get("q1") == "b":
            score += 1

        if request.POST.get("q2") == "a":
            score += 1

        if request.POST.get("q3") == "c":
            score += 1

    return render(
        request,
        "assessment.html",
        {"score": score}
    )

@login_required
def reports(request):
    return render(request, "reports.html")

def api_jobs(request):

    jobs = Job.objects.all()

    data = []

    for job in jobs:
        data.append({
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "apply_link": job.apply_link,
        })

    return JsonResponse(data, safe=False)

def jobs(request):
    jobs_data = [
        {
            "title": "Python Developer",
            "company": "Infosys",
            "location": "Chennai",
            "apply_link": "https://www.linkedin.com/jobs/"
        },
        {
            "title": "Java Developer",
            "company": "Wipro",
            "location": "Bengaluru",
            "apply_link": "https://careers.wipro.com/"
        },
        {
            "title": "Frontend Developer",
            "company": "TCS",
            "location": "Hyderabad",
            "apply_link": "https://www.tcs.com/careers"
        }
    ]

    return render(request, "jobs.html", {"jobs": jobs_data})