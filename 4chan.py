import json, os, time, urllib2, re, argparse


def argsHandler():
	parser = argparse.ArgumentParser()
	parser.add_argument('board', action="store")
	parser.add_argument('thread', action="store")
	parser.add_argument('-yt', action="store_true", default=False)
	return parser.parse_args()

def download(board, thread, filename):
	try:
		filename = filename
		link = "http://i.4cdn.org/" + board + "/" + filename
		downloadfile = urllib2.urlopen(link)
		
		print "Downloading: " + filename
		fileloc = os.path.join(board+thread, filename)
		output = open(fileloc,'wb')

		output.write(downloadfile.read())

		output.close()
	except urllib2.HTTPError:
		print "Can't download file"
	time.sleep(1)

def youtubeLinks(data, folder):
	ytRegex = re.compile("(youtu\.be\/|youtube\.com\\\/(watch\?(.*&)?v=|(embed|v)\/))([^\?&\"'<]+)" )
	data = data.replace("<wbr>", "")
	youtube = ytRegex.findall(data)
	filename = "youtube.txt"
	fileloc = os.path.join(folder, filename)
	output = open(fileloc, 'w')

	for video in youtube:
		output.write("http://youtu.be/" + video[4] + "\n")

	output.close



options = argsHandler()
jsonLink = "http://a.4cdn.org/" + options.board + "/thread/" + options.thread + ".json"
try:
	os.mkdir(options.board+options.thread)
except Exception, e:
	pass

while True:
	
	data = urllib2.urlopen(jsonLink).read()
	jsonData = json.loads(data)
	folder = options.board+options.thread
	i = 0

	while i <= len(jsonData["posts"]):
		try:
			filename = str(jsonData["posts"][i]["tim"]) + jsonData["posts"][i]["ext"]
			fileloc = os.path.join(options.board+options.thread, filename)
			if not os.path.isfile(fileloc):
				download(options.board, options.thread, filename)

		except Exception, e:
			pass
		
		i+=1
		
	

	if options.yt == True:
		youtubeLinks(data, folder)

	print "No New Images. Sleeping for 30 seconds."
	time.sleep(30)
