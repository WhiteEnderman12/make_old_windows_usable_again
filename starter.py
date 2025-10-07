import subprocess

try:
	print("starting Proxy...")
	process = subprocess.Popen(["python", "proxy/proxy_server.py"])
except Exception as e:
	print("start failed! See errorlog")
	file = open("errorlog.log", "a")
	file.write(str(e))
	file.close()

try:
	print("starting Backend Simulator...")
	process = subprocess.Popen(["python", "backendsimulator/backendsimulator.py"])
except Exception as e:
	print("start failed! See errorlog")
	file = open("errorlog.log", "a")
	file.write(str(e))
	file.close()
