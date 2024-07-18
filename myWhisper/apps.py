from django.apps import AppConfig


# inherit appConfig,
class MywhisperConfig(AppConfig):
    # default type of auto-incrementing primary key field for models in this app
    # BigAutoField : 64 bit integer for auto generated IDs
    default_auto_field = 'django.db.models.BigAutoField'
    # sets the name of the application
    name = 'myWhisper'
