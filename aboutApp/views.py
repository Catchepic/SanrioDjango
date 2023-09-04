from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Store
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404


def survey(request):
    return render(request, 'survey.html', {'active_menu': 'survey', 'sub_menu': 'nav-survey'})


def idea(request):
    return render(request, 'idea.html ', {'active_menu': 'idea', 'sub_menu': 'nav-idea'})


def storeDetail(request, id):
    """
    产品详情页
    :param request:
    :param id:
    :return:
    """
    store = get_object_or_404(Store, id=id)
    store.views += 1
    store.save()
    return render(request, 'storeDetail.html', {
        'active_menu': 'stores',
        'store': store,  # 传递给前端的模板变量
    })


# Path: productsApp\urls.py
def stores(request):
    """
    产品列表页
    :param request:
    :param storeName:
    :return:
    """
    submenu = 'nav-limit'
    storeList = Store.objects.all().filter()
    p = Paginator(storeList, 2)  # 过滤好的数据，每页显示两条
    if p.num_pages <= 1:
        pageData = ''  # 向前端传递空串
    else:
        page = int(request.GET.get('page', 1))  # 前端页码超链接 传过来的具体页码
        storeList = p.page(page)  # 具体页码要显示的两条记录
        left = []  # 列表
        right = []
        left_has_more = False
        right_has_more = False
        first = False
        last = False
        total_pages = p.num_pages  # 总页数
        page_range = p.page_range  # 页数范围
        if page == 1:
            right = page_range[page:page + 2]  # 列表 right[0]=2 right[1]=3
            print(total_pages)
            if right[-1] < total_pages - 1:  # right[-1]为3
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        elif page == total_pages:
            left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]  # 倒数第3页，倒数第2页
            if left[0] > 2:  # 倒数第3页页码大于2
                left_has_more = True
            if left[0] > 1:
                first = True
        else:  # 不是第一页或最后一页
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
        pageData = {  # 字典，会传给前端
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
            'total_pages': total_pages,
            'page': page,
        }
    return render(request, 'limit.html', {
        'active_menu': 'limit',
        'storeList': storeList,  # 给四个模板变量传值
        'pageData': pageData,
        'sub_menu': submenu
    })


def contact(request):
    return render(request, 'contact.html.', {'active_menu': 'contact', 'sub_menu': 'nav-contact'})
