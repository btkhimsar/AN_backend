def categories_dict(categories_list):
    request_dict = {}
    for category in categories_list:
        request_dict[category._id] = category
    return request_dict


def request_json_for_category(category, language):
    request_data = {'category_id': category._id, 'name': category.name[language],
                    'icon_url': category.icon_url}
    if len(category.questions):
        request_data['has_questions'] = True
    else:
        request_data['has_questions'] = False
    return request_data


def request_json(super_category, fetched_categories_dict, language):
    request_data = {'super_category_id': super_category._id, 'name': super_category.name[language],
                    'default_view_count': super_category.default_view_count, 'categories': []}
    for category_obj_id in super_category.categories:
        category_obj = request_json_for_category(fetched_categories_dict[category_obj_id], language)
        request_data['categories'].append(category_obj)
    return request_data



