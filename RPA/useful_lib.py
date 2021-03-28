#useful_lib.py
# 200821
# CK

import tagui as t
import datetime
import time
import re

######
# tomorrow
# 190808
# CK
def tomorrow(self):
	tomorrow = datetime.date.today() + datetime.timedelta(days=1)
	return tomorrow.strftime("%d/%m/%Y")

######
# date_format
# 190808
# CK
def date_format(date, format='Y-m-d'):
	format2 = ''
	for elem in format:
		if (re.search('[a-zA-Z]', elem)):
			format2 = format2+'%'+elem
		else:
			format2 = format2 + elem
	#print("format2 = "+format2)
	return date.strftime(format2)

######
# today
# 190808
# CK
def today(format='Y-m-d'):
	return date_format(datetime.date.today(), format)

######
# now
# 190808
# CK
def now(format='Ymd_HM'):
	#attendance 2019-05-23 20190628_0932
	#https://github.com/ck81/iss-tms/tree/v2.39/03_print_attendance
	return date_format(datetime.datetime.now(), format)

######
# calculate_elapsed_time
# 190814
# CK
def calculate_elapsed_time(start_time, end_time):
	timeDiff_s = end_time - start_time
	timeDiff_min = timeDiff_s/60
	timeDiff_hr = timeDiff_min/60

	if (timeDiff_min<1):
		elapsed_time = "{:.2f} sec".format(timeDiff_s);
	elif (timeDiff_hr<1):
		elapsed_time =  "{:.2f} min".format(timeDiff_min);
	else:
		elapsed_time = "{:.2f} hr".format(timeDiff_hr);

	return elapsed_time

######
# get_elapsed_time
# 190814
# CK
def get_elapsed_time(start_time):
	end_time = time.time()
	elapsed_time = calculate_elapsed_time(start_time, end_time)
	return elapsed_time

######
# wait_for_pageload
# 190708
# CK
def wait_for_pageload(selector, wait_time=36):
	wait_status = 0
	print("Waiting for page to load...")
	for loop_wait in range(1, wait_time):
		if t.present(selector):
			wait_status = 1
			break
		else:
			print(f'{loop_wait} second elapsed...')
			time.sleep(1)
	if (wait_status==0):
		sys.exit(f'Timeout! wait_for_pageload >>> {wait_time}')
	else:
		print("Page Loaded!")
		print("")
		return selector
