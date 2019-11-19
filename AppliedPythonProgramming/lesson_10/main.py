import os
import sys
import http.client
from urllib import request, parse
import xml.etree.ElementTree as Et
from html import parser as html_parser


BASE = os.path.dirname(__file__)

SITE_ADDR = 'info.cern.ch'

FILE_LOCATION = 'hypertext/WWW/Help.html'

URL = 'http://{}/{}'.format(SITE_ADDR, FILE_LOCATION)


def url_parse_task():
	parsed = parse.urlparse(URL)
	print(parsed)
	print(parsed[1])
	print(parsed[2] + parsed[3] + parsed[4] + parsed[5])
	print()

	built_url = parse.urlunparse(parsed)
	print(built_url)


def http_connection_task():
	try:
		server = http.client.HTTPConnection(SITE_ADDR, 80)
		server.request('GET', FILE_LOCATION)
		response = server.getresponse()
	except:
		info = sys.exc_info()
		print('Error HTTPConnection:\n', info[0], info[1])
		sys.exit()

	print('...reply...')
	if response.status == 200:
		with open('{}/url1.txt'.format(BASE), 'wb') as f:
			read_response = response.read()
			f.write(read_response)
			print(read_response)
		response.close()
	else:
		print('Error:', response.status, response.reason)

	print('...ready')


def http_request_task():
	print('Start...')

	remote_file = request.urlopen(URL)
	with open('{}/url2.html'.format(BASE), 'wb') as f:
		f.write(remote_file.read())

	chrome = '/usr/bin/google-chrome'

	os.execl(chrome, chrome, '{}/url2.html'.format(BASE))

	remote_file.close()

	print('..ready')


def print_xml(node, indent=''):
	print(indent, node.tag, node.attrib)
	if not node.getchildren():
		if node.text:
			print(indent + '\t', node.text)
	else:
		for child in node:
			print_xml(child, indent + '\t')


def xml_task():
	root = Et.parse('data.xml')
	print_xml(root.getroot())


class CustomHtmlParser(html_parser.HTMLParser):

	INDENT = ''

	def error(self, message):
		print('Error:', message)

	def handle_starttag(self, tag, attrs):
		print('{}(start)'.format(tag), attrs, ' ', end='')
		CustomHtmlParser.INDENT += '    '

	def handle_endtag(self, tag):
		print('{}(end)'.format(tag))
		CustomHtmlParser.INDENT = CustomHtmlParser.INDENT[:len(CustomHtmlParser.INDENT) - 4]

	def handle_data(self, data):
		if data and str(data).strip() != '':
			print('\n{}'.format(CustomHtmlParser.INDENT), data)


def html_task():
	site_addr = 'bank.gov.ua'
	file_location = '/markets/exchangerates?date=19.11.2019&period=daily'
	url = 'https://{}{}'.format(site_addr, file_location)

	print('Start...')

	remote_file = request.urlopen(url)
	with open('nbu_course.html', 'wb') as f:
		f.write(remote_file.read())
	remote_file.close()

	print('..ready\n')

	with open('nbu_course.html', 'r') as html_file:
		custom_parser = CustomHtmlParser()
		custom_parser.feed(html_file.read())


if __name__ == '__main__':
	# url_parse_task()
	# http_connection_task()
	# http_request_task()
	# xml_task()
	html_task()


"""
	print(root[1].attrib['list'], root[1][0].attrib['name'], root[1][0][2].text)

	for serv in root.iter('service'):
		print(serv.attrib)
	print()

	for furn in root.iter('furniture'):
		print(furn.attrib['name'], ':')
		for serv in furn.findall('service'):
			sa = serv.get('sale')
			de = serv.get('delivery')
			mn = serv.get('mounting')
			gu = serv.get('guarantee')
			if sa:
				print(sa, ' ', end='')
			if de:
				print(de)
			if mn:
				print(mn, ' ', end='')
			if gu:
				print(gu)
		print()
"""
