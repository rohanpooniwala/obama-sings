import youtube_dl
from bs4 import BeautifulSoup
import urllib.request

class AppURLopener(urllib.request.FancyURLopener):
	version = "Chrome/46.0"
	pass

def search_link(name):
	## IMPLEMENT SCRAPPING!!!!
	##sample : https://www.google.co.in/search?q=lalala&tbm=
	
	name = name.split(' ')
	temp = ''
	for _ in name:
		temp += _ +'+'
	temp = temp[:-1]
	
	google_link = 'https://www.youtube.com/results?search_query='+temp
	opener = AppURLopener()
	text = opener.open(google_link).read()

	soup = BeautifulSoup(text, 'lxml')
	
	links = []
	s_name = ""
	anc = soup.findAll('a')
	for a in anc:
		if (not a.parent or a.parent.name.lower() != "h3"):
			continue
		try:
			link = a['href']
			#print (a.encode('utf-8'))
			links.append([youtube_dl.utils.sanitize_filename(a.text), "www.youtube.com"+link])
		except KeyError:
			continue

	return links

def download(name, link, filename='', audio_only=False):
	try:
		filename = name if filename=='' else filename
		ydl_opts = {
			'format': 'bestvideo+bestaudio/best',
			'download_archive': './temp_video/downloaded',
			'outtmpl': "./temp_video/"+filename+'.%(ext)s',
			#'restrictfilenames': True,
		}
		if audio_only:
			ydl_opts = {
				'format': 'bestaudio/best',
				'postprocessors': [{
					'key': 'FFmpegExtractAudio',
					'preferredcodec': 'wav',
					'preferredquality': '192',
				}],
				'download_archive': './temp_video/downloaded',
				'outtmpl': "./temp_video/"+filename+'.%(ext)s',
				'fragment_retries': "infinite",

				#'restrictfilenames': True,
			}

		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			ydl.download([link])
		
		return True
	except Exception as e:
		print (e)
		return False