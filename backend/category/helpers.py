def categories_dict(categories_list):
    request_dict = {}
    for category in categories_list:
        request_dict[str(category.id)] = category
    return request_dict


def request_json_for_category(category, user_language):
    request_data = {'category_id': str(category.id), 'name': category.name[user_language],
                    'icon_url': category.icon_url, 'has_questions': category.has_questions}
    return request_data


def request_json(super_category, fetched_categories_dict, user_language):
    request_data = {'super_category_id': str(super_category.id), 'name': super_category.name[user_language],
                    'default_view_count': super_category.default_view_count, 'categories': []}
    for category_obj_id in super_category.categories:
        category_obj = request_json_for_category(fetched_categories_dict[category_obj_id], user_language)
        request_data['categories'].append(category_obj)
    return request_data



