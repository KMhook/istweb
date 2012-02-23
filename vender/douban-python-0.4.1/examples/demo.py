#!/usr/bin/env python
#coding=utf-8

import sys

try:
    import web
except Exception:
    print 'please install webpy first'
    sys.exit(0)

try:
    from douban.service import DoubanService
    from douban.client import OAuthClient
except ImportError:
    print 'please install douban-python'
    sys.exit(0)

HOST = 'http://www.douban.com'
PREFIX = '/service/apidemo' 
API_KEY=''
SECRET=''

request_tokens = {}
access_tokens = {}

def html_header():
    print """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <title>API认证演示</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <style>
    body {padding:0;margin: 0;background: #FEFEFE;}
    #maxw{ margin: 0 auto; padding:8px 30px;  background: #FFF;  max-width: 964px; width:expression( documentElement.clientWidth > 940 ? (documentElement.clientWidth == 0 ? (body.clientWidth >940 ? "940" : "auto") : "940px") : "auto" ); }

    form { padding: 0; border: 0px; }
    textarea{ overflow:auto; }
    a:link { color: #336699; text-decoration: none; }
    a:visited { color: #666699; text-decoration: none; }
    a:hover { color: #FFFFFF; text-decoration: none; background: #003399; }
    a:active { color: #FFFFFF; text-decoration: none; background: #FF9933; }
    a img { border-width:0; }

    body,td,th { font: 12px Arial, Helvetica, sans-serif; line-height: 150%; }
    table { border-collapse:collapse; border: none; padding: 0; margin: 0; }
    h1 { font-size: 25px; font-weight: bold; color: #494949; margin:0 0 0px 0; padding: 8px 0px 6px 0px; line-height:1.1em; }
    h2 { font: 14.8px normal Arial, Helvetica, sans-serif; color: #006600; margin-bottom: 5px; line-height: 150%; }
    h3 {width:100%;height:26px;margin-left:4px;font: 14.8px normal Arial, Helvetica, sans-serif;color: #666666;margin-bottom: 1px;line-height: 150%;background:url(/pics/topicbar.gif) no-repeat right top}
    h3 img{margin:1px 1px 0 0;}
    ul { list-style-type: none; margin: 0; padding: 0; }
    h4 {height:26px; margin:0 0 15px 4px; font: 12px normal Arial, Helvetica, sans-serif;color: #666666;line-height: 1.8em;background:url(/pics/topicbar.gif) no-repeat right top;}

    .obss {width :100%}
    .obs{ margin: 0 0 10px 0; float: left; text-align: center; overflow: hidden; width: 105px; }
    .obs dt{ height: 114px; width: 105px; overflow: hidden; }
    .obs dd{ margin: 0; height: 80px; overflow: hidden; }

    .gact { color: #BBBBBB; font-size: 12px; text-align: center; cursor:pointer; }
    </style>
    <body>
    <div id="maxw">
    <h1>API认证演示</h1>"""

def html_footer():
    print """
    </div>
    </body>
</html>"""

def search_panel(q = "monty python"):
    print """
            <h2>搜索电影并添加收藏...</h2>
            <form action="%s/search" method="GET">
            <input name="q" width="30" value="%s">
            <input type="submit" value="搜索电影">
            </form>""" % (PREFIX, q)


class index(object):
    def GET(self):
        html_header()
        search_panel()
        html_footer()

        
class search(object):
    def GET(self):
        q = web.input().get('q','')
        html_header()
        search_panel(q)
        if q:
            service = DoubanService(api_key=API_KEY,secret=SECRET)
            feed = service.SearchMovie(q)
            print '<div class="obss" style="margin-top:20px">'
            for movie in feed.entry:
                print '<dl class="obs"><dt>'
                print '<div class="gact"><a href="%s/collection?sid=%s">想看</a></div>' % (PREFIX, movie.id.text)
                print '<a href="%s" title="%s"><img src="%s" class="m_sub_img"/></a>' % (movie.GetAlternateLink().href, movie.title.text, ((len(movie.link) >= 3) and movie.link[2].href) or '')
                print '</dt><dd>'
                print '<a href="%s">%s</a>' % (movie.GetAlternateLink().href, movie.title.text)
                print '</dd>'
                print '</dl>'
            print '</div>'
        html_footer()

class collection(object):
    def GET(self):
        sid = web.input().get('sid','')
        if not sid:
            print 'no sid'
            return 
        
        client = OAuthClient(key=API_KEY, secret=SECRET)
        cookies = web.cookies()
        access_key = cookies.get('access_key')
        access_secret = access_tokens.get(access_key)

        if not access_key or not access_secret:
            request_key = web.input().get('oauth_token','')
            request_secret = request_tokens.get(request_key)
            if request_key and request_secret:
                try:
                    access_key, access_secret = \
                        client.get_access_token(request_key, request_secret) 
                    if access_key and access_secret:
                        # store user access key in cookie, 
                        # not accessable by other people
                        web.setcookie('access_key', access_key)
                        access_tokens[access_key] = access_secret
                except Exception:
                    access_token = None
                    print '获取用户授权失败'
                    return 
            else:
                client = OAuthClient(key=API_KEY, secret=SECRET) 
                key, secret = client.get_request_token()
                if key and secret:
                    request_tokens[key] = secret
                    url = client.get_authorization_url(key, secret, callback=HOST+PREFIX+'/collection?sid='+sid)
                    web.tempredirect(url)
                    return
                else:
                    print '获取 Request Token 失败'
                    return 

        service = DoubanService(api_key=API_KEY, secret=SECRET)
        movie = service.GetMovie(sid)
        html_header()
        search_panel()
        print '<h2>你希望收藏电影: %s</h2>' % (movie.title.text)
        print '<div class="obss" style="margin-top:20px">'
        print '<dl class="obs"><dt>'
        print '<a href="%s" title="%s"><img src="%s" class="m_sub_img"/></a>' % (movie.GetAlternateLink().href, movie.title.text, movie.link[2].href)
        print '</dt><dd>'
        print '<a href="%s">%s</a>' % (movie.GetAlternateLink().href, movie.title.text)
        print '</dd>'
        print '</dl>'
        if access_key and access_secret:
            if service.ProgrammaticLogin(access_key, access_secret):
                try:
                    entry = service.AddCollection('wish', movie, tag=['test'])
                    if entry:
                        print '<span>已添加到你的收藏</span>'
                    else:
                        print '<span>添加收藏失败</span>'
                except Exception:
                    print '<span>添加收藏失败, 授权失效</span>'
                    del access_tokens[access_key]
                    web.setcookie('access_key', '', 0)
        else:
            print '<span>无法添加收藏，可能你因为你没有授权这个应用访问你在豆瓣的数据</span>'
        print '</div>'
        html_footer()

urls = (
    PREFIX+'/', 'index',
    PREFIX+'/search', 'search',
    PREFIX+'/collection', 'collection',
)
    
if __name__ == '__main__':
    web.run(urls, globals())
