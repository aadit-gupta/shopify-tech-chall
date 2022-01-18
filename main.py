import os

from flask import Flask,render_template,request,redirect,send_file
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "main.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Tool(db.Model):
    name = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return "<Name: {}>".format(self.name)


@app.route("/", methods=["GET", "POST"])
def index():
    tools = None
    if request.form:
        try:
            tool = Tool(name=request.form.get("name"))
            db.session.add(tool)
            db.session.commit()
        except:
            print("Error in adding tool")
    tools = Tool.query.all()
    return render_template("index.html", tools=tools)


@app.route("/update", methods=["POST"])
def update():
    try:
        newname = request.form.get("newname")
        oldname = request.form.get("oldname")
        tool = Tool.query.filter_by(name=oldname).first()
        tool.name = newname
        db.session.commit()
    except:
        print("Error in updating tool")
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    name = request.form.get("name")
    tool = Tool.query.filter_by(name=name).first()
    db.session.delete(tool)
    db.session.commit()
    return redirect("/")


# flask route for dumping database into a csv file
@app.route("/export")
def dump():
    tools = Tool.query.all()
    with open("inventory.csv", "w") as f:
        for tool in tools:
            f.write("{0}\n".format(tool.name))
    return send_file('inventory.csv', as_attachment=True)


if __name__ == "__main__":
    db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
