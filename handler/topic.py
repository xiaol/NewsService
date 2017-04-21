# coding=utf-8
import logging
import json
import random
import datetime
from bson import ObjectId

import requests
from tornado.web import RequestHandler

from operations.apprequest_ops import AppRequestItemOperation
from utils.response_handler import response_fail_json, response_success_json
from utils.utility import get_mongodb, get_mongodb246, extractor, change_text_txt
from utils.cache import redis_v2


class NewsDataHandler(RequestHandler):
    def post(self, *args, **kwargs):
        args = self.request.arguments
        for i in args:
            args[i] = args[i][0]
        # try:
        #     news = json.loads(data)
        # except Exception, e:
        #     response = response_fail_json(ret_message=u'json报文解析失败')
        #     self.write(response)
        #     return
        args['channel_id'] = ObjectId('57ac38feda083a1c19957b1c')
        args['online_source_sid'] = 3732
        ret, message = AppRequestItemOperation().create_app_item(args)
        if ret:
            redis_v2.sadd('spiders:spiders:parse', str(ret))
            logging.warning('Insert item success: wandoujia')
            response = response_success_json(ret_message=message)
        else:
            response = response_fail_json(ret_message=message)
            # logging.warning(response)
            # logging.warning('params: ' + json.dumps(args))
        self.write(response)


class JikeNewsDataHandler(RequestHandler):

    DOWNLOAD_KEY = "spiders:spiders:downloads"

    def post(self, *args, **kwargs):
        # args = self.request.arguments
        item_list_json = self.get_argument('news_list')
        item_list = json.loads(item_list_json)
        for i in item_list:
            params = dict()
            if 'app_name' not in i or 'published_date' not in i:
                continue
            params['app_name'] = i['app_name']
            params['published_date'] = i['published_date']
            params['type'] = 2
            if 'author' in i and i['author']:
                params['author'] = i['author']
            if 'summary' in i and i['summary']:
                try:
                    params['summary'] = i['summary'].encode('utf8')
                except:
                    params['summary'] = i['summary']
                if len(params['summary']) <= 60:
                    params['article_title'] = params['summary']
            else:
                params['summary'] = ''
            params['detail_html'] = params['summary']
            # if 'pictureUrl' in i and i['pictureUrl']:
            #     for j in i['pictureUrl']:
            #         params['detail_html'] += '<img src= %s />' % str(j)
            if 'link' in i and i['link']:
                params['link'] = i['link']
            else:
                continue
            params['online_source_sid'] = 3733
            params['channel_id'] = ObjectId("57ac392ada083a1c19957b1d")
            ret, message = AppRequestItemOperation().create_jike_app_item(params)
            if not ret:
                # logging.warning('params: ' + json.dumps(i))
                # logging.warning('Warning message: ' + message)
                continue
            logging.warning('Insert news success: jike')

            redis_v2.sadd(self.DOWNLOAD_KEY, str(ret))

        response = response_success_json()
        self.write(response)


class WeiboNewsDataHandler(RequestHandler):

    DOWNLOAD_KEY = "spiders:spiders:downloads"

    def post(self, *args, **kwargs):
        item_list_json = self.get_argument('news_list')
        item_list = json.loads(item_list_json)
        db = get_mongodb246()
        for i in item_list:
            weibo = db.weibo.find_one({'id': i['status']['id']})
            if weibo:
                logging.warning('Drop item: already exists')
                continue
            i['id'] = i['status']['id']
            i['procedure'] = 0
            db.weibo.insert(i)
            if 'video' in i:
                video_url = i['video']['streamUrl']
                if i['video']['streamUrlHd']:
                    video_url = i['video']['streamUrlHd']
                if not video_url or not video_url.startswith('http://gslb.miaopai.com'):
                    continue
                i['video_url'] = video_url
                print i['video_url']
                try:
                    self._video_adapter(i)
                except Exception as e:
                    logging.error(e.message)
                continue
            if 'mblogcards' in i and not i['mblogcards']:
                continue
            short_url = i['mblogcards'][0]['shortUrl']
            r = requests.get(short_url, timeout=15)
            url = r.url
            document = dict()
            document['site_id'] = ObjectId('583bc5155d272cd5c47a7668')
            document['channel_id'] = ObjectId('583bc834fe8eca697abd5f9b')
            document['headers'] = None
            document['cookies'] = None
            document['url'] = url
            document['crawl_url'] = url
            document['pagination'] = False
            document['proxy'] = 0
            document['pages'] = list()
            document['online_source_sid'] = 4850
            document['html'] = ''
            document['comment'] = {
                    # "user_id":i['status']['userId'],
                    # "weibo_id":i['status']['id'],
                    # "comment_count":i['status']['commentsCount']
            }
            document['fields'] = {}
            document['category'] = 1
            document['use_mobile_ua'] = False
            document['use_random_ua'] = True
            document['insert'] = datetime.datetime.now()
            document['upload'] = True
            document['procedure'] = 0
            try:
                db = get_mongodb246()
                db.v2_requests.insert(document)
                redis_v2.sadd(self.DOWNLOAD_KEY, str(document['_id']))
                logging.warning('Insert item success : weibo')

            except Exception as e:
                logging.warning('Error message: ' + e.message)
            if '_id' in document:
                print document['_id']

        self.write(response_success_json())

    def _video_adapter(self, item):
        UPLOAD = "http://10.25.60.218:8081/api/store/video"
        f = "%a %b %d %H:%M:%S +0800 %Y"
        ptime = datetime.datetime.strptime(item["status"]["createDate"], f)
        thumbnail = item["video"]["pagePic"]
        if not thumbnail.startswith("http"):
            return
        duration = int(item["video"].get("duration", 0))
        click_times = item["video"].get("onlineUsersNumber", 0)
        pname = u"微博热点"
        icon = "https://oss-cn-hangzhou.aliyuncs.com/bdp-images/35731635d18811e6bfb780e65007a6da.jpg"
        if 'avatarHd' in item['status']:
            icon = item['status']['avatarHd']
            pname = item['status']['userName']
        data = {
            "title": item['status']['blogContent'],
            "unique_id": item['video']['h5Url'],
            "publish_url": item['video']['h5Url'],
            "publish_site": pname,
            "publish_time": ptime.isoformat()[:-7]+"Z",
            "insert_time": self.format_time().isoformat()[:-7]+"Z",
            "author": "",
            "author_icon": "",
            "site_icon": icon,
            "channel_id": 35,
            "second_channel_id": 0,
            "source_id": 4850,
            "online": True,
            "video_url": item['video_url'],
            "video_thumbnail": thumbnail,
            "video_duration": duration,
            "play_times": click_times,
        }
        try:
            r = requests.post(UPLOAD, json=data, timeout=(5, 10))
        except Exception as e:
            logging.warning(e.message)
        else:
            if r.status_code == 200:
                result = r.json()
                logging.info("Store video: %s" % json.dumps(result))
                self.store_relate_videos(result["id"])
            else:
                logging.info("status code: %s" % r.status_code)

    @staticmethod
    def store_relate_videos(nid):
        url = "http://10.25.60.218:8081/search/relate/video"
        try:
            r = requests.post(url, data={"id": nid}, timeout=(5, 10))
        except Exception as e:
            logging.warning(e.message)
        else:
            if r.status_code == 200:
                logging.info("%s relate videos for %d" % (len(r.json()), nid))


    @staticmethod
    def format_time(t=None):
        f = "%Y-%m-%d %H:%M:%S"
        result = None
        if t is None:
            return datetime.datetime.now()
        try:
            result = datetime.datetime.strptime(t, f)
        except Exception:
            pass
        if result is None:
            result = datetime.datetime.now()
        return result


class VideoViewHandler(RequestHandler):
    def get(self, *args, **kwargs):
        db = get_mongodb()
        count = db.news.find({'status': 4}).count()
        skip = random.randint(0, count-11)
        videos_data = db.news.find({'status': 4}).skip(skip).limit(10)
        html_code_list = list()
        for j in videos_data:
            item = dict()
            item['url'] = j['key']
            item['title'] = j['title']
            item['pub_time'] = j['publish_time']
            item['docid'] = item['url']
            item['content_html'] = j['content_html']
            content_list = extractor(j['content_html'])
            item['content'] = json.dumps(change_text_txt(content_list))
            html = ''
            html += '<center><h2>' + item['title'] + '</h2></center>'
            html += '<p>' + item['pub_time'] + '</p>'
            # html += '<p>' + item['pub_name'] + '</p>'
            content = json.loads(item['content'])
            if not content:
                continue
            for i in content:
                if 'txt' in i:
                    html += '<p>&nbsp&nbsp&nbsp&nbsp&nbsp' + i['txt'] + '</p>'
                elif 'img' in i:
                    html += '<center><img src="' + i['img'].encode('utf8') + '"></center>'
                elif 'video' in i:
                    html += '<center><video controls="controls" src="%s"></center>' % i['video'].encode('utf8')
            html += '<p>' + '-'*100 + '</p>'
            html_code_list.append(html)
        self.render('item.html', data=html_code_list)
