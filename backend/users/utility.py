from category.models import Category

def create_user_dict(user):
    user_details = {}
    user_details['mobile'] = user.mobile
    user_details['name'] = user.name
    user_details['user_language'] = user.user_language
    user_details['user_type'] = user.user_type
    user_details['token'] = user.token
    user_details['active'] = user.active
    if user.work_category is not None:
        category = Category.objects.get(id=user.work_category)
        user_details['work_category'] = category.name[user.user_language]
    if user.base_location is not None:
        user_details['base_location'] = user.base_location
    if user.work_radius is not None:
        user_details['work_radius'] = user.work_radius
    if len(user.email):
        user_details['email'] = user.email
    if len(user.address):
        user_details['address'] = user.address
    return user_details

def create_point_dict(latitude, longitude):
    point = {'type': 'Point', 'coordinates': [latitude, longitude]}
    return point