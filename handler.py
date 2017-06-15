#!/usr/bin/env python3
import cgi
import html

form = cgi.FieldStorage()
text = form.getfirst("TEXT", "Неделя не выбрана")
text = html.escape(text)
print("Content-type: text/html\n\n")
print("""<!DOCTYPE HTML>
        <html>
        <head>
             <meta charset="UTF-8">
             <script type="text/javascript">
             window.location="http://tomas.hse7.ru/";""")
if text != "Неделя не выбрана":
    num_of_graph = int(text)
    f1 = open('links_in_json' + text + '.txt', 'r').read()
    f2 = open('links_in_json.txt', 'w')
    f2.write(f1)
    f2.close()
    f1.close()
    print("""</script></head><body>""")
else:
    print("""alert("Вы не выбрали неделю"); </script> </head><body>""")
print("""</body>
        </html>""")