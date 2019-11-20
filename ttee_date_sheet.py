import fitz
import utilities as utl
import json
import datetime as date
import argparse
import string
import re

date_format = "^(\d{1,2}\.\d{1,2}\.\d{4})$"
date_tester = re.compile(date_format)

parser = argparse.ArgumentParser(description="Extract datesheet form pdf and save it as json file.")
parser.add_argument("filein", help="Filename of tentative datesheet",
					type=str)
parser.add_argument("fileout", help="Filename to save output in",
					type=str)
args = parser.parse_args()

doc = fitz.open(args.filein)

page = doc.loadPage(0)
text = page.getText("dict")

previous_type = ''
count = 0
date_pos_1 = text['blocks'][utl.index.date_index(utl.DateSheetType.tentative)[0]]['lines'][utl.index.date_index(utl.DateSheetType.tentative)[1]]['bbox'][0]
morning_session_pos = text['blocks'][utl.index.morning_session_index(utl.DateSheetType.tentative)[0]]['lines'][utl.index.morning_session_index(utl.DateSheetType.tentative)[1]]['bbox'][0]
evening_session_pos = text['blocks'][utl.index.evening_session_index(utl.DateSheetType.tentative)[0]]['lines'][utl.index.evening_session_index(utl.DateSheetType.tentative)[1]]['bbox'][0]
datesheet = dict()
dates = dict()
for_exam = text['blocks'][1]['lines'][0]['spans'][1]['text']
for_exam = string.capwords(for_exam)
published_on = text['blocks'][0]['lines'][0]['spans'][0]['text']
tmp = published_on.split(' ')
tmp = list(filter(None, tmp))
published_on = tmp[2] + '-' + utl.get_month_int(tmp[1].replace(",","")) + "-0" + tmp[0][0:1]
last_refreshed = date.datetime.now()

date = ''
previous_type = ''
def insert_date(temp_subjects_morning, temp_subjects_evening, date):
	subjects_morning = []
	subjects_evening = []
	if not date:
		return
	data = temp_subjects_morning.split(utl.keys.split_by(utl.DateSheetType.tentative))
	for d in data:
		d = d.replace("-","")
		d = d.split('(')[0]
		d = d.strip()
		if len(d) > 0:
			subjects_morning.append(d)
	data = temp_subjects_evening.split(utl.keys.split_by(utl.DateSheetType.tentative))
	for d in data:
		d = d.replace("-","")
		d = d.split('(')[0]
		d = d.strip()
		if len(d) > 0:
			subjects_evening.append(d)
	dates[date] = {
			'Morning' : subjects_morning.copy(),
			'Evening': subjects_evening.copy()}

temp_subjects_morning = ""
temp_subjects_evening = ""
for n in range(doc.pageCount):
	page = doc.loadPage(n)
	text = page.getText("dict")
	for block in text['blocks']:
		if 'lines' in block:
			for line in block['lines']:
				if 'bbox' in line and 'spans' in line:
					data = ''
					for span in line['spans']:
						if 'text' in span:
							data += span['text']
					if line['bbox'][0] == date_pos_1:
						data = data.strip()
						if date_tester.match(data):
							if previous_type == 'morning_session' or previous_type == 'evening_session':
								insert_date(temp_subjects_morning, temp_subjects_evening, date)
								temp_subjects_evening = ""
								temp_subjects_morning = ""
							tmp = data.split('.')
							date = tmp[2] + '-' + utl.add_zero(tmp[1], 2) +'-' + utl.add_zero(tmp[0], 2)
							previous_type = 'date'
					elif line['bbox'][0] == morning_session_pos:
						previous_type = 'morning_session'
						temp_subjects_morning += data
					elif line['bbox'][0] == evening_session_pos:
						previous_type = 'evening_session'
						temp_subjects_evening += data

if len(date) == 10 and date not in dates:
	insert_date(temp_subjects_morning, temp_subjects_evening, date)
	temp_subjects_morning = ""
	temp_subjects_evening = ""
datesheet = {
	'exam_text': for_exam,
	'published_on': published_on,
	'last_refreshed': str(last_refreshed),
	'date_sheet': dates
}

with open(args.fileout, 'w') as f:
	f.write(json.dumps(datesheet))
