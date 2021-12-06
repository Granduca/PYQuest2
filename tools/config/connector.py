"""Service file for bot connection"""
from os.path import abspath, dirname, join

this_file_path = abspath(dirname(__file__))

"""TOKEN"""
token_file = "token.txt"  # file with token WARNING -> relative path
token_file_path = join(this_file_path, token_file)
with open(token_file_path) as token:
    TOKEN = token.readline()

"""PROXY"""
proxy_head = 'socks5h://'

proxy_file = "proxy.txt"  # file with proxy WARNING -> relative path
proxy_file_path = join(this_file_path, proxy_file)
with open(proxy_file_path) as proxy_f:
    proxy_address = proxy_f.readline()

proxy = "{}{}".format(proxy_head, proxy_address)
BOT_REQUEST_KWARGS = {
        'proxy_url': proxy,
        'con_pool_size': 8  # what is it connection pool size?
    }
