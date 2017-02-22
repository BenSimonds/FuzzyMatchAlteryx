"""Generate some random data."""

import csv
import random
import datetime


def get_firstnames(n):
	"""Return a python list of valid first names."""
	with open('sources/CSV_Database_of_First_Names.csv','r') as csvfile:
		_reader = csv.reader(csvfile)
		return [row[0].upper() for row in _reader][1:n] # can only generate so many.

def get_lastnames(n):
	"""Return a python list of valid first names."""
	with open('sources/CSV_Database_of_Last_Names.csv','r') as csvfile:
		_reader = csv.reader(csvfile)
		return [row[0].upper() for row in _reader][1:n] # can only generate so many.

def get_postcodes(n):
	"""Lazily generate random postcodes."""		
	# Format AANN NAA
	chars = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
	digits = list('1234567890')

	def gen_postcode():
		postcode = []
		postcode.append(random.choice(chars))
		postcode.append(random.choice(chars))
		postcode.append(random.choice(digits))
		postcode.append(random.choice(digits))
		postcode.append(random.choice(digits))
		postcode.append(random.choice(chars))
		postcode.append(random.choice(chars))
		return ''.join(postcode)

	postcodes = []
	for x in range(0,n):
		postcodes.append(gen_postcode())

	return postcodes

def  get_dobs(y,m,d, n):
	"""takes iso date and returns days after that."""
	startdate = datetime.date(y,m,d)
	td = datetime.timedelta(days=1)
	dobs = []
	for x in range(0,n):
		dobs.append(startdate.strftime('%Y-%m-%d'))
		startdate += td

	return dobs

		

def get_companies(n):
	"""Big ugly file, use a generator to not bother reading so much."""
	
	def company_generator():
		with open('sources/BasicCompanyData-2017-02-03-part2_5.csv','r', encoding='utf-8') as csvfile:
			_reader = csv.reader(csvfile)
			for row in _reader:
				yield row

	cg = company_generator()
	next(cg)   # Discard header row.
	return [next(cg)[0] for i in range(0,n)]

if __name__ == '__main__':
	fn = get_firstnames(10)
	print(fn[0:100])
	ln = get_lastnames(10)
	print(ln[0:100])

	x = get_companies(10)
	print(x)

	print('Done')

	print(get_postcodes(10))

	print(get_dobs(1970,1,1,10))
	# Generate a csv of some data.
	with open('../exampledata.csv','w') as csvfile:
		_writer = csv.writer(csvfile, delimiter='	', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
		_writer.writerow(['First Name','Last Name','DoB','Postcode','Company'])
			
		fns = get_firstnames(10000)
		lns = get_lastnames(10000)
		dobs = get_dobs(1970,1,1,10000)
		postcodes = get_postcodes(10000)
		companies = get_companies(10000)

		def pick_allow_null(list,nullprob):
			if random.random() > nullprob:
				return random.choice(list)
			else:
				return 'NULL'

		for x in range(0,100000):
			_writer.writerow([
				random.choice(fns),
				random.choice(lns),
				pick_allow_null(dobs,0.1),
				pick_allow_null(postcodes,0.1),
				pick_allow_null(companies,0.1)
				])