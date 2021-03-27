from django.db.models import Q


def filter_or_get_all_tasks(tag):
    """Фильтрует записи по тегу, если он передан, иначе отдает все записи"""
    if tag:
        return Q(tag=tag)
    return Q()
