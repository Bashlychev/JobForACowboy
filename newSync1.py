import http.client
import json
import time

apis = [
	'api3/config',
	'api3/client',
	'api4/catalog/products',
	'api4/catalog/productCategories',
	'api4/catalog/productSubcategories',
	'api4/catalog/trades',
	'api4/catalog/prices',
	'api3/discount',
	'api4/catalog/priceTypes',
	'api3/photo/category',
	'api3/client/spravochnik',
	'api3/reject',
	'api3/kpi',
	'api3/task/get',
	#'api3/finans/postPayment',
	'api4/payment/balance',
	#'api3/visit/postCheck',
	'api3/defect/reasons',
	'api3/client/inventory',
	'api4/catalog/notes',
	'api3/tara',
	'api4/catalog/warehouses',
	'api4/stock',
	'api3/outlet/v3',
	'api3/client/dayTransactions',
]

server = 'test202.sddev.uz'
login = ''
password = ''

def getToken(server: str, login: str, password: str):
	conn = http.client.HTTPSConnection(server)
	conn.request('POST', f"/api4/login", json.dumps({
		'login': login,
		'password': password
	}))
	res = conn.getresponse()
	if (res.status == 200):
		data = json.loads(res.read())
		print(data)
		if data['status'] == True:
			return data['result']['token']
	return None

token = getToken(server, login, password)
print(f"token is {token}")

n = 100 # number of synchronizations

for i in range(n):
	for api in apis:
		conn = http.client.HTTPSConnection(server)
		conn.connect()
		conn.set_debuglevel(0) # set to 1 if you need debug logs
		conn.request("GET", f"/{api}?u=agent&apiVersion=3&deviceToken={token}&chk={int(time.time())}")
		res = conn.getresponse()

		print(api, i)
		print(res.status, res.reason)

		if res.status != 200:
			break

		try:
			body = json.loads(res.read())
			#print(body)
		except json.JSONDecodeError:
			print("response is not valid json")
			break


