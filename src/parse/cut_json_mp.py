import jieba
import sys
import time, datetime
import json
from multiprocessing import Process
import subprocess
import re
import traceback
import logging

jieba.set_dictionary('/root/dict.txt.big')
jieba.load_userdict('/root/dict.txt.ptt')

stopwords = [ '的', '我', '了', '在', '有', '也', '都', '就', '妳', '不', '你', '說', '要', '被', '會', '嗎', '跟', '很', '到',"是","人","啊","沒","吧","啦","去","看","就是","好","新聞","他","她","為","但","為","這","才","又","真的","可以","不是","自己","喔","呢","這個","只是","這麼"]
punc = ['，','=','。','-','「','」','[',']',':','?','：','？','.','＿','！','!','~','(',')','/',',','（','）',"'",'"','、','_','+','..','....']

author_tmp = []

def write_to_file(fn, author, words, mode):
	fw = 0
	author = author.split('(')[0]
	author = re.compile('[^a-zA-Z0-9]').sub('', author)
	if author.strip() == '':
		return
	if mode == 0:
		fw = open('post/' + author + '.' + fn.split('/')[1], 'w+')
	else:
		subprocess.check_output('mkdir -p /tmp/ramdisk/member/' + author, shell=True)
		fw = open('/tmp/ramdisk/member/' + author + '/' + fn.split('/')[1], 'w+')
	fw.write(' '.join(words))
	fw.close()

def save_to_tmp(author, words, wkid):
	author = author.split('(')[0]
	author = re.compile('[^a-zA-Z0-9]').sub('', author)
	if author.strip() == '' or len(author) > 20:
		return
	if not author in author_tmp[wkid]:
		author_tmp[wkid][author] = []
	author_tmp[wkid][author].extend(words)

def filter_words(rwords):
	nwords = []
	for word in rwords:
		if word in stopwords or word in punc or word.strip() == '':
			continue
		nwords.append(word)
	return nwords

def work(fn, wkid):
	try:
		data = json.load(open(fn))
		raw_words = jieba.cut(data['title'] + ' ' + data['body'])
		words = filter_words(raw_words)
		save_to_tmp(data['author'], words, wkid)
		for push in data['push']:
			raw_push = jieba.cut(push['content'])
			push_words = filter_words(raw_push)
			save_to_tmp(push['author'], push_words, wkid)
			words.extend(push_words)
		write_to_file(fn, data['author'], words, 0)
	except Exception as e:
		logging.error(traceback.format_exc())

nth = 24

qs = []

for i in range(nth):
  qs.append([])
  author_tmp.append({})

lns = 0

for fn in sys.stdin:
	qs[lns % nth].append(fn.strip())
	lns += 1

print("{0} jobs inserted".format(lns))

def doJob(wkid):
	print(str(len(qs[wkid])) + " jobs accepted", file=sys.stderr)
	for j in qs[wkid]:
		work(j, wkid)
	for author, words in author_tmp[wkid].items():
		subprocess.check_output('mkdir -p /tmp/ramdisk/member/' + author, shell=True)
		fw = open('/tmp/ramdisk/member/' + author + '/' + str(wkid) + '.txt', 'w+')
		fw.write(' '.join(words))
		fw.close()

thd = []

print("start", file=sys.stderr)
print(datetime.datetime.now(), file=sys.stderr)

for i in range(24):
	thd.append(Process(target=doJob, args=(i,)))
	thd[i].start()

for i in range(24):
	thd[i].join()

print("end", file=sys.stderr)
print(datetime.datetime.now(), file=sys.stderr)
