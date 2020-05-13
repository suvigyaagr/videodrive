from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def get_paginated_object(paginator: Paginator, page: int):
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = []
    return objects


def convert_last_video_dt_to_page_token(last_id: str):
    page_token_list = [chr(97+int(i)) for i in str(last_id)]
    return ''.join(page_token_list).upper()


def get_last_video_dt_from_page_token(token: str):
    last_id_str_list = [str(ord(i)-97) for i in token.lower()]
    return int(''.join(last_id_str_list))
