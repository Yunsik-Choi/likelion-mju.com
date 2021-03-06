from django.shortcuts import render
from page.models import Application

# Create your views here.
def home(request):
    return render(request, 'home.html')

def apply(request):
    if request.method == 'POST':
        application = Application.objects.filter(user=request.user)
        if not application:
            application = Application()
        else:
            application = Application.objects.get(user=request.user)
        application.user = request.user
        application.field = request.POST['field']
        application.answers = {
            'answer1': request.POST['answer1'],
            'answer2': request.POST['answer2'],
            'answer3': request.POST['answer3'],
            'answer4': request.POST['answer4']
        }
        if 'portfolio' in request.FILES:
            application.portfolio = request.FILES['portfolio']
        application.date = request.POST['date']

        if 'btn' in request.POST:
            application.is_submit = False
            application.save()
            return render(request, 'home.html', {"message": "지원서가 임시저장되었습니다. 꼭 지원기간 내에 제출해주세요!"})

        application.is_submit = True
        application.save()
        return render(request, 'complete.html')
    else:
        try:
            application = request.user.application
            if application.is_submit == True:
                return render(request, 'home.html', {"message": "지원서 제출이 완료되었습니다."})

            return render(request, 'apply.html', {
                'field': application.field,
                'answer1': application.answers['answer1'],
                'answer2': application.answers['answer2'],
                'answer3': application.answers['answer3'],
                'answer4': application.answers['answer4'],
                'portfolio': application.portfolio,
                'date': application.date
            })
        except Application.DoesNotExist:
            return render(request, 'apply.html')

def complete(request):
    return render(request, 'complete.html')

def list(request):
    if request.user.is_superuser:
        applications = Application.objects.all()
        return render(request, 'apply_list.html', {'applications':applications})

def list_opt(request, opt):
    if request.user.is_superuser:
        applications = Application.objects.all()
        if opt == "save":
            applications = applications.filter(is_submit=False)
        elif opt == "submit":
            applications = applications.filter(is_submit=True)
        return render(request, 'apply_list.html', {'applications':applications})

def detail(request, id):
    if request.user.is_superuser:
        application = Application.objects.get(pk=id)
        return render(request, 'apply.html', {
                'mode': 'admin',
                'user': application.user,
                'field': application.field,
                'answer1': application.answers['answer1'],
                'answer2': application.answers['answer2'],
                'answer3': application.answers['answer3'],
                'answer4': application.answers['answer4'],
                'portfolio': application.portfolio,
                'date': application.date
            })

def intro(request):
    return render(request, 'intro.html')