from django.shortcuts import render

# Create your views here.
from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.template.defaultfilters import default

from .models import Doc
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.http import StreamingHttpResponse  # 用于将文件流发送给浏览器
import base64

import urllib  # url解析
import json  # json字符串使用
import os  # 执行操作系统命令
from django.views.decorators.csrf import csrf_exempt  # 跨站点验证
from django.http import JsonResponse  # json字符串响应

def survey(request):
    return render(request, 'product.html')


def honor(request):
    return render(request, 'productDetail.html')


def melody(request):
    return render(request, 'Melody.html')

def read_file(file_name, size):
    """

    :param file_name:
    :param size:
    """
    with open(file_name, mode='rb') as fp:
        while True:
            c = fp.read(size)
            if c:
                yield c
            else:
                break


def getDoc(request, id):
    """

    :param request:
    :param id:
    :return:
    """
    doc = get_object_or_404(Doc, id=id)
    update_to, filename = str(doc.file).split('/')
    filepath = '%s/media/%s/%s' % (os.getcwd(), update_to, filename)
    response = StreamingHttpResponse(read_file(filepath, 512))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{}"'.format(
        filename)
    return response

def download(request):
    """
    :param request:
    :return:
    """
    submenu = 'download'
    docList = Doc.objects.all().order_by('-publishDate')
    p = Paginator(docList, 3)
    if p.num_pages <= 1:
        pageData = ''
    else:
        page = int(request.GET.get('page', 1))
        docList = p.page(page)  # 那一页的数据
        left = []
        right = []
        left_has_more = False
        right_has_more = False
        first = False
        last = False
        total_pages = p.num_pages
        page_range = p.page_range
        if page == 1:
            right = page_range[page:page + 2]
            print(total_pages)
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        elif page == total_pages:
            left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        else:
            left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]
            right = page_range[page:page + 2]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        pageData = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
            'total_pages': total_pages,
            'page': page,
        }
    return render(
        request, 'docList.html', {
            'active_menu': 'service',
            'sub_menu': submenu,
            'docList': docList,
            'pageData': pageData,
        })
