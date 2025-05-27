from django.apps import apps


def get_model_class(app_label, model_name):
    """
    Убедитесь, что модель импортирована только после полной инициализации Django.
    """
    return apps.get_model(app_label, model_name)