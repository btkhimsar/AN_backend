def create_user_dict(user):
    user_details = {'mobile': user.mobile, 'name': user.name, 'user_language': user.user_language,
                    'user_type':user.user_type}
    if len(user.email):
        user_details['email'] = user.email
    if user.base_location is not None:
        user_details['base_location'] = user.base_location
    if user.work_radius is not None and user.work_radius<=10 and user.work_radius>=3:
        user_details['work_radius'] = user.work_radius
    if user.work_category is not None:
        user_details['work_category'] = user.work_category
    if len(user.address):
        user_details['address'] = user.address
    return user_details
