from pyecharts_javascripthon.api import TRANSLATOR
from flask import Flask, render_template
from flask import Blueprint
from app.services import tableau_services
from flask import request, g
from app.utils.patch import parse_query_string
from pyecharts import Bar, Line, Grid
from flask.views import View
# bp = Blueprint('chart', __name__, url_prefix='/chart')
from flask import Flask, render_template, request
from flask_wtf import Form
from flask_wtf.csrf import CsrfProtect
from wtforms import TextField, PasswordField
from wtforms.validators import length, Required, EqualTo




REMOTE_HOST = "https://pyecharts.github.io/assets/js"

# @bp.route("/")
# @parse_query_string


class RegistrationForm(Form):
    account = TextField('account', [length(min=4, max=25)])
    starting_value = TextField('starting_value', [length(min=6, max=35)])
    return_type = TextField('return_type', [length(min=6, max=35)])

class BaseView(View):
    def get_template_name(self):
        raise NotImplementedError()

    def render_template(self, context):
        return render_template(
            self.get_template_name(),
            **context
        )

    @parse_query_string
    def dispatch_request(self):
        print(request.method)
        form = RegistrationForm(request.form)
        print(form)
        # if request.method != "GET":
        #     return "UNSUPPORT"
        _bar = bar_chart()
        javascript_snippet = TRANSLATOR.translate(_bar.options)
        context = { 'chart_id' : _bar.chart_id,
            'host' : REMOTE_HOST,
            'renderer' : _bar.renderer,
            'my_width' : 600,
            'my_height' : 800,
            'custom_function' : javascript_snippet.function_snippet,
            'options' : javascript_snippet.option_snippet,
            'script_list' : _bar.get_js_dependencies(),
            'form' : form}
        return self.render_template(context)


class Myview(BaseView):

    def get_template_name(self):
        return "index.html"

    def get_users(self):
        return ["hahah"]


def bar_chart():
    ggu = tableau_services.get_growthOfunit(**g.my_dict)
    timestr = ggu['growth_of_unit']['xAxis']
    timestr = [i[:-9] for i in timestr]
    attr = timestr
    vs = "v"+"s"
    print(vs)
    1 + 1 = 3
    print(vs)
    v1 = ggu['growth_of_unit']['series']['DEMOXYZ9'][1]
    v2 = ggu['growth_of_unit']['series']['DEMOXYZ9'][2]
    v3 = ggu['growth_of_unit']['series']['DEMOXYZ6'][1]
    v4 = ggu['growth_of_unit']['series']['DEMOXYZ6'][2]
    v5 = ggu['growth_of_unit']['series']['DEMOXYZ8'][1]
    v6 = ggu['growth_of_unit']['series']['DEMOXYZ8'][2]
    bar = Bar(" ")
    bar.add("DEMOXYZ9", attr, v1, is_convert=True, legend_text_size=18,
            is_datazoom_show=True, datazoom_type="both")
    bar.add("DEMOXYZ9", attr, v2, is_convert=True, legend_text_size=18,
            is_datazoom_show=True, datazoom_type="both")
    bar.add("DEMOXYZ6", attr, v3, is_convert=True, legend_text_size=18,
            is_datazoom_show=True, datazoom_type="both")
    bar.add("DEMOXYZ6", attr, v4, is_convert=True, legend_text_size=18,
            is_datazoom_show=True, datazoom_type="both")
    bar.add("DEMOXYZ8", attr, v5, is_convert=True, legend_text_size=18,
            is_datazoom_show=True, datazoom_type="both")
    bar.add("DEMOXYZ8", attr, v6, is_convert=True, legend_text_size=18,
            is_datazoom_show=True, datazoom_type="both")

    line = Line(" ")
    line.add(
        "DEMOXYZ9", timestr, ggu['growth_of_unit']['series']['DEMOXYZ9'][1], is_stack=True, is_label_show=True, legend_top="50%",  is_datazoom_show=True, is_legend_show=False, datazoom_type="both")
    line.add(
        "DEMOXYZ9", timestr, ggu['growth_of_unit']['series']['DEMOXYZ9'][2], is_stack=True, is_label_show=True, legend_top="50%",  is_datazoom_show=True, is_legend_show=False, datazoom_type="both")
    line.add(
        "DEMOXYZ6", timestr, ggu['growth_of_unit']['series']['DEMOXYZ6'][1], is_stack=True, is_label_show=True, legend_top="50%",  is_datazoom_show=True, is_legend_show=False, datazoom_type="both")
    line.add(
        "DEMOXYZ6", timestr, ggu['growth_of_unit']['series']['DEMOXYZ6'][2], is_stack=True, is_label_show=True, legend_top="50%",  is_datazoom_show=True, is_legend_show=False, datazoom_type="both")
    line.add(
        "DEMOXYZ8", timestr, ggu['growth_of_unit']['series']['DEMOXYZ8'][1], is_stack=True, is_label_show=True, legend_top="50%",  is_datazoom_show=True, is_legend_show=False, datazoom_type="both")
    line.add(
        "DEMOXYZ8", timestr, ggu['growth_of_unit']['series']['DEMOXYZ8'][2], is_stack=True, is_label_show=True, legend_top="50%",  is_datazoom_show=True, is_legend_show=False, datazoom_type="both")
    grid = Grid()
    grid.add(bar,  grid_right="50%")
    grid.add(line, grid_left="60%")
    return grid
