from flask import Flask


class MyApp(Flask):
    def __init__(self, *args, **kwargs):
        super(MyApp, self).__init__(*args, **kwargs)
        self.config['SECRET_KEY'] = "super_secret_key"


app = MyApp(__name__, static_folder='../main_app/static', template_folder='../main_app/templates')
