# Auto Scraping Pinterest Image / Url
# By RozhBasXYZ ( FREE )

import requests, re, time, urllib.parse, json, os
ses = requests.Session()
tampung = []

class Pinterest:
	def __init__(self):
		self.now = str(time.time()).replace('.','')[:-4]
		self.tampung = tampung ; self.nomor = 0
		self.cari = urllib.parse.quote(input("[!] masukan kata kunci yang kamu cari\n[?] input : ")); print("-"*20)
		self.scrol = int(input("[!] berapa kali ingin scrol ke bawah?\n[!] note semakin dikit semakin akurat\n[?] input : ")); print("-"*20)
		print("[!] dump di mulai tekan ctrl+c untuk stop dump"); print("-"*20)
		self.awal = ses.get('https://id.pinterest.com/resource/UserExperienceResource/get/?source_url=/search/pins/?rs=typed&q='+self.cari+'&data={"options":{"placement_ids":[29],"extra_context":{"search_query":"'+urllib.parse.unquote(self.cari)+'"}},"context":{}}&_='+self.now).text
		self.head = {"User-Agent": "Mozilla/5.0 (Linux; Android 11; 220333QAG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36", "X-APP-VERSION": "ba6e535", "X-Pinterest-AppState": "active", "X-Pinterest-ExperimentHash": re.findall('"experiment_hash":"(.*?)",',str(self.awal))[0], "X-Pinterest-PWS-Handler": "www/search/[scope].js", "X-Pinterest-Source-Url": "/search/pins/?rs=typed&q="+self.cari, "X-Requested-With": "XMLHttpRequest", "Accept":"application/json, text/javascript, */*, q=0.01"}
		try: self.get_source()
		except KeyboardInterrupt: Pinterest().simpan_foto()
		self.simpan_foto()
	
	def simpan_foto(self):
		print("\r"); print("-"*20)
		if input(f"\r[!] telah terkumpul total {len(self.tampung)} link foto\n[!] ingin simpan menjadi gambar [Y/N]\n[?] pilih : ") in ["n","N","NO","No","no"]:
			for _ in tampung: open(f"/sdcard/ROZHBAS/{urllib.parse.unquote(self.cari)}{str(time.time()).replace('.','')[:-4]}.txt","w").write(_+"\n")
			exit(f"[!] link tersimpan di folder internal ROZHBAS")
		else: print("-"*20)
		file = input("[?] harap masukan nama untuk file\n[!] cukup nama saja contoh 'FotoAbg'\n[?] nama  : "); print("-"*20)
		for foto in self.tampung:
			try:
				open(f"/sdcard/ROZHBAS/{file}{str(time.time()).replace('.','')[:-4]}.jpg","wb").write(urllib.request.urlopen(foto).read())
				self.nomor += 1
				print("\r[!] sukses menyimpan {} dari {} foto".format(self.nomor, len(self.tampung)), end="", flush=True)
			except: pass	
		
	def get_source(self):
		try:
			link = ses.get('https://id.pinterest.com/resource/BaseSearchResource/get/?source_url=/search/pins/?rs=typed&q='+self.cari+'&data={"options":{"article":"","appliedProductFilters":"---","price_max":null,"price_min":null,"query":"'+urllib.parse.unquote(self.cari)+'","scope":"pins","auto_correction_disabled":"","top_pin_id":"","filters":""},"context":{}}&_='+self.now, headers=self.head).text
			for pin in re.findall('"id":"(\d+)"', link):
				if len(pin)==18: self.get_source_pin(pin)
			self.get_source_url(link)
		except Exception as e: pass
	
	def get_source_url(self, link):
		for rozh_bas in range(self.scrol):
			try:
				for pin in re.findall('"id":"(\d+)"', link):
					if len(pin)==18: self.get_source_pin(pin)
				for url in re.findall('"url":"(.*?)"', str(link)):
					if "com/736" in str(url):
						if url in self.tampung: pass
						else: print("[!] link :",url); self.tampung.append(url)
					else: continue
				date = {"data": json.dumps({"options":{"article":"","appliedProductFilters":"---","price_max": "null","price_min": "null","query": urllib.parse.unquote(self.cari),"scope":"pins","auto_correction_disabled":"","top_pin_id":"","filters":"","bookmarks": [re.findall('"bookmark":"(.*?)"', link)[0]]},"context":{}}), "source_url": "/search/pins/?rs=typed&q="+self.cari}
				link = ses.post("https://id.pinterest.com/resource/BaseSearchResource/get/", params=date, headers={**self.head, "X-CSRFToken": ses.cookies["csrftoken"]}).text
			except Exception as e: pass
		
	def get_source_pin(self, pin):
		try:
			link = ses.get('https://id.pinterest.com/resource/RelatedPinFeedResource/get/?source_url=/pin/'+pin+'/&data={"options":{"field_set_key":"unauth_react","page_size":12,"pin":"'+pin+'","source":"search"},"context":{}}&_=1688744498583'+self.now, headers={**self.head, "X-CSRFToken": ses.cookies["csrftoken"], "X-Pinterest-Source-Url": f"/pin/{pin}/"}).text
			for url in re.findall('"url":"(.*?)"', str(link)):
				if "originals" in str(url):
					if url in self.tampung: pass
					else: print("[!] link :",url); self.tampung.append(url)
				else: continue
			self.get_next_pin(link, pin)
		except Exception as e: pass
		
	def get_next_pin(self, link, pin):
		main_link = 'https://id.pinterest.com/resource/RelatedPinFeedResource/get/?source_url=/pin/'+pin+'/&data={"options":{"field_set_key":"unauth_react","page_size":12,"pin":"'+pin+'","source":"search","bookmarks": ["'+re.findall('"bookmark":"(.*?)"', link)[0]+'"]},"context":{}}&_='+self.now
		for rozh_bas in range(self.scrol):
			try:
				link = ses.get(main_link, headers={**self.head, "X-CSRFToken": ses.cookies["csrftoken"], "X-Pinterest-Source-Url": f"/pin/{pin}/"}).text
				for url in re.findall('"url":"(.*?)"', str(link)):
					if "originals" in str(url):
						if url in self.tampung: pass
						else: print("[!] link :",url); self.tampung.append(url)
					else: continue
				main_link = 'https://id.pinterest.com/resource/RelatedPinFeedResource/get/?source_url=/pin/'+pin+'/&data={"options":{"field_set_key":"unauth_react","page_size":12,"pin":"'+pin+'","source":"search","bookmarks": ["'+re.findall('"bookmark":"(.*?)"', link)[0]+'"]},"context":{}}&_='+self.now
			except Exception as e: pass
	
if __name__ == "__main__":
	try: os.mkdir("/sdcard/ROZHBAS")
	except: pass
	os.system("clear")
	print(f""" ______ _______ _______ ______ 
|   __ \   _   |     __|   __ \ | rozh auto \n|      <       |__     |    __/ | scraping
|___|__|___|___|_______|___|    | pinterest\n{'-'*33}"""); Pinterest()
