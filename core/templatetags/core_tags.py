from django import template
from django.conf import settings
from qorder.models import *


register = template.Library()
from core.models import EmserUser, Page


@register.simple_tag
def simple_tag(value):
    pass

@register.filter
def if_page_by_user(user, values):
    try:
        u = EmserUser.objects.get(username=user)
        if u.is_admin:
            return True
        pages_enabled = u.get_my_pages()
        print(pages_enabled)
        pages = values.split('~')
        print(pages)
        if len(pages)==1:
            page = Page.objects.get(page=pages[0])
            return page in pages_enabled
        else:
            ret = False

            for p in pages:
                try:
                    page = Page.objects.get(page=p)
                    if page in pages_enabled:
                        #print('page: '+str(page))
                        ret = True
                        break
                except Exception as e:
                    print('error' + str(e))
                    #print(p)       
            #print(ret)        
            return ret
    except Exception as e:

        print(e)
        #print('error')
        return False


@register.assignment_tag
def assignment_tag(user, values):
    pass
