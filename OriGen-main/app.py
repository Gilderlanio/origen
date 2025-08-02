from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():  # put application's code here
    return render_template("new_home.html")

@app.route('/genes')
def genes():  # put application's code here
    return render_template("genes.html")

@app.route('/variants')
def variants():  # put application's code here
    return render_template("variants.html")

@app.route('/networks')
def networks():
    return render_template("networks.html")

if __name__ == '__main__':
    import subprocess
    subprocess.Popen(["streamlit", "run", "mod_gene_stream.py", "--server.port=8501"])
    subprocess.Popen(["streamlit", "run", "mod_variant_stream.py", "--server.port=8502"])
    subprocess.Popen(["streamlit", "run", "mod_network_stream.py", "--server.port=8503"])
    app.run(debug=True)