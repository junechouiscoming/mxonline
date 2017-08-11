from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import render_to_response
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CourseOrg, CityDict

class OrgView(View):
    def get(self, request):
        # 取出课程机构和城市 数据
        all_org = CourseOrg.objects.all()
        org_nums = all_org.count()
        all_city = CityDict.objects.all()

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        objects = ['john', 'edward', 'josh', 'frank']
        p = Paginator(all_org, 5, request=request)
        orgs = p.page(page)

        return render(request, 'org-list.html', {
            'all_org': orgs,
            'all_city': all_city,
            'org_nums': org_nums,
        })