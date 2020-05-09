from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def get_paginated_object(paginator: Paginator, page: int):
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = []
    return objects
