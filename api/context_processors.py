def frontend(request):
    """Заглушка для шаблонов до реализации своей аутентификации."""
    return {
        'is_logged_in': False,
        'current_user_email': None,
    }
