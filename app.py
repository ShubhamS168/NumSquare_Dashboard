from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)

# Create database tables (run once)
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/square', methods=['POST'])
def square():
    num = int(request.form['num'])
    result = Result(value=num*num)
    db.session.add(result)
    db.session.commit()
    return redirect(url_for('results'))  # Redirect to results page

@app.route('/results')
def results():
    all_results = Result.query.all()
    return render_template('results.html', results=all_results)

@app.route('/chart')
def chart():
    # Get data from the database
    results = Result.query.all()
    x = [i.id for i in results]
    y = [i.value for i in results]
    
    # Generate plot
    plt.figure()
    plt.plot(x, y, 'ro-')
    plt.title('Square Values Over Time')
    plt.xlabel('Entry ID')
    plt.ylabel('Computed Value')
    
    # Convert plot to HTML image
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()  # Prevent memory leaks
    
    return render_template('chart.html', plot_url=plot_url)

if __name__ == "__main__":
    app.run(debug=True)
