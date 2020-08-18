import NwAuctionDvdCheckConfig as config
from datetime import datetime

def ParseMyTitleLine(inString:str):
	parts = inString.split()
	returnVal = ['', None]
	title = ''

	# invalid title
	if len(parts) < 2 or not RepresentsInt(parts[len(parts)-1]):
		return [inString.strip(), '0000', False]

	# valid Title
	return [' '.join(parts[0:len(parts)-1]), parts[len(parts)-1], True]


def ParseNwLine(inString:str):
	TITLE_TERMINATOR = '(DVD,'
	
	parts = inString.split()
	returnVal = ['', '0000', True]
	title = ''
	dvdIdx = 0

	if not TITLE_TERMINATOR in inString:
		return [inString.strip(), '0000', False]
	
	# get the title
	for p in parts:
		dvdIdx += 1
		if p == TITLE_TERMINATOR:
			returnVal[0] = title.strip()
			break
		title += p + ' '

	# find the year
	while dvdIdx < len(parts):
		if RepresentsInt(parts[dvdIdx]) and int(parts[dvdIdx]) > 1900:
			returnVal[1] = parts[dvdIdx]
			break
		if RepresentsInt(parts[dvdIdx][:-1]) and int(parts[dvdIdx][:-1]) > 1900: # ignore trailing char on date
			returnVal[1] = parts[dvdIdx][:-1]
			break

		dvdIdx += 1

	return returnVal


def ReadTextFile(filename:str):
	file = None
	try:
		file = open(filename)
	except Exception as ex:
		print(f'Unable to open file. ({filename}) {ex}')
		return None
		
	return file.readlines()

def RepresentsInt(inString:str):
	try:
		a = int(inString)
	except:
		return False
		
	return True
	

def Main():
	
	WRITE_MY_DVD_WARNINGS = False
	WRITE_NW_DVD_WARNINGS = False
	WRITE_MY_TITLES = False
	WRITE_NW_TITLES = False
	WRITE_UNMATCHED_NW_TITLES = True

	myDvdsRaw = ReadTextFile(config.MovieListFilename)
	if myDvdsRaw == None:
		print(f'Unable to read file {config.MovieListFilename}')
		Exit(1)

	myTitlesWarnings = []
	myTitles = []
	for title in myDvdsRaw:
		parsed = ParseMyTitleLine(title)
		if parsed[2] == False:
			myTitlesWarnings.append(title)
			continue
		elif len(title.strip()) == 0:
			continue

		t = f'{parsed[0]} {parsed[1]}'
		if t not in myTitles:
			myTitles.append(t)


	nwDvdsRaw = ReadTextFile(config.NwAuctionInputFilename)
	if nwDvdsRaw == None:
		print(f'Unable to read file {config.NwAuctionInputFilename}')
		Exit(1)

	nwTitlesWarnings = []
	nwTitles = []
	for title in nwDvdsRaw:
		parsed = ParseNwLine(title)
		if parsed[2] == False:
			nwTitlesWarnings.append(title)
			continue
		elif len(title.strip()) == 0:
			continue

		t = f'{parsed[0]} {parsed[1]}'
		if t not in nwTitles:
			nwTitles.append(t)

	# make a list of titles that nw has that do not appear in my list
	unMatchedNwTitles = []
	for title in nwTitles:
		if title not in myTitles:
			unMatchedNwTitles.append(title)

	
	output = None
	try:
		output = open(config.OutputFilename, 'w')
	except Exception as ex:
		print(f'Unable to open file {config.OutputFilename} for output')
		exit(1)

	if WRITE_MY_DVD_WARNINGS == True:
		output.write(datetime.now().strftime("%m/%d/%Y, %H:%M:%S\n"))
		output.write('\n============================\n=== MY DVD WARNING ITEMS ===\n============================\n\n')
		output.writelines(myTitlesWarnings)

	if WRITE_NW_DVD_WARNINGS == True:
		output.write('\n\n============================\n=== NW DVD WARNING ITEMS ===\n============================\n\n')
		output.writelines(nwTitlesWarnings)

	if WRITE_MY_TITLES == True:	
		output.write('\n\n=================\n=== MY TITLES ===\n=================\n\n')
		output.writelines(s + '\n' for s in myTitles)

	if WRITE_NW_TITLES == True:	
		output.write('\n\n=================\n=== NW TITLES ===\n=================\n\n')
		output.writelines(s + '\n' for s in nwTitles)

	if WRITE_UNMATCHED_NW_TITLES == True:	
		output.write('\n\n===========================\n=== UNMATCHED NW TITLES ===\n==========================\n\n')
		output.writelines(s + '\n' for s in unMatchedNwTitles)

	output.close()



if __name__ == '__main__':
	Main()

