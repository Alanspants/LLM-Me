from flask import Flask, request, render_template, session, redirect, jsonify

app = Flask(__name__)

# <form action="" method="post" id='myForm'>
#     <button name="button" value="value">Send</button>
# </form>
#
# <form action="" method="post" id='myForm2'>
#     <button id="myButton2" name="button2" value=0 onclick="modifyData()">Send</button>
# </form>
#
# <script>
#     function modifyData() {
#         data = "I want to send this to backend"
#         document.getElementById("myButton2").value = data;
#     }
# </script>

# @app.route("/", methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         if list(request.form.keys())[0] == 'button':
#             print(request.form['button'])
#
#         if list(request.form.keys())[0] == 'button2':
#             print(request.form['button2'])
#
#     return render_template("index.html")


@app.route("/index", methods=['GET', 'POST'])
def index():
    print(request.files)
    return render_template('index.html')


if __name__ == "__main__":
    app.run(port=5000)
