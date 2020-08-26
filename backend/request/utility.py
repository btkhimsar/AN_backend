from Constants.image_urls import HOME_ICON
from category.models import Category, SuperCategory
from users.models import User

def create_point_dict(latitude, longitude):
    point = {'type': 'Point', 'coordinates': [latitude, longitude]}
    return point

def request_json_for_myrequests(request):
    request_data = {}
    user = User.objects.get(id=request.user_id)
    language = user.user_language
    category = Category.objects.get(id=request.category_id)
    super_category = SuperCategory.objects.get(id=request.super_category_id)
    if language=='english':
        request_data['title'] = "You requested for"
    elif language=='hindi':
        request_data['title'] ='आपने निवेदन किया'
    request_data['subtitle'] = '{} > {}'.format(super_category.name[language], category.name[language])
    request_data['isCompleted'] = request.isCompleted
    request_data['request_id'] = str(request.id)
    return request_data

def request_json_for_workrequests(request):
    request_data = {}
    user = User.objects.get(id=request.user_id)
    request_data['title'] = 'Request from {}'.format(user.name)
    request_data['subtitle'] = request.location_name
    request_data['subtitle_icon'] = HOME_ICON
    request_data['mobile'] = request.mobile
    request_data['type'] = 'request'
    request_data['request_id'] = str(request.id)
    return request_data


def header_for_today(ret, language):
    if language=='english':
        ret.append({'title': 'Today', 'type': 'header'})
    elif language=='hindi':
        ret.append({'title': 'आज', 'type': 'header'})

def footer_for_today(ret, language):
    if language=='english':
        ret.append({'title': '120 other requests already completed', 'type': 'footer'})
    elif language=='hindi':
        ret.append({'title': '120 अन्य अनुरोध पहले ही पूरे हो चुके हैं', 'type': 'footer'})

def header_for_1dayago(ret, language):
    if language=='english':
        ret.append({'title': '1 day ago', 'type': 'header'})
    elif language=='hindi':
        ret.append({'title': '1 दिन पहले', 'type': 'header'})

def footer_for_1dayago(ret, language):
    if language=='english':
        ret.append({'title': '120 other requests already completed', 'type': 'footer'})
    elif language=='hindi':
        ret.append({'title': '120 अन्य अनुरोध पहले ही पूरे हो चुके हैं', 'type': 'footer'})

def location_text(language, len, category):
    if language=='english':
        return "{} active requests for {} near".format(len, category.name[language])
    else:
        return "निकट {} के लिए {} सक्रिय कार्य अनुरोध".format(category.name[language], len)