from django import forms
from .models import Resume


class ResumeForm(forms.ModelForm):  # 建立模型表单类
    class Meta:  # 通过元信息类进行模型的定制化
        """
        通过元信息类进行模型的定制化
        """
        model = Resume  # 需要定制化的模型
        fields = ('name', 'character', 'storeName', 'storeInfo', 'bossName', 'bossNum', 'email',
                  'experience', 'position')  # 需要定制化的字段

