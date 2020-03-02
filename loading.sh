rm -rf static/css
rm -rf static/js
rm static/favicon.ico
rm templates/index.html
cp -r stockm/dist/css static/ && \
cp -r stockm/dist/js static/ && \
cp stockm/dist/favicon.ico static/ && \
cp stockm/dist/index.html templates/ && \
python3 postaddjinja2.py