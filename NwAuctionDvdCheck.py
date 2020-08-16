import NwAuctionDvdCheckConfig as config

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
		return false
		
	return true
	

def Main():
	
	myDvdsRaw = ReadTextFile(config.MovieListFilename)
	if myDvdsRaw == None:
		print(f'Unable to read file {config.MovieListFilename}')
		Exit(1)

	myDvdWarnings = []
	myDvds = []
	# for title in myDvdsRaw:
		# parts = 

	nwDvds = ReadTextFile(config.NwAuctionInputFilename)
	if myDvds == None:
		print(f'Unable to read file {config.NwAuctionInputFilename}')
		Exit(1)

if __name__ == '__main__':
	Main()

