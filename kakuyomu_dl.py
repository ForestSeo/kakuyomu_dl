# coding: UTF-8

# 警告: README.md を必ず読んでください
# WARNING: Be sure to read README.md


import os
from pathlib import Path
from bs4 import BeautifulSoup
import requests
import time

# PDF作成をreportlabで行う
from reportlab.platypus import BaseDocTemplate, PageTemplate
from reportlab.platypus import Paragraph, PageBreak, FrameBreak
from reportlab.platypus.flowables import Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4, portrait, mm
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase import cidfonts
from reportlab.platypus.frames import Frame


# 現在のファイルのディレクトリに移動
this_file = Path(os.path.abspath(__file__))
os.chdir(this_file.parent)


# /works/<num> からChapterのURLを取得
def get_urls(url):
	data = requests.get(url)
	soup = BeautifulSoup(data.text, "html.parser")

	urls = soup.select("li.widget-toc-episode > a")
	lst = [f"https://kakuyomu.jp{u.get('href')}" for u in urls]
	return lst


# get_urlsで取得したChapterにアクセスしてテキストを取ってきてPDFに変換
def create_pdf(url, file_name_start):
	data = requests.get(url)
	soup = BeautifulSoup(data.text, "html.parser")

	title = soup.find("p", class_="widget-episodeTitle").text

	content = soup.find("div", class_="widget-episodeBody").text
	content = content.replace("\n", "<br/>")


	pdfmetrics.registerFont(cidfonts.UnicodeCIDFont("HeiseiMin-W3"))

	doc = BaseDocTemplate(f"./output/{file_name_start}{title}.pdf", title="カクヨム", pagesize=portrait(A4))

	frames = [
	    Frame(5 * mm, 5 * mm, 20 * cm, 29 * cm, showBoundary=0),
	]

	page_template = PageTemplate("frames", frames=frames)
	doc.addPageTemplates(page_template)

	style_dict = {
		"name": "nomarl",
		"fontName": "HeiseiMin-W3",
		"fontSize": 20,
		"leading": 25,
		"firstLineIndent": 0,
	}
	style = ParagraphStyle(**style_dict)

	style_big_dict = {
		"name": "nomarl",
		"fontName": "HeiseiMin-W3",
		"fontSize": 30,
		"leading": 50,
		"firstLineIndent": 0,
	}
	style_big = ParagraphStyle(**style_big_dict)

	flowables = []

	para = Paragraph(title, style_big)
	flowables.append(para)

	flowables.append(PageBreak())

	para = Paragraph(content, style)
	flowables.append(para)

	doc.multiBuild(flowables)

	print(title)


# ChapterのURLのリスト
urls = get_urls(input("URL >> "))

# enumerateで番号を頭にふってファイルを保存
for idx, url in enumerate(urls, 1):
	name_initial = str(idx).zfill(3) + "-"
	create_pdf(url, name_initial)

	# 連続してアクセスしないように1s間とる
	time.sleep(1)
