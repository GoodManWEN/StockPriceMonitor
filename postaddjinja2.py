from os import path

WORKING_PATH = path.dirname(path.abspath(__file__))

with open(path.join(WORKING_PATH,'templates/index.html'),'r') as f:
	html = f.read()
ind = html.index('</body></html>')
html = html[:ind] + '{{ full_list | safe }}' + html[ind:]
with open(path.join(WORKING_PATH,'templates/index.html'),'w') as f:
	f.write(html)