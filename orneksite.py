from flask import Flask,render_template
import os
from sqlalchemy import Column,String,Integer,create_engine,Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import eventlet



engine  =   create_engine("sqlite:///orneksite.db")

# DB



Base = declarative_base()


class Projects(Base):
    __tablename__ = "Projects"
    id = Column(Integer, primary_key=True)
    header = Column(String)
    article = Column(Text)

Base.metadata.create_all(engine)

Session =   sessionmaker(bind=engine)
session =   Session()



def append_project(header,article):
    project =   Projects(header=header,article=article)
    session.add(project)
    session.commit()



def upgrade_project(header,nheader,narticle):
    project =   session.query(Projects).filter_by(header=header).first()
    project.header  =   nheader
    project.article =   narticle
    session.commit()

def delete_project(header):
    project =   session.query(Projects).filter_by(header=header).first()
    session.delete(project)
    session.commit()

# WEB

app     =   Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
eventlet.monkey_patch()

def bind_engine_to_thread():
    
    app.app_context().push()
    app.db = engine


@app.route("/")
def merhaba():
    return render_template("orneksite.html")

@app.route("/home_page")
def home_page():
    return render_template("index.html")

@app.route("/contact_us")
def contact_us():
    return render_template("contact.html")

@app.route("/about_us")
def about_us():
    return render_template("about.html")

@app.route("/projects")
def projects():
    session = Session()
    folder_path = os.path.join(app.static_folder, 'projects')
    
    resimler = os.listdir(folder_path)

    project =   session.query(Projects).all()
    

    return render_template("projects.html",resimler=resimler,project=project)


@app.route("/<sayi>")
def proje(sayi):
    
    for i in range(1, 15):
        if sayi == f"proje{i}.jpg":

            project =   session.query(Projects).filter_by(id=i).first()
                 
            filename    =f"/projects/proje{i}.jpg"
            return render_template("proje.html",filename=filename,header=project.header,article=project.article)

    return render_template("proje.html")



if __name__ == "__main__":
    bind_engine_to_thread()

    
    app.run(debug=True,threaded=True)