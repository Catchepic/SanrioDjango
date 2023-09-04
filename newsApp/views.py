# Create your views here.
from django.shortcuts import render
from .models import MyNew  # 新闻表
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from pyquery import PyQuery as pq


# Create your views here.
def news(request, newName):
    submenu = newName  # 侧边导航栏的激活状态
    if newName == 'company':
        newName = '企业要闻'
    elif newName == 'industry':
        newName = '角色新闻'
    else:
        newName = '通知公告'

    newList = MyNew.objects.all().filter(
        newType=newName).order_by('-publishDate')
    for mynew in newList:
        html = pq(mynew.description)  # 使用pq方法解析html内容
        mynew.mytxt = pq(html)('p').text()  # 截取html段落文字
    p = Paginator(newList, 5)  # 过滤好的数据，每页显示5条
    if p.num_pages <= 1:
        pageData = ''  # 向前端传递空串
    else:
        page = int(request.GET.get('page', 1))  # 前端页码超链接 传过来的具体页码
        newList = p.page(page)  # 具体页码要显示的5条记录
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

    return render(request, 'newList.html', {
        'active_menu': 'news',  # base.html新闻动态所在li的id号为news
        'sub_menu': submenu,
        'newName': newName,
        'newList': newList,
        'pageData': pageData,

    })


def newDetail(request, id):
    mynew = get_object_or_404(MyNew, id=id)  # 从MyNew表中获取指定id号的新闻
    mynew.views += 1
    mynew.save()
    return render(request, 'newDetail.html', {
        'active_menu': 'news',
        'mynew': mynew,  # 传递给前端的模板变量
    })


def search(request):
    keyword = request.GET.get('keyword')
    newList = MyNew.objects.filter(title__icontains=keyword)  # 标题中包含指定关键字
    newName = "关于" + "\"" + keyword + "\"" + "的搜索结果"
    return render(request, 'searchList.html', {
        'active_menu': 'news',
        'newName': newName,
        'newList': newList,
    })
