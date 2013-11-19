#coding=utf-8
import random
import datetime
from flask import  (Blueprint, request, redirect, render_template, url_for,
                 jsonify)
from flask.views import MethodView
from data_analysis.models import Apidist, Celery, Mongo

posts = Blueprint('posts', __name__, template_folder='templates')

color = ["#FF0F00", "#FF6600", "#FF9E01", "#FCD202", "#F8FF01", "#B0DE09",
         "#04D215", "#0D8ECF", "#0D52D1", "#2A0CD0", "#8A0CCF", "#CD0D74",
         "#754DEB", "#2c3e50", "#2c3e50", "#e67e22", "#e74c3c", "#ecf0f1",
         "#95a5a6", "#d35400", "#8e44ad", "#8e44ad", "#bdc3c7", "#d35400",
         "#1abc9c", "#2ecc71", "#3498db", "#9b59b6", "#34495e"]

celery = dict(task=[('count', ["simple_column", "pie"]),
                    ('cost', ["multi_column"])],
              time=[('count', ["simple_column", "pie"])])

mongo = dict(all=[('getmore', ["multi_column"]), ('update', ["multi_column"]),
                  ('insert', ["multi_column"]), ('command', ["multi_column"]),
                  ('query', ["multi_column"])],
             sentiment=[('getmore', ["multi_column"]), ('update', ["multi_column"]),
                        ('insert', ["multi_column"]), ('command', ["multi_column"]),
                        ('query', ["multi_column"])],
             qq_online=[('getmore', ["multi_column"]), ('update', ["multi_column"]),
                        ('insert', ["multi_column"]), ('command', ["multi_column"]),
                        ('query', ["multi_column"])],
             total=[('getmore', ["simple_column", "pie"]),
                    ('update', ["simple_column", "pie"]),
                    ('insert', ["simple_column", "pie"]),
                    ('command', ["simple_column", "pie"]),
                    ('query', ["simple_column", "pie"]),
                    ('all_op', ["simple_column", "pie"]),
                    ('all_slow', ["simple_column", "pie"])])
d3 = dict()


def make_json(res, title, category, value, chart, key, des, total, titles=None,
              values=None):
    color1, color2, color3 = None, None, None
    if titles is not None:
        func= lambda x:x[values[key]]
    else:
        func= lambda x:x[value]
    dict_list = sorted(res, key=func, reverse=True)
    if titles is None:
        l = len(dict_list)
        color_choice = random.sample(color, l)
        for num, d in enumerate(dict_list):
            d['color'] = color_choice[num]
    else:
        color_choice = random.sample(color, 3)
        for d in dict_list:
            d['color1'] = color_choice[0]
            d['color2'] = color_choice[1]
            d['color3'] = color_choice[2]
    return jsonify(result=dict_list, title=title, category=category, des=des,
                   value=value, titles=titles, values=values, chart=chart,
                   total=total)

def make_factory(change_dict):
    dict = {'title': 'name', 'value': 'call'}
    dict.update(change_dict)
    return dict

class JsonView(MethodView):

    def get(self, url):
        if url == 'celery':
            return jsonify(celery)
        elif url == 'mongo':
            return jsonify(mongo)

class IndexView(MethodView):

    def get(self):
        return redirect(url_for('.mongo'))

class D3View(MethodView):

    def get(self):
        return render_template('posts/d3.html', des=u'celery任务调用次数略览',
                               title=u'Celery Task调用分布')

class TroubleView(MethodView):

    def get(self):
        return render_template('posts/trouble.html', title=u'Mongodb存在问题分析',
                               des=u'总结错误索引原因和解决方案')

class MongoView(MethodView):

    def get(self):
        l = Mongo.objects.distinct(field="database")
        #l.insert(0, 'all')
        l.insert(0, 'total')
        return render_template('posts/index.html', first_type=u'Mongodb分析',
                               title=u'Mongodb使用数据分析', l=l,
                               des=u'数据库操作数据分析')

    def all(self, type):
        return self.time('all', type)

    def sentiment(self, type):
        return self.time('sentiment', type)

    def qq_online(self, type):
        return self.time('qq_online', type)

    def time(self, database, type):
        if database == 'all':
            obj = Mongo.objects()['hour']
        else:
            obj = Mongo.objects(database=database)[0]['hour']
        o = []
        all_total = 0
        slow_total = 0
        for i in range(24):
            i = str(i)
            d = {}
            d['name'] = u'{0}时'.format(str(i))
            d['op'] = obj[i]['op'][type]
            d['slow'] = obj[i]['slow'][type]
            all_total += d['op']
            slow_total += d['slow']
            o.append(d)
        titles = (u'慢查询', u'全部查询')
        values = ('slow', 'op')
        return make_factory({'titles': titles, type: o,
                             'total': '慢查询:{0}, 全部查询:{1}'.format(
                                 slow_total, all_total),
                             'des': '[数据库{0} 类型{1}] 总量'.format(database,
                                                                      type),
                             'category': u'mongodb分析', 'values': values})

    def total_data(self, type):
        getmore, insert, update, command, query = 0, 0, 0, 0, 0
        for i in range(24):
            for obj in Mongo.objects():
                insert += obj['hour'][str(i)][type]['insert']
                update += obj['hour'][str(i)][type]['update']
                command += obj['hour'][str(i)][type]['command']
                query += obj['hour'][str(i)][type]['query']
                getmore += obj['hour'][str(i)][type]['getmore']
        count = []
        for name, call in ((u'查询', query), (u'插入', insert),
                           (u'命令', command), (u'更新', update),
                           ('getomre', getmore)):
            d = {}
            d['name'] = name
            d['call'] = call
            count.append(d)
        total = getmore + insert + update + command + query
        return count, total

    def all_op(self):
        data = self.total_data('op')
        return make_factory({'all_op': data[0], 'des': u'数据库操作总量',
                             'category': u'mongodb操作分布',
                             'total': data[1]})

    def all_slow(self):
        data = self.total_data('slow')
        return make_factory({'all_slow': data[0], 'des': u'数据库慢查询总量',
                             'category': u'mongodb慢操作分布',
                             'total': data[1]})

    def total(self, type):
        if type == 'all_op':
            return self.all_op()
        elif type == 'all_slow':
            return self.all_slow()
        call = 0
        call_total = 0
        count = []
        for i in range(24):
            d = {}
            for obj in Mongo.objects():
                call += obj['hour'][str(i)]['total']
            d['name'] = u'{0}时'.format(str(i))
            d['call'] = call
            call_total += call
            call = 0
            count.append(d)
        return make_factory({type: count, 'category':u'mongodb分布',
                             'des': u'数据库查询总量',
                             'total': call_total})

    def post(self):
        return get_form(request, self, mongo, key=1)


def get_form(request, self, type, key=2):
    vt = request.form.getlist('vt')[0]
    data_type = request.form.getlist('type')[0]
    data_type = data_type if data_type else type[vt][0][0]
    chart = request.form.getlist('chart')[0]
    if not chart:
        for t in type[vt]:
            if data_type == t[0]:
                chart = t[1][0]
    data = getattr(self, vt)(data_type)
    if chart in ["simple_column", "pie"]:
        return make_json(data[data_type], data['title'], data['category'],
                          data['value'], chart, key, data['des'], data['total'])
    elif chart == 'multi_column':
        return make_json(data[data_type], data['title'], data['category'],
                         data['value'], chart, key, data['des'], data['total'],
                         titles=data['titles'], values=data['values'])


class CeleryView(MethodView):
    def time(self, type):
        count = []
        total = 0
        for i in range(23):
            d = {}
            d['name'] = u'{0}时'.format(str(i))
            d['call'] = Celery.objects(
                time__gte=datetime.datetime(2013, 10, 27, i),
                time__lt=datetime.datetime(2013, 10, 27, i+1)).count()
            total += d['call']
            count.append(d)
        return make_factory(dict(count=count, category=u'celery分布',
                                 des=u'celery总量', total=total))

    def post(self):
        return get_form(request, self, celery)

    def task(self, type):
        count = []
        cost = []
        total = 0
        for i in Celery.objects.distinct(field='task'):
            d = {}
            c = {}
            data = Celery.objects(task=i)
            d['call'] = data.count()
            d['name'], c['name'] = i, i
            c['avg'] = data.order_by('cost')[0].cost, # min
            c['min'] = data.average('cost'),
            c['max'] = data.order_by('-cost')[0].cost # max
            total += d['call']
            cost.append(c)
            count.append(d)
            titles = (u'最小值', u'平均值', u'最大值')
            values = ('avg', 'min', 'max')
        return make_factory(dict(titles=titles, count=count, cost=cost,
                                 category=u'celery分析', values=values,
                                 des=u'celery总量', total=total))

    def get(self):
        l = ['task', 'time']
        return render_template('posts/index.html', first_type=u'监控类型',
                               title=u'mongo日志分析',
                               des=u'分析mongodb全天日志整理的分布数据', l=l)

posts.add_url_rule('/mongo/', view_func=MongoView.as_view('mongo'))
posts.add_url_rule('/', view_func=IndexView.as_view('index'))
posts.add_url_rule('/celery/', view_func=CeleryView.as_view('celery'))
posts.add_url_rule('/json/<url>/', view_func=JsonView.as_view('json'))
posts.add_url_rule('/d3/', view_func=D3View.as_view('d3'))
posts.add_url_rule('/trouble/', view_func=TroubleView.as_view('trouble'))
