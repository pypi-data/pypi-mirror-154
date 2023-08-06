#!/usr/bin/env python
import glob
import json
import logging
import math
import mimetypes
import os
import platform
import re
import shutil
import socket
import subprocess
import sys
import tempfile
from multiprocessing import Process
from random import uniform
from socket import gaierror
from time import sleep
from importlib.metadata import metadata
from urllib.error import URLError
from urllib.parse import unquote, urldefrag, urljoin, urlparse

import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import FakeUserAgentError, UserAgent
from packaging.version import parse
from requests.auth import HTTPBasicAuth
from requests.packages import urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from robotsparsetools import NotFoundError, Parse
from tqdm import tqdm

try:
    import msvcrt
except:
    import termios

try:
    metadata("prop-request")
    _binary = False
except:
    _binary = True
    _prop_directory = os.path.join(os.environ.get("HOME"), ".prop-datas")
    if not os.path.isdir(_prop_directory):
        os.mkdir(_prop_directory)

"""
下記コマンド実行必要
pip install requests numpy beautifulsoup4 requests[socks] fake-useragent tqdm
(urllib3はrequests付属)
"""

urllib3.disable_warnings(InsecureRequestWarning)

VERSION = parse("1.2.7")


class error:
    @staticmethod
    def print(msg):
        print(f"\033[31m{msg}\033[0m", file=sys.stderr)
        print("\n\033[33mIf you don't know how to use, please use '-h', '--help' options and you will see help message\033[0m", file=sys.stderr)
        sys.exit(1)

class LoggingHandler(logging.StreamHandler):
    color = {'INFO': '\033[36mINFO\033[0m', 'WARNING': '\033[33mWARNING\033[0m', 'WARN': '\033[33mWARN\033[0m', 'ERROR': '\033[31mERROR\033[0m'}
    def __init__(self, level=logging.NOTSET):
        super().__init__(level)

    def emit(self, record):
        try:
            record.levelname = LoggingHandler.color.get(record.levelname, record.levelname)
            msg = self.format(record)
            tqdm.write(msg, file=sys.stderr)
            self.flush()
        except Exception:
            self.handleError(record)

class LoggingFileHandler(logging.Handler):
    def __init__(self, file, mode="a", level=logging.NOTSET):
        super().__init__(level)
        self.file = open(file, mode)

    def emit(self, record):
        try:
            record.msg = re.sub('\033\\[[+-]?\\d+m', '', str(record.msg))
            record.levelname = re.sub('\033\\[[+-]?\\d+m', '', record.levelname)
            msg = self.format(record)
            self.file.write(msg)
            self.file.write('\n')
            self.file.flush()
        except Exception as e:
            self.handleError(record)

class setting:
    """
    オプション設定やファイルへのログを定義するクラス
    """
    if _binary:
        log_file = os.path.join(_prop_directory, 'log.log')
        config_file = os.path.join(_prop_directory, 'config.json')
    else:
        log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log.log')
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')

    def __init__(self):
        # 設定できるオプションたち
        # 他からimportしてもこの辞書を弄ることで色々できる
        self.options = {'download_name': '', 'limit': 0, 'only_body': False, 'debug': False, 'parse': False, 'types': 'get', 'payload': None, 'output': True, 'filename': None, 'timeout': (3.0, 60.0), 'redirect': True, 'upload': None, 'json': False, 'search': None, 'header': {'User-Agent': 'Prop/1.1.2'}, 'cookie': None, 'proxy': {"http": os.environ.get("http_proxy") or os.environ.get("HTTP_PROXY"), "https": os.environ.get("https_proxy") or os.environ.get("HTTPS_PROXY")}, 'auth': None, 'bytes': False, 'recursive': 0, 'body': True, 'content': True, 'conversion': True, 'reconnect': 5, 'caperror': True, 'noparent': False, 'no_downloaded': False, 'interval': 1, 'start': None, 'format': '%(file)s', 'info': False, 'multiprocess': False, 'ssl': True, 'parser': 'html.parser', 'no_dl_external': True, 'save_robots': True, 'check_only': False}
        # 以下logger設定
        logger = logging.getLogger('Log of Prop')
        logger.setLevel(20)
        sh = LoggingHandler()
        self.fh = LoggingFileHandler(setting.log_file)
        logger.addHandler(sh)
        logger.addHandler(self.fh)
        format = logging.Formatter('%(asctime)s:[%(levelname)s]> %(message)s')
        sh.setFormatter(format)
        self.fh.setFormatter(format)
        self.log = logger.log

    def config_load(self) -> None:
        """
        設定ファイルをロード
        """
        if os.path.isfile(setting.config_file):
            with open(setting.config_file, 'r') as f:
                config = json.load(f)
            if isinstance(config['timeout'], list):
                config['timeout'] = tuple(config['timeout'])
            self.options.update(config)

    def config(self, key: str, value: str or bool or None) -> None:
        """
        オプションの設定
        """
        self.options[key] = value

class cache:
    """
    キャッシュ(stylesheet)を扱うクラス
    """
    if _binary:
        root = os.path.join(_prop_directory, 'cache')
    else:
        root = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache')
    configfile = os.path.join(root, '.cache_info')
    if os.path.isfile(configfile):
        with open(configfile, 'r') as f:
            _caches = json.load(f)
    else:
        _caches = dict()

    def __init__(self, url, parse):
        self.parse = parse
        host = self.parse.get_hostname(url) 
        if not os.path.isdir(self.root):
            os.mkdir(self.root)
        self.directory = os.path.join(cache.root, host)
        if not os.path.isdir(self.directory):
            os.mkdir(self.directory)

    @staticmethod
    def get_cache(url) -> str or None:
        return cache._caches.get(url)

    def save(self, url, body: bytes) -> str:
        file = os.path.join(self.directory, self.parse.get_filename(url))
        with open(file, 'wb') as f:
            f.write(body)
        cache._caches[url] = file

    @staticmethod
    def update(option):
        file = os.path.join('styles', '.prop_info.json')
        if os.path.isfile(file):
            with open(file, 'r') as f:
                info_dict = json.load(f)
        else:
            info_dict = dict()
        if not cache._caches:
            return
        for url, path in tqdm(cache._caches.items()):
            r = requests.get(url, timeout=option['timeout'], proxies=option['proxy'], headers=option['header'], verify=option['ssl'])
            with open(path, 'wb') as f:
                f.write(r.content)
            tqdm.write(f"updated '{path}'")
            if url in info_dict:
                shutil.copy(path, info_dict[url])
                tqdm.write(f"updated '{info_dict[url]}'")
            sleep(0.5)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        with open(cache.configfile, 'w') as f:
            json.dump(self._caches, f)

class history:
    """
    ダウンロード履歴関連の関数を定義するクラス
    基本的に./history配下のファイルのみ操作
    """
    if _binary:
        root = os.path.join(_prop_directory, 'history')
    else:
        root = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'history')
    def __init__(self, url: str):
        self.domain = urlparse(url).netloc
        self.history_file = os.path.join(history.root, self.domain+'.txt')
        if not os.path.isdir(history.root):
            os.mkdir(history.root)

    def write(self, content: str or list, end: str = '\n') -> None:
        if isinstance(content, list):
            content: str  = '\n'.join(content)
        if content in self.read():
            return
        with open(self.history_file, 'a') as f:
            f.write(content+end)

    def read(self) -> set:
        if os.path.isfile(self.history_file):
            with open(self.history_file, 'r') as f:
                return set(f.read().rstrip().splitlines())
        else:
            return set()

class parser:
    """
    HTMLやURL解析
    spiderはaタグとimgタグから参照先URLを抽出し保存、html_extractionは任意のタグを抽出
    """
    status_messages = {400: 'Bad Request', 401: 'Unauthorized', 402: 'Payment Required', 403: 'Forbidden', 404: 'Not Found', 405: 'Method Not Allowed', 406: 'Not Acceptable', 407: 'Proxy Authentication Required', 408: 'Request Timeout', 409: 'Conflict', 410: 'Gone', 411: 'Length Required', 412: 'Precondition Failed', 413: 'Payload Too Large', 414: 'URI Too Long', 415: 'Unsupported Media Type', 416: 'Range Not Satisfiable', 417: 'Expectation Failed', 418: "I'm a teapot", 421: 'Misdirected Request', 422: 'Unprocessable Entity', 423: 'Locked', 424: 'Failed Dependency', 425: 'Too Early', 426: 'Upgrade Required', 428: 'Precondition Required', 429: 'Too Many Requests', 431: 'Request Header Fields Too Large', 451: 'Unavailable For Legal Reasons', 500: 'Internal Server Error', 501: 'Not Implemented', 502: 'Bad Gateway', 503: 'Service Unavailable', 504: 'Gateway Timeout', 505: 'HTTP Version Not Supported', 506: 'Variant Also Negotiates', 507: 'Insufficient Storage', 508: 'Loop Detected', 510: 'Not Extended', 511: 'Network Authentication Required'}
    def __init__(self, option, log, *, dl=None):
        self.option = option
        self.log = log
        self.parser = self.option['parser']
        self.dl = dl

    @staticmethod
    def get_rootdir(url: str) -> str or None:
        """
        ホームアドレスを摘出
        """
        if parser.is_url(url):
            result = urlparse(url)
            return result.scheme+'://'+result.hostname
        else:
            return None

    @staticmethod
    def query_dns(url: str):
        if parser.is_url(url):
            host = parser.get_hostname(url)
        else:
            host = url
        if host:
            i = socket.getaddrinfo(host, None)
            return i
        else:
            raise gaierror()

    @staticmethod
    def get_hostname(url: str) -> str or None:
        if parser.is_url(url):
            return urlparse(url).hostname
        else:
            return None

    @staticmethod
    def get_filename(url, name_only=True):
        if not isinstance(url, str):
            return url
        result = unquote(url.rstrip('/').split('/')[-1])
        if name_only:
            defrag = urldefrag(result).url
            return parser.delete_query(defrag)
        return result

    @staticmethod
    def splitext(url):
        if not isinstance(url, str):
            return url
        split = url.rstrip('/').split('.')
        if len(split) < 2 or not split[-1] or '/' in split[-1] or urlparse(url).path in {'', '/'}:
            return (url, '.html')
        else:
            return ('.'.join(split[:-1]), '.'+split[-1])

    @staticmethod
    def delete_query(url):
        if not isinstance(url, str):
            return url
        index = url.find('?')
        if 0 <= index:
            return url[:index]
        else:
            return url

    @staticmethod
    def is_url(url: str) -> bool:
        """
        引数に渡された文字列がURLか判別
        """
        return bool(re.match(r"https?://[\w!\?/\+\-_~=;\.,\*&@#\$%\(\)'\[\]]+", url))

    def html_extraction(self, source: bytes or str, words: dict) -> str:
        data = bs(source, self.parser)
        if 'css' in words:
            code: list = data.select(words.get('css'), limit=self.option.get('limit') or None)
        else:
            code: list = data.find_all(name=words.get('tags'), attrs=words['words'], limit=self.option.get('limit') or None)
        return '\n\n'.join(map(str, code))

    def is_success_status(self, returncode):
        if 200 <= returncode < 400:
            self.log(20, f'{returncode}: Success request')
            return True
        else:
            self.log(40, '{}: {}'.format(returncode, parser.status_messages.get(returncode, "unknown")))
            return False

    def delay_check(self):
        """
        指定されているインターバルがrobots.txtのcrawl_delayの数値以上か判定
        もしcrawl_delayの数値より少なかったらインターバルをcrawl_delayの数値に置き換える
        """
        delay = self.robots.delay()
        if delay is not None and self.option['interval'] < delay:
            self.log(30, f"it changed interval because it was shorter than the time stated in robots.txt  '{self.option['interval']}' => '{delay}'")
            self.option['interval'] = delay

    def _cut(self, list, get, cwd_url, response, root_url, downloaded, is_ok, info_dict, cut=True):
        data: dict = dict()
        did_host: set = set()
        dns = False
        start = self.option['start'] is None
        for tag in list:
            if isinstance(get, str):
                url: str = tag.get(get)
            else:
                for g in get:
                    url = tag.get(g)
                    if url:
                        break
                else:
                    continue
                url = url
            if not url or '#' in url or url in info_dict:
                continue
            if self.is_url(url):
                target_url: str = url
                dns = True
            else:
                target_url: str = urljoin(cwd_url, url)
                if not self.is_url(target_url):
                    continue
            if cut and not start:
                if target_url.endswith(self.option['start']):
                    start = True
                else:
                    continue
            if cut and ((self.option['noparent'] and (not target_url.startswith(response.url) and target_url.startswith(root_url))) or target_url in set(data.values()) or ((target_url.startswith(cwd_url) and  '#' in target_url) or (self.option['no_dl_external'] and not target_url.startswith(root_url)))):
                continue
            if cut and (self.option['download_name'] not in target_url or (self.option['no_downloaded'] and target_url in downloaded)):
                continue
            if self.option['debug']:
                self.log(20, f"found '{target_url}'")
            if self.option['save_robots'] and not is_ok(url):
                self.log(30, f'{target_url} is prohibited by robots.txt')
                continue
            if dns:
                try:
                    hostname = self.get_hostname(target_url)
                    if hostname not in did_host:
                        if not hostname:
                            raise gaierror()
                        if self.option['debug']:
                            self.log(20, f"querying the DNS server for '{hostname}' now...")
                        i = self.query_dns(hostname)
                except gaierror:
                    self.log(30, f"skiped {target_url} because there was no response from the DNS server")
                    continue
                except:
                    pass
                finally:
                    dns = False
                    did_host.add(hostname)
            data[url] = target_url
            if cut and 0 < self.option['limit'] <= len(data):
                break
        return data

    def _get_count(self):
        files = list(filter(lambda p: bool(re.match(re.escape(self.option['formated']).replace(r'%\(num\)d', r'\d+').replace(r'%\(file\)s', '.*').replace(r'%\(ext\)s', '.*'), p)), os.listdir()))
        if files:
            string = self.option['formated'].split('%(num)d')
            start = len(string[0])
            if string[1]:
                end = string[1][0]
                num = map(lambda p: int(p[start:p.find(end, start)]), files)
            else:
                num = map(lambda p: int(p[start:]), files)
            return max(num)+1
        return 0

    def spider(self, response, *, h=sys.stdout, session):
        """
        HTMLからaタグとimgタグの参照先を抽出し保存
        """
        temporary_list: list = []
        temporary_list_urls: list = []
        if '%(num)d' in self.option['formated']:
            count = self._get_count()
        else:
            count = 0          
        max = self.option['interval']+3
        info_file = os.path.join('styles', '.prop_info.json')
        if self.option['no_downloaded']:
            downloaded: set = h.read()
        else:
            downloaded: set = set()
        if (not os.path.isfile(os.path.join('styles', '.prop_info.json'))) and self.option['body'] and not self.option['start'] and not self.option['check_only'] and not (self.option['no_downloaded'] and response.url.rstrip('/') in downloaded):
            root = self.dl.recursive_download(response.url, response.text, count)
            count += 1
            WebSiteData: dict = {response.url: root}
            h.write(response.url.rstrip('/'))
        elif self.option['check_only']:
            WebSiteData: dict = {response.url: response.url}
        else:
            WebSiteData: dict = dict()
        if os.path.isfile(info_file):
            with open(info_file, 'r') as f:
                WebSiteData.update(json.load(f))
        root_url: str = self.get_rootdir(response.url)
        # ↑ホームURLを取得
        cwd_urls = [response.url]
        # ↑リクエストしたURLを取得
        # aタグの参照先に./~~が出てきたときにこの変数の値と連結させる
        if self.option['debug']:
            self.log(20, 'checking robots.txt...')
        try:
            self.robots = Parse(root_url, requests=True, headers=self.option['header'], proxies=self.option['proxy'], timeout=self.option['timeout'])
            is_ok = self.robots.can_crawl
            self.delay_check()
        except NotFoundError:
            is_ok = lambda *_: True
            if self.option['debug']:
                self.log(20, 'robots.txt was none')
        source = [response.content]
        print(f"\033[36mhistories are saved in '{h.history_file}'\033[0m", file=sys.stderr)
        for n in range(self.option['recursive']):
            for source, cwd_url in zip(source, cwd_urls):
                datas = bs(source, self.parser)
                if self.option['body']:
                    a_data: dict = self._cut(datas.find_all('a'), 'href', cwd_url, response, root_url, downloaded, is_ok, WebSiteData) #aタグ抽出
                    link_data: dict = self._cut(datas.find_all('link', rel='stylesheet'), "href", cwd_url, response, root_url, downloaded, is_ok, WebSiteData, cut=False) # rel=stylesheetのlinkタグを抽出
                if self.option['content']:
                    img_data: dict = self._cut(datas.find_all('img'), ['src', 'data-lazy-src', 'data-src'], cwd_url, response, root_url, downloaded, is_ok, WebSiteData) # imgタグ抽出
                self.option['header']['Referer'] = cwd_url
                if self.option['body']:
                    if not os.path.isdir('styles') and not self.option['check_only']:
                        os.mkdir('styles')
                        self.log(20, 'loading stylesheets...')
                        before_fmt = self.dl.option['formated']
                        self.dl.option['formated'] = os.path.join('styles', '%(file)s')
                        for from_url, target_url in tqdm(link_data.items(), leave=False, desc="'stylesheets'"):
                            with cache(target_url, self) as caches:
                                che = caches.get_cache(target_url)
                                if che:
                                    result = os.path.join('styles', os.path.basename(che))
                                    shutil.copy(che, result)
                                    self.log(20, f"using cache instead of downloading '{target_url}'") 
                                else:
                                    for i in range(self.option['reconnect']+1):
                                        try:
                                            if i == 0:
                                                self.log(20, f"request start: '{target_url}'")
                                            else:
                                                self.log(20, f"retrying {i}")
                                            res: requests.models.Response = session.get(target_url, timeout=self.option['timeout'], proxies=self.option['proxy'], headers=self.option['header'], verify=self.option['ssl'])
                                            if not self.is_success_status(res.status_code):
                                                break
                                            if self.option['debug']:
                                                tqdm.write(f"response speed: {res.elapsed.total_seconds()}s [{len(res.content)} bytes data]", file=sys.stderr)
                                            res.close()
                                            result = self.dl.recursive_download(res.url, res.content)
                                            caches.save(target_url, res.content)
                                            break
                                        except Exception as e:
                                            if i >= self.option['reconnect']-1:
                                                self.log(30, e)
                                            sleep(1)
                                            continue
                                WebSiteData[from_url] = result
                                if os.path.isdir('styles'):
                                    with open(info_file, 'w') as f:
                                        json.dump(WebSiteData, f, indent=4, ensure_ascii=False)
                        self.dl.option['formated'] = before_fmt
                    for from_url, target_url in tqdm(a_data.items(), leave=False, desc="'a tag'"):
                        for i in range(self.option['reconnect']+1):
                            try:
                                if i == 0:
                                    self.log(20, f"request start: '{target_url}'")
                                else:
                                    self.log(20, f"retrying {i}...")
                                res: requests.models.Response = session.get(target_url, timeout=self.option['timeout'], proxies=self.option['proxy'], headers=self.option['header'], verify=self.option['ssl'])
                                if not self.is_success_status(res.status_code):
                                    break
                                temporary_list.append(res.content)
                                temporary_list_urls.append(res.url)
                                h.write(target_url)
                                if self.option['debug']:
                                    tqdm.write(f"response speed: {res.elapsed.total_seconds()}s [{len(res.content)} bytes data]", file=sys.stderr)
                                res.close()
                                if self.option['check_only']:
                                    WebSiteData[target_url] = 'Exists' if self.is_success_status(res.status_code) else 'Not'
                                else:
                                    result = self.dl.recursive_download(res.url, res.content, count)
                                    count += 1
                                    WebSiteData[from_url] = result
                                    if os.path.isdir('styles'):
                                        with open(info_file, 'w') as f:
                                            json.dump(WebSiteData, f, indent=4, ensure_ascii=False)
                                break
                            except Exception as e:
                                if i >= self.option['reconnect']-1:
                                    self.log(30, e)
                                sleep(1)
                                continue
                        else:
                            if self.option['debug']:
                                self.log(20, f"didn't response '{target_url}'")
                            continue
                        sleep(round(uniform(self.option['interval'], max), 1))
                if self.option['content']:
                    for from_url, target_url in tqdm(img_data.items(), leave=False, desc="'img tag'"):
                        for i in range(self.option['reconnect']):
                            try:
                                if i == 0:
                                    self.log(20, f"request start: '{target_url}'")
                                else:
                                    self.log(20, f"retrying {i}")
                                res: requests.models.Response = session.get(target_url, timeout=self.option['timeout'], proxies=self.option['proxy'], headers=self.option['header'], verify=self.option['ssl'])
                                h.write(target_url)
                                if not self.is_success_status(res.status_code):
                                    break
                                if self.option['debug']:
                                    tqdm.write(f"response speed: {res.elapsed.total_seconds()}s [{len(res.content)} bytes data]", file=sys.stderr)
                                res.close()
                                if self.option['check_only']:
                                    WebSiteData[target_url] = 'Exists' if self.is_success_status(res.status_code) else 'Not'
                                else:
                                    result = self.dl.recursive_download(res.url, res.content, count)
                                    count += 1
                                    WebSiteData[from_url] = result
                                    if os.path.isdir('styles'):
                                        with open(info_file, 'w') as f:
                                            json.dump(WebSiteData, f, indent=4, ensure_ascii=False)
                                break
                            except Exception as e:
                                if i >= self.option['reconnect']-1:
                                    self.log(30, e)
                                continue
                        else:
                            if self.option['debug']:
                                self.log(20, f"didn't response '{target_url}'")
                        sleep(round(uniform(self.option['interval'], max), 1))
            cwd_urls = temporary_list_urls
            temporary_list_urls: list = []
            source = temporary_list
            temporary_list: list = []
            if self.option['debug']:
                self.log(20, f'{n+1} hierarchy... '+'\033[32m'+'done'+'\033[0m')
        if self.option['check_only']:
            for k, v in WebSiteData.items():
                print('{}  ... {}{}\033[0m'.format(k, '\033[32m' if v == 'Exists' else '\033[31m', v))
            sys.exit()
        elif os.path.isdir('styles'):
            with open(info_file, 'w') as f:
                json.dump(WebSiteData, f, indent=4, ensure_ascii=False)
        return WebSiteData

class downloader:
    """
    再帰ダウンロードやリクエスト&パースする関数を定義するクラス
    start_download以降の関数は再帰ダウンロード関連の関数
    """
    def __init__(self, url: str, option, parsers='html.parser'):
        self.url = url # リスト
        self.parser: str = parsers
        self.option = option
        self.session = requests.Session()
        logger = logging.getLogger('Log of Prop')
        self.log = logger.log
        self.parse = parser(self.option, self.log, dl=self)

    def start(self) -> None:
        """
        URLに対してリスエストを送る前準備と実行
        """
        methods: dict = {'get': self.session.get, 'post': self.session.post, 'put': self.session.put, 'delete': self.session.delete}
        instance: requests = methods.get(self.option['types'])
        if self.option['debug']:
            self.log(20, """
request urls: {0}
\033[35m[settings]\033[0m
{1}
            """.format(self.url, '\n'.join([f'\033[34m{k}\033[0m: {v}' for k, v in self.option.items()])))
        for url in self.url:
            try:
                hostname = self.parse.get_hostname(url)
                if not hostname:
                    self.log(40, f"'{url}' is not url")
                    continue
                if self.option['debug']:
                    self.log(20, f"querying the DNS server for '{hostname}' now...")
                i = self.parse.query_dns(hostname)
                if self.option['debug']:
                    self.log(20, f"request start {url} [{i[0][-1][0]}]")
                self.request(url, instance)
            except gaierror:
                self.log(20, f"skiped '{url}' because there was no response from the DNS server")
                continue
            except Exception as e:
                if self.option['caperror']:
                    self.log(40, f'\033[31m{str(e)}\033[0m')
                continue

    def request(self, url: str, instance) -> str or List[requests.models.Response, str]:
        self.option['formated']: str = self.option['format'].replace('%(root)s', self.parse.get_hostname(url))
        if self.option['types'] != 'post':
            r: requests.models.Response = instance(url, params=self.option['payload'], allow_redirects=self.option['redirect'], cookies=self.option['cookie'], auth=self.option['auth'], timeout=self.option['timeout'], proxies=self.option['proxy'], headers=self.option['header'], verify=self.option['ssl'], stream=True)
        else:
            if self.option['upload']:
                name, form = self.option['upload']
                with open(name, 'rb') as f:
                    if form:
                        upload_data = {form: (f.name, f, mimetypes.guess_type(f.name)[0])}
                    else:
                        upload_data = {f.name: f}
                    r: requests.models.Response = instance(url, allow_redirects=self.option['redirect'], cookies=self.option['cookie'], auth=self.option['auth'], proxies=self.option['proxy'], timeout=self.option['timeout'], headers=self.option['header'], verify=self.option['ssl'], files=upload_data, stream=True)
            elif self.option['json']:
                r: requests.models.Response = instance(url, json=self.option['payload'], allow_redirects=self.option['redirect'], cookies=self.option['cookie'], auth=self.option['auth'], proxies=self.option['proxy'], timeout=self.option['timeout'], headers=self.option['header'], verify=self.option['ssl'], stream=True)
            else:
                r: requests.models.Response = instance(url, data=self.option['payload'], allow_redirects=self.option['redirect'], cookies=self.option['cookie'], auth=self.option['auth'], proxies=self.option['proxy'], timeout=self.option['timeout'], headers=self.option['header'], verify=self.option['ssl'], stream=True)
        if self.option['debug'] and not self.option['info']:
            print(f'\n\033[35m[response headers]\033[0m\n\n'+'\n'.join([f'\033[34m{k}\033[0m: {v}' for k, v in r.headers.items()])+'\n', file=sys.stderr)
        if not self.parse.is_success_status(r.status_code):
            return
        if self.option['check_only'] and not self.option['recursive']:
            print(f'{url}  ... \033[32mExists\033[0m')
            return
        h = history(r.url)
        if self.option['recursive']:
            if self.option['filename'] is os.path.basename:
                self.option['filename']: str = '.'
            if self.option['check_only'] or self.option['filename'] is not None and not os.path.isfile(self.option['filename']):
                if not os.path.isdir(self.option['filename']):
                    os.mkdir(self.option['filename'])
                cwd = os.getcwd()
                os.chdir(self.option['filename'])
                self.log(20, 'parsing...')
                res = self.parse.spider(r, h=h, session=self.session)
                self.log(20, 'download... '+'\033[32m'+'done'+'\033[0m')
                self.start_conversion(res)
                os.chdir(cwd)
                return
            else:
                self.log(40, 'the output destination is not a directory or not set')
                sys.exit(1)
        elif self.option['info']:
            self._print(r, [r.headers], file=self.get_fmt(r))
            return
        elif self.option['search']:
            result = self.parse.html_extraction(r.text, self.option['search'])
            save_filename = self.get_fmt(r)
            if save_filename:
                with open(save_filename, 'w') as f:
                    f.write(result)
            else:
                print(result)
            return
        elif self.option['only_body']:
            try:
                s = bs(r.content, self.parser)
                save_filename = self.get_fmt(r)
                if save_filename:
                    with open(save_filename, 'w') as f:
                        f.write(s.text)
                else:
                    print(s.text)
            except Exception as e:
                self.log(40, e)
            return
        length = r.headers.get('content-length')
        save_filename = self.get_fmt(r)
        if save_filename:
            if length:
                with open(save_filename, 'wb') as f:
                    self.save(f.write, length, r)
            else:
                with open(save_filename, 'wb') as f:
                    f.write(r.content)
        else:
            self.save(tqdm.write, length, r)

    def get_fmt(self, r):
        if self.option['filename']:
            if self.option['filename'] is os.path.basename:
                save_filename = self.parse.get_filename(r.url)
            elif os.path.isdir(self.option['filename']):
                save_filename: str = os.path.join(self.option['filename'], self.parse.get_filename(r.url))
            else:
                save_filename: str = self.option['filename']
            return save_filename
        else:
            return None

    def save(self, write, length, r):
        if write == tqdm.write:
            try:
                if 1048576 <= int(length) and not self.ask_continue("The output will be large, but they will be printed to stdout.\nContinue?"):
                    return
            except:
                pass
            with tqdm(total=int(length) if length else None, unit="B", unit_scale=True) as p:
                for b in r.iter_content(chunk_size=16384):
                    write(b.decode(errors='backslashreplace'), end='')
                    p.update(len(b))
        else:
            with tqdm(total=int(length) if length else None, unit="B", unit_scale=True) as p:
                for b in r.iter_content(chunk_size=16384):
                    write(b)
                    p.update(len(b))

    def _print(self, response, output=None, file=None) -> None:
        if file:
            sys.stdout = open(file, 'w')
        tqdm.write('\n\033[35m[histories of redirect]\033[0m\n')
        if not response.history:
            tqdm.write('-')
        else:
            for h in response.history:
                tqdm.write(h.url)
                tqdm.write('↓')
            tqdm.write(response.url)
        tqdm.write('\033[35m[cookies]\033[0m\n')
        if not response.cookies:
            tqdm.write('-')
        else:
            for c in response.cookies:
                tqdm.write(f'\033[34m{c.name}\033[0m: {c.value}')
        tqdm.write('\n\033[35m[response headers]\033[0m\n')
        for i in output:
            if isinstance(i, (str, bytes)):
                tqdm.write(str(i), end='')
            else:
                for k, v  in i.items():
                    tqdm.write(f'\033[34m{k}\033[0m: {v}')
        sys.stdout.flush()
        if file:
            sys.stdout.close()
            sys.stdout = sys.__stdout__

    def _split_list(self, array, N):
        n = math.ceil(len(array) / N)
        return [array[index:index+n] for index in range(0, len(array), n)]

    def start_conversion(self, info: tuple) -> None:
        """
        ファイルパス変換をスタートする
        """
        if self.option['conversion'] and self.option['body']:
            self.log(20, 'convert... ')
            self.local_path_conversion(info)
            self.log(20, 'convert... '+'\033[32m' + 'done' + '\033[0m')

    def recursive_download(self, url: str, source: bytes or str, number: int=0) -> str:
        """
        HTMLから見つかったファイルをダウンロード
        """
        exts = self.parse.splitext(self.parse.delete_query(url))
        # フォーマットを元に保存ファイル名を決める
        save_filename: str = self.option['formated'].replace('%(file)s', ''.join(self.parse.splitext(self.parse.get_filename(url)))).replace('%(num)d', str(number)).replace('%(ext)s', exts[1].lstrip('.'))
        if os.path.isfile(save_filename) and not self.ask_continue(f'{save_filename} has already existed\nCan I overwrite?'):
            return save_filename
        while True:
            try:
                if isinstance(source, str):
                    with open(save_filename, 'w') as f:
                        f.write(source)
                else:
                    with open(save_filename, 'wb') as f:
                        f.write(source)
                sleep(0.5)
                break
            except Exception as e:
                # エラーがでた場合、Warningログを表示し続けるか標準入力を受け取る[y/n]
                self.log(30, e)
                if self.ask_continue('continue?'):
                    continue
                else:
                    return
        if self.option['debug']:
            self.log(20, f'saved: {url} => {os.path.abspath(save_filename)}')
        return save_filename

    def local_path_conversion(self, conversion_urls) -> None:
        if self.option['conversion'] and self.option['body']:
            if self.option['multiprocess']:
                to_path = list(conversion_urls.values())
                splited_path_list = self._split_list(to_path, 4) # 4分割
                processes: list = []
                for path in splited_path_list[1:]:
                    # 分けた内3つをサブプロセスで変換する
                    # 残り一つはメインプロセスで変換
                    p = Process(target=self.conversion_path, args=(path, conversion_urls, self.option['formated']))
                    p.start()
                    processes.append(p)
                try:
                    self.conversion_path(splited_path_list[0], conversion_urls, self.option['formated'])
                finally:
                    for n, p in enumerate(processes):
                        # 作成した全てのサブプロセスの終了を待つ
                        p.join()
                        self.log(20, f'#{n+1}'+'\033[32m'+'done'+'\033[0m')
            else:
                self.conversion_path(list(conversion_urls.values()), conversion_urls, self.option['formated'])

    def conversion_path(self, task, all_download_data, save_fmt: str) -> None:
        # URL変換
        for path in task:
            while True:
                try:
                    if not path.endswith('.html'):
                        break
                    with open(path, 'r') as f:
                        source: str = f.read()
                    for from_, to in all_download_data.items():
                        source = source.replace(from_, to)
                    with open(path, 'w') as f:
                        f.write(source)
                    if self.option['debug']:
                        self.log(20, f"converted '{path}'")
                    break
                except Exception as e:
                    self.log(30, f'pid: {os.getpid()} {e}')
                    if self.ask_continue('continue?'):
                        continue
                    else:
                        break

    if platform.system() == 'Windows':
        def receive(self):
            result = msvcrt.getch()
            return str(result).lower()
    else:
        def receive(self):
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            new = termios.tcgetattr(fd)
            new[3] &= ~termios.ICANON
            new[3] &= ~termios.ECHO
            try:
                termios.tcsetattr(fd, termios.TCSANOW, new)
                result = sys.stdin.read(1).lower()
            finally:
                termios.tcsetattr(fd, termios.TCSANOW, old)
            return result

    def ask_continue(self, msg) -> bool:
        while True:
            tqdm.write(f'{msg}[y/N]\n')
            res = ''
            answer = self.receive()
            while answer != '\n':
                res += answer
                tqdm.write(answer, end='')
                sys.stdout.flush()
                answer = self.receive()
            if res in {'y', 'n', 'yes', 'no'}:
                break
            print('\033[1A\r', end='')
        print('\033[1A\r\033[0J', end='')
        print('\033[1A\r\033[0J', end='', file=sys.stderr)
        sys.stdout.flush()
        sys.stderr.flush()
        return res in {'y', 'yes'}

def tor(port=9050):
    return {'http': f'socks5://127.0.0.1:{port}', 'https': f'socks5://127.0.0.1:{port}'}

def help() -> None:
    print("""
<usage>
prop <option> URL [URL...]
if you want to read the URL from standard input, please use '-' instead of URL

<List of options>
-o, --output [file path]
Specify the output destination file
Default setting is standard output

-O
Download with the same name as the download source file name

-i, --ignore
Even if set timeout, it ignore

-t, --timeout [timeout time (number)]
Set the timeout time
Please specify number
Also, the -i option takes precedence over this option

-x, --method [method]
Communicate by specifying the communication method
The default is get
Communication that can be specified with -x, --method option

- get
- post
- delete
- put

-S, --ignore-SSL
Ignore SSL certificate validation

-d, --data param1=value1 param2=value2 
Specify the data and parameters to send
Specify as follows
prop -d q=hogehoge hl=fugafuga URL
Please specify the -j option when sending in json format

-j, --json
Send data in json format

-H, --header HeaderName1=HeaderInformation1 HeaderName2=HeaderInformation2 
Communicate by specifying the header

-a, --fake-user-agent [BrowserName]
It use the automatically generated User-Agent
In addition, it is also possible to specify the name of the browser to automatically generate the User-Agent

-c, --cookie cookie name 1 = information 1 cookie name 2 = information 2
Communicate by specifying the cookies

-X, --proxy [proxy]
Specify the proxy to use for communication

--tor [port number (optional)]
It use tor as a proxy
If you omit the port number, 9050 will be used
And, there are some things you need to do before using this option
Windows:
Just run tor.exe

Mac:
Please enter the following command to start tor
$ brew services start tor

Linux:
Please enter the following command to start tor
$ sudo service tor start

-F, --information
Outputs only status code, redirect history, cookie information, response header information
If you have specified this option and want to output to a file, use> (redirect) instead of the -o option

-s, --search-words [words]
Extracts and outputs the code such as the specified tag, class, id, etc. from the source code of the site
If you specify more than one, separate them with ',' (don't use a space)
Example of use
prop -s tags=a,img,script class=test [URL]

>>> Extract and display the code of a tag, img tag, and script tag from the test class

Also, if limit=number or use -M, --limit option, only the specified number will be extracted
Example of use
prop -s tags=a limit=2 [URL]

>>> Extract a tag from the top to the second

Below is an example of attribute specification (there are others)
class=class name
id=id
text=Contents of tag(character string)
tags=tag name
href=reference
src=reference

And, you can also use the css selector without using the above

prop -s "a, script" [URL]

-Y, --only-body
Show the only body if contents are html
(not body tag)

-M, --limit [num]
Specify the number of '-s', '--search' result or the number of recursive download files (-r, --recursive option)

-e, --no-catch-error
No output even if an error occurs

-R, --read-file [file path]
Reads the URL to download from the specified file

-B, --basic-auth [user id] [password]
Perform Basic authentication

-l, --no-redirect
Disable redirection

-u, --upload file [path] [form (optional)]
You can specify the file to upload at the time of post (multiple files cannot be specified)

-D, --debug
Display detailed information at the time of request

-----Below are the options related to recursive downloads-----

-r, --recursive [Recursion count (optional)]
Recursively download site text links
When specifying this option, be sure to specify the output destination with the -o option (specify "directory" instead of file)
Also, if you specify a directory that doesn't exist, a new one will be created.)
If you don't specify the number of recursion, it will be executed as if 1 was specified
Also, if the -nE option isn't specified, local path conversion will be performed automatically

-nc, --no-content
It don't download images

-nb, --no-body
Downloads only images (if this option is specified, the number of recursion will be 1 even if the number of recursion is specified)

-np, --no-parent
It don't download the parent directory of the download source URL

-nE, --no-conversion
It don't convert web page URL references to local paths

-dx, --download-external
Also download external address sites

-n, --download-filename [string]
Only download files include specified string

-f, --format [format]
You can specify the format of the file save name at the time of recursive download
If "%(file)s" or "%(num)d" aren't included in the character string, it won't be applied because saved name isn't changed for each file

Ex: Suppose there are text links https://example.com/2.html and https://example.com/3.html in https://example.com

prop -r -f "%(num)d-%(root)s-%(file)s" https://example.com

>>> https://example.com saved as 0-example.com, http://example.com/2 saved as 1-example.com-2.html, http://example.com/3 saved as 2-example.com-3.html

prop -r -f "%(num)d.%(ext)s" https://www.example.com

>>> https://example.com saved as 0.html, https://example.com/2.html saved as 1.html, https://example.com/3.html saved as 2.html

Specifiable format

- %(root)s
  Hostname

- %(file)s
  Web page file name (character string after the last '/'  in the URL of the site)
  And, this is automatically given an extension

- %(ext)s
  File extension (not including '.')

- %(num)d
  Consecutive numbers

-I, --interval [seconds]
Specifies the interval for recursive downloads
The default is 1 second

-m, --multiprocess
It use multi-thread processing when converting the URL reference destination of the downloaded
What you do with multithreading The processing time is greatly reduced
Recommended to specify

-nd, --no-downloaded
It don't download urls written in histories
This option doesn't work properly if you delete the files under the {history_directory} (even if you delete it, it will be newly generated when you download it again)

-----The following special options-----

-V, --version
Show the version that you are using

--purge-log
Remove log file

--purge-history
Remove all histories

--purge-cache
Remove all caches

-C, --check
It doesn't download, only checks if the specified URL exists
Checks recursively when used with the -r option

--config-file
Show the config file

--log-file
Show the file which logs are written

--history-directory
Show the directory which files which histories are written are stored

--cache-directory
Show the directory which caches(stylesheet) were stored

-U, --upgrade
Update the prop

--update-cache
Update downloaded caches
And, if you use this option in the directory that 'styles' directory exists, files in the 'styles' directory will be also updated

-p, --parse [file path (optional)]
Get HTML from file or standard input and parse it
You can use the -s option to specify the search tag, class, and id
If you specify a URL when you specify this option, an error will occur

[About parser and default settings]

The default HTML parser is html.parser, but you can also use an external parser
When using lxml
(1) Enter "pip install lxml" to install lxml
(2) Change the value of "parser" in {config_file} as follows
{
    "parser": "lxml"
}
You can also change the default settings by changing the contents of {config_file}
Setting Example
{
    "timeout": (3, 10),
    "header": {
        "User-Agent": "test"
    },
    "proxy": {
        "http": "https://IPaddress:PortNumber",
        "https": "https://IPaddress:PortNumber"
    },
}
The options that can be changed are as follows
{
    "types": "get",
    "timeout": [3.0, 60.0],
    "redirect": true,
    "search": false,
    "header": null,
    "cookie": null,
    "proxy": null,
    "auth": null,
    "recursive": 0,
    "body": true,
    "content": true,
    "conversion": true,
    "reconnect": 5,
    "caperror": true,
    "noparent": false,
    "no_downloaded": false,
    "interval": 1,
    "format": "%(file)s",
    "info": false,
    "multiprocess": false,
    "ssl": true,
    "parser": "html.parser",
    "no_dl_external": true,
    "save_robots": true // this recommended to specify true
}
""".replace("{config_file}", setting.config_file).replace("{log_file}", setting.log_file).replace('{history_directory}', history.root))

def conversion_arg(args) -> list:
    result: list = []
    for a in args:
        if a.startswith('-') and not a.startswith('--') and 2 < len(a) and not a in {'-np', '-nc', '-nb', '-nE', '-ns', '-nd', '-dx', '-st'}:
            results: str = '-'+'\n-'.join(a[1:])
            result.extend(results.splitlines())
        else:
            result.append(a)
    return result

def _argsplit(args):
    result: list = []
    continue_: str = None
    a = args.split(' ')
    for v in a:
        if (v.startswith("'") and not v.endswith("'")) or (v.startswith('"') and not v.endswith('"')):
            continue_ = v[0]
            s = [v.strip(continue_)]
        elif continue_ and v.endswith(continue_):
            s.append(v.strip(continue_))
            continue_ = None
            result.append(' '.join(s))
        elif continue_:
            s.append(v)
        else:
            result.append(v.strip("'\""))
    return result

def argument() -> (list, dict, logging.Logger.log):
        option: setting = setting()
        option.config_load()
        skip: int = 1
        url: list = []
        arg = conversion_arg(sys.argv)
        if len(arg) == 1:
            print("""
prop <options> URL [URL...]

\033[33mIf you want to see help message, please use '-h', '--help' options and you will see help\033[0m""")
            sys.exit()
        for n, args in enumerate(arg):
            if skip:
                skip -= 1
                continue
            if args == '-h' or args == '--help':
                help()
                sys.exit()
            elif args == '-V' or args == '--version':
                print(str(VERSION))
                sys.exit()
            elif args == '-o' or args == '--output':
                # 出力先ファイルの設定
                try:
                    filename: str = arg[n+1]
                except IndexError:
                    error.print(f"{args} [filename]\nPlease specify value of '{args}'")
                if filename != '-':
                    option.config('filename', os.path.join('.', filename))
                    option.config('output', False)
                skip += 1
            elif args == '-O':
                option.config('filename', os.path.basename)
                option.config('output', False)
            elif args == '-t' or args == '--timeout':
                try:
                    timeout: int = arg[n+1]
                except IndexError:
                    error.print(f"{args} [timeout]\nPlease specify value of '{args}'")
                if option.options.get('notimeout') is None:
                    try:
                        option.config('timeout', float(timeout))
                    except ValueError:
                        error.print(f"'{timeout}' isn't int or float\nPlease specify int or float")
                skip += 1
            elif args == '-i' or args == '--ignore':
                option.config('timeout', None)
                option.config('notimeout', True)
            elif args == '-x' or args == '--method':
                try:
                    method = arg[n+1].lower()
                except IndexError:
                    error.print(f"{args} [method]\nPlease specify value of '{args}'")
                if method in {'get', 'post', 'put', 'delete'}:
                    option.config('types', method)
                else:
                    error.print(f"'{method}' is unknown method")
                skip += 1
            elif args == '-S' or args == '--ignore-SSL':
                option.config('ssl', False)
            elif args == '-a' or args == '--fake-user-agent':
                try:
                    _stderr = sys.stderr
                    with open(os.devnull, "w") as null:
                        sys.stderr = null
                        ua = UserAgent()
                        sys.stderr = _stderr
                except Exception as e:
                    sys.stderr = _stderr
                    error.print(str(e))
                try:
                    fake = ua[arg[n+1]]
                    skip += 1
                except (IndexError, FakeUserAgentError):
                    fake = ua.random
                option.options['header']['User-Agent'] = fake
            elif args == '-d' or args == '-H' or args == '--data' or args == '--header' or args == '-c' or args == '--cookie':
                params: dict = dict()
                header: dict = dict()
                for d in arg[n+1:]:
                    i = d.split('=', 1)
                    if len(i) == 2:
                        if args == '-d' or args == '--data':
                            params[i[0]] = i[1]
                        else:
                            header[i[0]] = i[1]
                        skip += 1
                    else:
                        break
                if not params and not header:
                    error.print(f"{args} [Name=Value] [Name=Value]...\nPlease specify the value of the '{args}' option")
                if args == '-d' or args == '--data':
                    option.config('payload', params)
                elif args == '-c' or args == '--cookie':
                    option.config('cookie', params)
                else:
                    option.options['header'].update(header)
            elif args == '-j' or args == '--json':
                option.config('json', True)
            elif args == '-s' or args == '--search-words':
                try:
                    word = {'words': {}, 'limit': None}
                    for n, i in enumerate(arg[n+1:]):
                        fl = i.split('=', 2)
                        if (n == 0 and len(fl) == 1) or re.match(r'.*\[.*=.*\]$', i):
                            word['css'] = i
                            skip += 1
                            break
                        elif len(fl) == 2:
                            if  fl[0] != 'limit' and fl[0] != 'tags':
                                word['words'][fl[0]] = fl[1].split(',')
                            elif fl[0] == 'tags':
                                word['tags'] = fl[1].split(',')
                            else:
                                option.config('limit', int(fl[1]))
                            skip += 1
                        else:
                            break
                    option.config('search', word)
                except IndexError:
                    error.print(f"The specifying the argument of the '{args}' option is incorrect")
                except ValueError:
                    error.print(f'{fl[1]} is not number\nPlease specify number')
            elif args == '-Y' or args == '--only-body':
                option.config('only_body', True)
            elif args == '-l' or args == '--no-redirect':
                option.config('redirect', False)
            elif args == '-D' or args == '-D': 
                option.config('debug', True)
            elif args == '-u' or args == '--upload':
                try:
                    path = arg[n+1]
                    skip += 1
                except IndexError:
                    error.print(f"{args} [filepath]\nPlease specify value of '{args}'")
                try:
                    form = arg[n+2]
                    skip += 1
                except IndexError:
                    form = None
                if os.path.exists(path):
                    option.config('upload', (path, form))
                else:
                    error.print(f"The existence couldn't be confirmed: {path}")
                option.config('types', 'post')
            elif args == '-X' or args == '--proxy':
                try:
                    proxy_url: str = arg[n+1]
                except IndexError:
                    error.print(f"{args} [Proxy]\nPlease specify value of '{args}'")
                option.config('proxy', {"http": proxy_url, "https": proxy_url})
                skip += 1
            elif args == '-R' or args == '--read-file':
                try:
                    file: str = arg[n+1]
                except IndexError:
                    error.print(f"{args} [filepath]\nPlease specify value of '{args}'")
                urls: list = []
                options: list = []
                with open(file, 'r') as f:
                    instruct = list(filter(lambda s: s != '', f.read().splitlines()))
                for n, a in enumerate(instruct):
                    del sys.argv[1:]
                    sys.argv.extend(_argsplit(a))
                    url, log, option = argument()
                    urls.append(url)
                    options.append(option)
                return urls, log, options
            elif args == '-B' or args == '--basic-auth':
                try:
                    user: str = arg[n+1]
                    password: str = arg[n+2]
                    option.config('auth', HTTPBasicAuth(user, password))
                    skip += 2
                except:
                    error.print(f"{args} [UserName] [Password]\nThe specifying the argument of the '{args}' option is incorrect")
            elif args == '-r' or args == '--recursive':
                try:
                    number: int = int(arg[n+1])
                    skip += 1
                except (ValueError, IndexError):
                    number: int = 1
                option.config('recursive', number)
                result1, result2 = ('-nc' in arg or '--no-content' in arg), ('-nb' in arg or '--no-body' in arg)
                if result1:
                    option.config('content', False)
                if result2:
                    option.config('body', False)
                if result1 and result2:
                    error.print("'-nc' and '-nb' options cannot be used together")
                    sys.exit(1)
            elif args == '-st' or args == '--start':
                try:
                    option.config("start", arg[n+1])
                    skip += 1
                except IndexError:
                    error.print(f"{args} [StartName]\nPlease specify value of '{args}'")
            elif args == '-n' or args == '--download-filename':
                try:
                    option.config('download_name', arg[n+1])
                    skip += 1
                except IndexError:
                    error.print(f"{args} [string]\nPlease specify value of '{args}'")
            elif args == '-np' or args == '--no-parent':
                option.config('noparent', True)
            elif args in {'-nc', '-nb', '--no-content', '--no-body', '--update-cache', '-U', '--upgrade'}:
                continue
            elif args == '-M' or args == '--limit':
                try:
                    limit = int(arg[n+1])
                    skip += 1
                except IndexError:
                    error.print(f"{args} [limit]\nPlease specify value of '{args}'")
                except ValueError:
                    error.print('Please specify a number for the value of limit')
                option.config('limit', limit)
            elif args == '-e' or args == '--no-catch-error':
                option.config('caperror', False)
            elif args == '-dx' or args == '--download-external':
                option.config('no_dl_external', False)
            elif args == '-nE' or args == '--no-conversion':
                option.config('conversion', False)
            elif args == '-nd' or args == '--no-downloaded':
                option.config('no_downloaded', True)
            elif args == '-f' or args == '--format':
                try:
                    string: str = arg[n+1]
                except IndexError:
                    error.print(f"{args} [format]\nPlease specify value of '{args}'")
                if '%(file)s' in string or '%(num)d' in string:
                    if re.match(r'%\(num\)d[0-9]', string) or ('%(file)s' in string and (not string.endswith('%(file)s') or 1 < string.count('%(file)s'))) or (1 < string.count('%(num)d')) or any(map(string.__contains__, ['%(num)d%(file)s', '%(num)d%(ext)s'])):
                        print("""\033[33mSorry, about format, there are the following restrictions because it won't be able to generate an accurate serial number

- '%(file)s' and '%(ext)s' format can only be at the end

- '%(num)d' format cannot be included more than one

- Numbers cannot be used immediately after '%(num)d'

- '%(num)d%(file)s' and '%(num)d%(ext)s' cannot include in format\033[0m""")
                        sys.exit(1)
                    option.config('format', string)
                else:
                    option.log(30, '\033[33mFormat specified by you isn\'t applied because "%(file)s" or "%(num)d" aren\'t in it\nIf you want to know why it isn\'t applied without them, please see help message for more information\033[0m')
                skip += 1
            elif args == '-F' or args == '--information':
                option.config('info', True)
            elif args == '-I' or args == '--interval':
                try:
                    interval: float = float(arg[n+1])
                    option.config('interval', interval)
                    skip += 1
                except IndexError:
                    error.print(f"{args} [interval]\nPlease specify value of '{args}'")
                except ValueError:
                    error.print(f"Please specify int or float to value of '{args}'")
            elif args == '-m' or args == '--multiprocess':
                option.config('multiprocess', True)
            elif args == '--tor':
                try:
                    port = int(arg[n+1])
                    skip += 1
                except (IndexError, ValueError):
                    port = 9050
                Tor = tor(port)
                option.config('proxy', Tor)
            elif args == '-C' or args == '--check':
                option.config('check_only', True)
                option.config('filename', os.getcwd())
            elif args == '-p' or args == '--parse':
                try:
                    path = arg[n+1]
                    with open(path, 'r') as f:
                        html = f.read()
                    skip += 1
                except (IndexError, FileNotFoundError):
                    html = sys.stdin.read()
                option.config('parse', html)
            elif args == "--config-file":
                print(setting.config_file)
                sys.exit()
            elif args == "--log-file":
                print(setting.log_file)
                sys.exit()
            elif args == "--history-directory":
                print(history.root)
                sys.exit()
            elif args == "--cache-directory":
                print(cache.root)
                sys.exit()
            elif args == "--purge-log":
                if os.path.isfile(setting.log_file):
                    os.remove(setting.log_file)
                    print('done')
                else:
                    print('No log file')
                sys.exit()
            elif args == "--purge-history":
                if os.path.isdir(history.root):
                    files = len(glob.glob(os.path.join(history.root, "**"), recursive=True))
                    shutil.rmtree(history.root)
                    print(f'Removed: {files}')
                else:
                    print('No history')
                sys.exit()
            elif args == "--purge-cache":
                if os.path.isdir(cache.root):
                    files = len(glob.glob(os.path.join(cache.root, "**"), recursive=True))
                    shutil.rmtree(cache.root)
                    print(f'Removed: {files}')
                else:
                    print('No cache')
                sys.exit()
            else:
                url.append(args)
        return url, option.fh.file, option.options

def main() -> None:
    url, log_file, option = argument()
    if '--update-cache' in sys.argv:
        cache.update(option if isinstance(option, dict) else setting.options)
        sys.exit()
    elif '-U' in sys.argv or '--upgrade' in sys.argv:
        if _binary:
            res = requests.get("https://api.github.com/repos/mino-38/prop/releases", timeout=option['timeout'], proxies=option['proxy'], headers=option['header'], verify=option['ssl'])
            new_version = res.json()[0]["tag_name"]
            if VERSION < parse(new_version):
                with open(os.path.join(tempfile.gettempdir(), "prop-updater.bin"), "wb") as f, open(os.path.join(tempfile.gettempdir(), "prop-updater.sh"), "w") as s:
                    f.write(requests.get("https://github.com/mino-38/prop/releases/latest/download/prop", timeout=option['timeout'], proxies=option['proxy'], headers=option['header'], verify=option['ssl']).content)
                    s.write("""
function on_error () {
    echo -e "\\n\\033[33mFaild update\\nIf you run as root, this problem may solve\\033[0m"
    exit 1
}

trap on_error ERR

mv %(new_file)s %(bin_file)s
chmod a+rx %(bin_file)s
echo "Updated to version '%(version)s'"
rm %(script)s
                """ % {"bin_file": sys.executable, "new_file": f.name, "script": s.name, "version": new_version})
                subprocess.Popen("bash {}".format(s.name), shell=True, close_fds=True)
        else:
            subprocess.run(["pip", "install", "--upgrade", "prop-request"])
        sys.exit()
    for index, link in enumerate(url):
        if link == '-':
            link = sys.stdin.readline().rstrip()
        elif not parser.is_url(link):
            link = 'http://' + link
        url[index] = link
    with log_file:
        if url != [] and not (isinstance(option, dict) and option['parse']):
            if isinstance(option, list):
                dl: downloader = downloader(url[0], option[0], option[0]['parser'])
                dl.start()
                for u, o in zip(url[1:], option[1:]):
                    dl.url = u
                    dl.option = o
                    dl.parse.option = o
                    dl.start()
            else:
                dl: downloader = downloader(url, option, option['parser'])
                dl.start()
        elif option['parse']:
            dl: downloader = downloader(url, option, option['parser'])
            if option['only_body']:
                s = bs(option['parse'], dl.parser)
                result = s.text
            else:
                result = dl.parse.html_extraction(option['parse'], option['search'])
            if option['filename']:
                with open(option['filename'], 'w') as f:
                    f.write(result)
            else:
                print(result)
        elif url == []:
            error.print('Missing value for URL\nPlease specify URL')

if __name__ == '__main__':
    main()
