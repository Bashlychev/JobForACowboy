import http.client
import json

# https://test200.sddev.uz/api3/kpi/?u=agent&apiVersion=3&deviceToken=e0ccc2e7949ba1f400511c0e78db737847cf4386afd8965e5b30b0f2fabdfc4c&chk=1707383549791

conn = http.client.HTTPSConnection('test200.sddev.uz')
conn.connect()
conn.set_debuglevel(1)
for i in range(2000):
	conn.request("GET", "/api3/kpi/?u=agent&apiVersion=3&deviceToken=afd16bff81ff3e15337555d4283fb4266ef5159efad82dfcbc194d311ec9a46f&chk=1707383549791")
	res = conn.getresponse()
	print(res.status, res.reason, i)

	if res.status != 200:
		break

	try:
		body = json.loads(res.read())
		#print(body)
	except json.JSONDecodeError:
		print("response is not valid json")
		break


