from app import db

class basicinfo(db.Model):
    id = db.Column(db.Integer, primary_key=True, )
    name = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    profilePicture = db.Column(db.String(50))
    educational_backgrounds = db.relationship(
        'educationalbackground', backref='basicinfo', lazy=True)
    professional_experiences = db.relationship(
        'professionalexperience', backref='basicinfo', lazy=True)


class educationalbackground(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    degreeName = db.Column(db.String(20), nullable=False)
    schoolName = db.Column(db.String(20), nullable=False)
    passingYear = db.Column(db.Integer, nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    basic_info_id = db.Column(
        db.Integer, db.ForeignKey('basicinfo.id'), nullable=False)


class professionalexperience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    companyName = db.Column(db.String(20), nullable=False)
    designation = db.Column(db.String(20), nullable=False)
    entryDate = db.Column(db.Date, nullable=False)
    exitDate = db.Column(db.Date, nullable=False)
    referenceMail = db.Column(db.String(200), nullable=False)
    basic_info_id = db.Column(
        db.Integer, db.ForeignKey('basicinfo.id'), nullable=False)
