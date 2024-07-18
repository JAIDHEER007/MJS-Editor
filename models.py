from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func
import uuid


db = SQLAlchemy()
class Mermaids(db.Model):
    # id = db.Column(db.Integer, primary_key = True)
    unique_id = db.Column(db.String, default = lambda : str(uuid.uuid4().hex), primary_key = True)
    name = db.Column(db.Text, nullable = False)
    description = db.Column(db.String)
    folder_path = db.Column(db.String)
    created_date = db.Column(db.DateTime, default = func.now())

    def __repr__(self):
        return f"""
        unique_id: {self.unique_id}
        mermaid_name: {self.name}
        folder_path: {self.folder_path}
        created_date: {self.created_date}
        """





