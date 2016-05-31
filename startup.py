import sys
import markdown
from flask import Flask
from flask import render_template, request
from datetime import date
from flask_flatpages import FlatPages, pygments_style_defs
from flask_frozen import Freezer
from flask import Markup
from flask.ext.misaka import Misaka


BASE_URL = 'http://www.jamesharding.ca'
DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = 'content'
POST_DIR = 'posts'
HADOOP_DIR = 'hadoop'
VAGRANT_DIR = 'vagrant'
DOCKER_DIR = 'docker'
MONGODB_DIR = 'mongodb'
SPARK_DIR = 'spark'
FUSE_DIR = 'fuse'
CASSANDRA_DIR='cassandra'

app = Flask(__name__, static_url_path='/static')
Misaka(app)
flatpages = FlatPages(app)
freezer = Freezer(app)

app.config.from_object(__name__)

@app.context_processor
def inject_ga():
    return dict(BASE_URL=BASE_URL)

@app.route('/pygments.css')
def pygments_css():
    return pygments_style_defs('monokai'), 200, {'Content-Type': 'text/css'}

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/katerina/")
def katerina():
    return render_template('katerina.html')

@app.route("/ftejerez/")
def ftejerez():
    return render_template('ftejerez.html')

@app.route("/fathersday/")
def fathersday():
    return render_template('fathersday.html')

@app.route("/engineer/")
def engineer():
    return render_template('engineer.html')

@app.route("/pilot/")
def aviation():
    return render_template('pilot.html')

@app.route("/hobbies/")
def hobbies():
    return render_template('hobbies.html')

@app.route("/projects/")
def projects():
    return render_template('projects.html')

@app.route("/resume/")
def resume():
    return render_template('resume.html')

@app.route("/work-experience/")
def workexperience():
    return render_template('workexperience.html')

@app.route("/posts/")
def posts():
    posts = [p for p in flatpages if p.path.startswith(POST_DIR)]
    posts.sort(key=lambda item: item['date'], reverse=True)
    return render_template('posts.html', posts=posts)

@app.route('/posts/<name>/')
def post(name):
    path = '{}/{}'.format(POST_DIR, name)
    post = flatpages.get_or_404(path)
    return render_template('post.html', post=post)

@app.route('/docker/<name>/')
def docker(name):
    path = '{}/{}'.format(DOCKER_DIR, name)
    post = flatpages.get_or_404(path)
    return render_template('docker_template.html', post=post)

@app.route('/hadoop/<name>/')
def hadoop(name):
    path = '{}/{}'.format(HADOOP_DIR, name)
    post = flatpages.get_or_404(path)
    return render_template('hadoop_template.html', post=post)

@app.route('/vagrant/<name>/')
def vagrant(name):
    path = '{}/{}'.format(VAGRANT_DIR, name)
    post = flatpages.get_or_404(path)
    return render_template('vagrant-template.html', post=post)

@app.route('/cassandra/<name>/')
def cassandra(name):
    path = '{}/{}'.format(CASSANDRA_DIR, name)
    post = flatpages.get_or_404(path)
    return render_template('cassandra_template.html', post=post)

@app.route('/mongodb/<name>/')
def mongodb(name):
    path = '{}/{}'.format(MONGODB_DIR, name)
    post = flatpages.get_or_404(path)
    return render_template('post.html', post=post)

@app.route('/spark/<name>/')
def spark(name):
    path = '{}/{}'.format(SPARK_DIR, name)
    post = flatpages.get_or_404(path)
    return render_template('spark-template.html', post=post)

@app.route('/fuse/<name>/')
def fuse(name):
    path = '{}/{}'.format(FUSE_DIR, name)
    post = flatpages.get_or_404(path)
    return render_template('post.html', post=post)

@app.route('/robots.txt')
def robots():
    return render_template('robots.txt')

@app.route('/marketing-analytics/')
def marketing():
    return render_template('marketing-analytics.html')

@app.route('/aboutus/')
def aboutus():
    return render_template('aboutus.html')

@app.route('/sitemap.xml')
def sitemap():
    today = date.today()
    recently = date(year=today.year, month=today.month, day=1)
    posts = [p for p in flatpages if p.path.startswith(POST_DIR)]
    posts.sort(key=lambda item: item['date'], reverse=True)
    return render_template('sitemap.xml', posts=posts, today=today, recently=recently)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html'), 404

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(host='0.0.0.0', port=7777, debug=True)

