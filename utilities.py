from enum import Enum
import json
class DateSheetType(Enum):
	tentative = 0
	final = 1
	final_new = 2

class index:
	@classmethod
	def date_index(self, ds_type):
		if ds_type == DateSheetType.tentative:
			return [4,0]
		elif ds_type == DateSheetType.final:
			return [15, 1]
		else:
			return [4, 0]
	@classmethod
	def morning_session_index(self, ds_type):
		if ds_type == DateSheetType.tentative:
			return [5, 0]
		elif ds_type == DateSheetType.final:
			return [16, 0]
		else:
			return[6, 0]
	@classmethod
	def evening_session_index(self, ds_type):
		if ds_type == DateSheetType.tentative:
			return [6, 0]
		elif ds_type == DateSheetType.final:
			return [17, 0]
		else:
			return [7, 0]

class keys:
	@classmethod
	def exam_date(self, ds_type):
		if ds_type == DateSheetType.tentative:
			return 'EXDATE'
		elif ds_type == DateSheetType.final:
			return 'Date & Day'
	@classmethod
	def serial_no(self, ds_type):
		if ds_type == DateSheetType.tentative:
			return 'SR.NO'
		elif ds_type == DateSheetType.final:
			return ''
	@classmethod
	def morning_session(self, ds_type):
		if ds_type == DateSheetType.tentative:
			return 'MORNING'
		elif ds_type == DateSheetType.final:
			return 'Morning Session'
	@classmethod
	def evening_session(self, ds_type):
		if ds_type == DateSheetType.tentative:
			return 'EVENING'
		elif ds_type == DateSheetType.final:
			return 'Evening Session'
	@classmethod
	def split_by(self, ds_type):
		if ds_type == DateSheetType.tentative:
			return '/'
		elif ds_type == DateSheetType.final:
			return ','
		else:
			return '/'

def add_zero(number: str):
	if(len(number)==1):
		return '0' + number
	else:
		return number
def get_month_int(month: str):
	if month == 'Jan' or month == 'January':
		return '01'
	elif month == 'Feb' or month == 'February':
		return '02'
	elif month == 'Mar' or month == 'March':
		return '03'
	elif month == 'Apr' or month == 'April':
		return '04'
	elif month == 'May' or month == 'May':
		return '05'
	elif month == 'Jun' or month == 'June':
		return '06'
	elif month == 'Jul' or month == 'July':
		return '07'
	elif month == 'Aug' or month == 'August':
		return '08'
	elif month == 'Sep' or month == 'September':
		return '09'
	elif month == 'Oct' or month == 'October':
		return '10' 
	elif month == 'Nov' or month == 'November':
		return '11'
	elif month == 'Dec' or month == 'December':
		return '12'
def get_description(code: str) -> str:
	code = code.upper()
	code_map = {
		#BCA - Sem1
		"FEG02":    "Foundation course in English -2",
		"ECO01":    "Business Organization",
		"BCS011":   "Computer Basics and PC Software",
		"BCS012":   "Mathematics",
		"BCSL013":  "Computer Basics and PC Software Lab",

		#BCA - Sem2
		"ECO02":	"Accountancy-1",
		"MCS011":	"Problem Solving and Programming",
		"MCS012":	"Computer Organization and Assembly Language Programming",
		"MCS015":	"Communication Skills",
		"MCS013":	"Discrete Mathematics",
		"BCSL021":	"C Language Programming Lab",
		"BCSL022":	"Assembly Language Programming Lab",

		#BCA - Sem3
		"MCS021":	"Data and File Structures",
		"MCS023":	"Introduction to Database Management Systems",
		"MCS014":	"Systems Analysis and Design",
		"BCS031":	"Programming in C++",
		"BCSL032":	"C++ Programming Lab",
		"BCSL033":	"Data and File Structures Lab",
		"BCSL034":	"DBMS Lab",

		#BCA - Sem4
		"BCS040":	"Statistical Techniques",
		"MCS024":	"Object Oriented Technologies and Java Programming",
		"BCS041":	"Fundamentals of Computer Networks",
		"BCS042":	"Introduction to Algorithm Design",
		"MCSL016":	"Internet Concepts and Web Design",
		"BCSL043":	"Java Programming Lab",
		"BCSL044":	"Statistical Techniques Lab",
		"BCSL045":	"Algorithm Design Lab",

		#BCA - Sem5
		"BCS051":	"Introduction to Software Engineering",
		"BCS052":	"Network Programming and Administration",
		"BCS053":	"Web Programming",
		"BCS054":	"Computer Oriented Numerical Techniques",
		"BCS055":	"Business Communication",
		"BCSL056":	"Network Programming and Administration Lab",
		"BCSL057":	"Web Programming Lab",
		"BCSL058":	"Computer Oriented Numerical Techniques Lab",

		#BCA - Sem6
		"BCS062":	"E-Commerce",
		"MCS022":	"Operating System Concepts and Networking Management",
		"BCSL063":	"Operating System Concepts and Networking Management Lab",
		"BCSP064":	"Project",

		#MCA - Sem1
		"MCS011":	"Problem Solving and Programming",
		"MCS012":	"Computer Organization and Assembly Language Programming",
		"MCS013":	"Discrete Mathematics",
		"MCS014":	"Systems Analysis and Design",
		"MCS015":	"Communication Skills",
		"MCSL016":	"Internet Concepts and Web Design",
		"MCSL017":	"C and Assembly Language Programming Lab",

		#MCA - Sem2
		"MCS021":	"Data and File Structures",
		"MCS022":	"Operating System Concepts and Networking Management",
		"MCS023":	"Introduction to Database Management Systems",
		"MCS024":	"Object Oriented Technologies and Java Programming",
		"MCSL025":	"Lab (based on MCS-021, 022, 023 & 024)",

		#MCA - Sem3
		"MCS031":	"Design and Analysis of Algorithms",
		"MCS032":	"Object Oriented Analysis and Design",
		"MCS033":	"Advanced Discrete Mathematics",
		"MCS034":	"Software Engineering",
		"MCS035":	"Accountancy and Financial Management",
		"MCSL036":	"Lab (based on MCS-032, 034 and 035)",

		#MCA - Sem4
		"MCS041":	"Operating Systems",
		"MCS042":	"Data Communication and Computer Networks",
		"MCS043":	"Advanced Database Management Systems",
		"MCS044":	"Mini Project",
		"MCSL045":	"Lab (UNIX & Oracle)",

		#MCA - Sem5
		"MCS051":	"Advanced Internet Technologies",
		"MCS052":	"Principles of Management and Information Systems",
		"MCS053":	"Computer Graphics and Multimedia",
		"MCSL054":	"Lab (based on MCS-051 & 053)",

		#MCA - Sem6
		"MCSP060":"Project"
	}
	return code_map.get(code, '')
class Courses:
		filename = ""
		courses = []
		def __init__(self, filename):
			self.filename = filename
			with open(filename, 'r') as file:
				self.courses = json.loads(file.read())
		def get_course(self, course_code: str):
			for course in self.courses:
				if course["code"] == course_code:
					return course
			return None
		def get_title(self, course_code: str):
			for course in self.courses:
				if course["code"] == course_code:
					return course["title"]
			return ""
