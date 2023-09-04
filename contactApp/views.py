from django.shortcuts import render
from .models import Ad
from .forms import ResumeForm


# Create your views here.

def recruit(request):
    """
    加入恒达
    :param request:
    :return:
    """
    AdList = Ad.objects.all().order_by('-publishDate')
    if request.method == 'POST':
        resumeForm = ResumeForm(data=request.POST, files=request.FILES)  # 创建模型表单对象
        if resumeForm.is_valid():
            resumeForm.save()  # 存到数据库
            return render(request, 'success.html', {  # 提交了简历，进入success页面
                'active_menu': 'contactus',
                'sub_menu': 'recruit',
            })
    else:  # 没有提交
        resumeForm = ResumeForm()  # 创建模型表单对象，并传给recruit.html
    return render(
        request, 'recruit.html', {
            'active_menu': 'contactus',
            'sub_menu': 'recruit',
            'AdList': AdList,
            'resumeForm': resumeForm,
        })
