import requests
class Bot:
	def __init__(self):
		self.url = "https://api.telegram.org/bot1646042928:AAECtbzfL_5kk8EsdTqMobxynDAuFyePMVU/"

	def get_updates(self, offset=None, timeout=30):
		method = 'getUpdates'
		params = {'timeout': timeout, 'offset': offset}
		resp = requests.get(self.url + method,params)
		result_json = resp.json()['result']
		return result_json
	
	def get_last_update(self):
		get_result = self.get_updates()

		if len(get_result) > 0:
			last_update = get_result[-1]

		return last_update
	
	def send_message(self, chat_id, text):
		params = {'chat_id': chat_id, 'text': text}
		method = 'sendMessage'
		resp = requests.post(self.url + method, params)
		return resp