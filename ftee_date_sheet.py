import fitz
import utilities as utl
import json
import datetime as date
import argparse
parser = argparse.ArgumentParser(description="Extract datesheet form pdf and save it as json file.")
parser.add_argument("filein", help="Filename of tentative datesheet",
                    type=str)
parser.add_argument("fileout", help="Filename to save output in",
                    type=str)
args = parser.parse_args()
doc = fitz.open(args.filein)

page = doc.loadPage(0)
text = page.getText("dict")

tmp = text['blocks'][0]['lines'][0]['spans'][2]['text'].split(',')
published_on = tmp[1].strip() + '-' + utl.get_month_int(tmp[0].strip()) + '-'
tmp = text['blocks'][0]['lines'][0]['spans'][0]['text'].strip()
published_on += '0' + tmp if len(tmp) <= 1 else tmp

""" In new final datesheet of 2018, day and month are in different lines and year is entirely in different block"""
day_pos = text['blocks'][utl.index.date_index(utl.DateSheetType.final_new)[0]]['lines'][utl.index.date_index(utl.DateSheetType.final_new)[1]]['bbox'][0]
month_pos = text['blocks'][utl.index.date_index(utl.DateSheetType.final_new)[0]]['lines'][1]['bbox'][0]
year_pos = text['blocks'][5]['lines'][0]['bbox'][0]

""" Old style of date"""
# date_pos = text['blocks'][utl.index.date_index(utl.DateSheetType.final_new)[0]]['lines'][utl.index.date_index(utl.DateSheetType.final_new)[1]]['bbox'][0]

morning_session_pos = text['blocks'][utl.index.morning_session_index(utl.DateSheetType.final_new)[0]]['lines'][utl.index.morning_session_index(utl.DateSheetType.final_new)[1]]['bbox'][0]
evening_session_pos = text['blocks'][utl.index.evening_session_index(utl.DateSheetType.final_new)[0]]['lines'][utl.index.evening_session_index(utl.DateSheetType.final_new)[1]]['bbox'][0]

datesheet = dict()
dates = dict()
for_exam = text['blocks'][1]['lines'][0]['spans'][0]['text'].strip()
tmp = text['blocks'][0]['lines'][0]['spans'][2]['text'].split(',')
published_on = tmp[1].strip() + '-' + utl.get_month_int(tmp[0].strip()) + '-'
tmp = text['blocks'][0]['lines'][0]['spans'][0]['text'].strip()
published_on += '0' + tmp if len(tmp) <= 1 else tmp
last_refreshed = date.datetime.now()

subjects_morning = ''
subjects_evening = ''
date = ''
day = ''
month = ''
previous_type = ''
def insert_date():
	global subjects_evening, subjects_morning, previous_type
	tmp = subjects_morning.split(utl.keys.split_by(utl.DateSheetType.final_new))
	tmp_m_list = []
	for d in tmp:
		d = d.strip()
		if len(d) > 0:
			tmp_m_list.append(d)
	tmp = subjects_evening.split(utl.keys.split_by(utl.DateSheetType.final_new))
	tmp_e_list = []
	for d in tmp:
		d = d.strip()
		if len(d) > 0:
			tmp_e_list.append(d)

	dates[date] = {
			'Morning' : tmp_m_list.copy(),
			'Evening': tmp_e_list.copy()
			}
	subjects_morning = ''
	subjects_evening = ''
	previous_type = ''

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
					if line['bbox'][0] == day_pos:
						data = data.strip()
						if len(data) == 3:
							if previous_type == 'evening_session':
								insert_date()
							day = data.replace('-', '')
							previous_type = 'day'
					if line['bbox'][0] == month_pos:
						data = data.strip()
						if len(data) == 4:
							month = data.replace('-', '')
							month = utl.get_month_int(month)
							previous_type = 'month'
					if line['bbox'][0] == year_pos:
						data = data.strip()
						if len(data) == 2:
							year = '20' + data.strip()
							date = year + '-' + month + '-' + day
							previous_type = 'year'
					elif line['bbox'][0] == morning_session_pos:
						previous_type = 'morning_session'
						subjects_morning += data
					elif line['bbox'][0] == evening_session_pos:
						previous_type = 'evening_session'
						subjects_evening += data
if len(date) == 10 and date not in dates:
	insert_date()
datesheet = {
	'exam_text': for_exam,
	'published_on': published_on,
	'last_refreshed': str(last_refreshed),
	'date_sheet': dates
}
with open(args.fileout, 'w') as f:
	f.write(json.dumps(datesheet))
