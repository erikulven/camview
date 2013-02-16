from flask import Flask
from flask import request
from flask import render_template
import os
page_size = 50
app = Flask(__name__)
image_path = '/Users/erik/projects/camview/static/cam/'


def datetime_str(fname):
    """
    convert filename to date string
    000DC5D9AC49(bergcam)_1_20130131214855_100.jpg
    """
    ds = []
    us_cnt = 0
    for c in fname:
        if '_' == str(c):
            us_cnt += 1
        if int(us_cnt) == 2 and '_' != str(c):
            ds.append(c)
    dt_str = ''.join(ds)
    return "%s-%s-%s %s:%s:%s" % (dt_str[:4], dt_str[4:6], dt_str[6:8], dt_str[8:10], dt_str[10:12], dt_str[12:14])


def date_str(datetime_str):
    return datetime_str[:10]


@app.route('/')
@app.route('/cam')
@app.route('/<date>')
@app.route('/cam/<date>')
def index(date=None):
    page_no = int(request.args.get('page_no', '1'))
    images = os.listdir(image_path)
    dates = []
    for fname in images:
        dts = datetime_str(fname)
        dt = date_str(dts)
        if not dt in dates:
            dates.append(dt)
    count = len(images)

    selected = sorted([img for img in images if not date or date in datetime_str(img)], reverse=True)
    page_count = count / page_size
    end = (page_no * page_size)
    start = (end - page_size)
    if end > count:
        end = count

    imgs = []
    for fname in selected[start:end]:
        dts = datetime_str(fname)
        imgs.append((dts, fname))

    return render_template('index.html', images=imgs, dates=dates, date=date,
                           count=count, count_date=len(selected), page_no=page_no,
                           page_count=page_count)

if __name__ == '__main__':
    app.debug = True
    app.run()
    # app.run(host='0.0.0.0')
