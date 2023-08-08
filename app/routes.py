from datetime import datetime
import json
import re
from flask import request, jsonify, make_response
from app import app, db
from app.models import basicinfo, educationalbackground, professionalexperience
import os
from werkzeug.utils import secure_filename
from marshmallow import Schema, fields, ValidationError, validate

class BasicInfoSchema(Schema):
    name = fields.String(required=True, validate=[
        validate.Length(max=20),
        validate.Regexp(r'^[a-zA-Z ]*$', error='name can only contain alphabetic characters')
    ])
    gender = fields.String(required=True, validate=validate.OneOf(['male', 'female']), error='gender can be male or female only')
    email = fields.Email(required=True, error="invalid email format")
    phone = fields.String(required=True, validate=validate.Regexp(r'^\d{10}$', error='invalid phone number'))
    address = fields.String(required=True, validate=validate.Length(max=200), error="address cannot exceed 200 characters")
    profilePicture = fields.String()

def validate_educational_form_data(data):
    errors = {}
    
    tenth = data.get('tenth')      
    if tenth:
        if not tenth.get('schoolName'):
            errors['tenth'] = {'schoolName': 'school name is required'}
        elif len(tenth.get('schoolName')) > 50:
            errors['tenth'] = {'schoolName': 'school name should not exceed 50 characters'}
        elif not tenth.get('schoolName').isalpha():
            errors['tenth'] = {'schoolName': 'school name should contain alphabets only'}
        if not tenth.get('passingYear'):
            errors['tenth'] = {'passingYear': 'passing year is required'}
        elif not tenth.get('passingYear').isdigit() or not (1949< int(tenth.get('passingYear')) < int(datetime.now().year)):
            errors['tenth'] = {'passingYear': 'invalid passing year.'}
        if not tenth.get('percentage'):
            errors['tenth'] = {'percentage': 'percentage is required'}
        elif not tenth.get('percentage').isdigit() or not (0 <= int(tenth.get('percentage')) <= 100):
            errors['tenth'] = {'percentage': 'invalid percentage'}        

    
    twelfth = data.get('twelfth')
    if twelfth:
        if not twelfth.get('schoolName'):
            errors['twelfth'] = {'schoolName': 'school name is required'}
        elif len(twelfth.get('schoolName')) > 50:
            errors['twelfth'] = {'schoolName': 'school name should not exceed 50 characters'}
        elif not twelfth.get('schoolName').isalpha():
            errors['twelfth'] = {'schoolName': 'school name should contain alphabets only'}
        if not twelfth.get('passingYear'):
            errors['twelfth'] = {'passingYear': 'passing year is required'}
        elif not twelfth.get('passingYear').isdigit() or not (1949< int(twelfth.get('passingYear')) < int(datetime.now().year)):
            errors['twelfth'] = {'passingYear': 'Invalid passing year'}
        if not twelfth.get('percentage'):
            errors['twelfth'] = {'percentage': 'percentage is required'}
        elif not twelfth.get('percentage').isdigit() or not (0 <= int(twelfth.get('percentage')) <= 100):
            errors['twelfth'] = {'percentage': 'invalid percentage'}        
    
    graduation = data.get('graduation')
    if graduation:
        if not graduation.get('schoolName'):
            errors['graduation'] = {'schoolName': 'school name is required'}
        elif len(graduation.get('schoolName')) > 50:
            errors['graduation'] = {'schoolName': 'school name should not exceed 50 characters'}
        elif not graduation.get('schoolName').isalpha():
            errors['graduation'] = {'schoolName': 'school name should contain alphabets only'}
        if not graduation.get('passingYear'):
            errors['graduation'] = {'passingYear': 'passing year is required'}
        elif not graduation.get('passingYear').isdigit() or not (1949< int(graduation.get('passingYear')) < datetime.now().year):
            errors['graduation'] = {'passingYear': 'invalid passing year'}
        if not graduation.get('percentage'):
            errors['graduation'] = {'percentage': 'percentage is required'}
        elif not graduation.get('percentage').isdigit() or not (0 <= int(graduation.get('percentage')) <= 100):
            errors['graduation'] = {'percentage': 'invalid percentage'}       
    
    other_education = data.get('otherEducation')
    if other_education:
        for i, item in enumerate(other_education):
            if not item.get('schoolName'):
                errors[f'otherEducation-{i}'] = {'schoolName': 'school name is required'}
            elif len(item.get('schoolName')) > 50:
                errors[f'otherEducation-{i}'] = {'schoolName': 'school name should not exceed 50 characters'}
            elif not item.get('schoolName').isalpha():
                errors[f'otherEducation-{i}'] = {'schoolName': 'school name should contain alphabets only'}
            if not item.get('passingYear'):
                errors[f'otherEducation-{i}'] = {'passingYear': 'passing year is required'}
            elif not item.get('passingYear').isdigit() or not (1949< int(item.get('passingYear')) < datetime.now().year):
                errors[f'otherEducation-{i}'] = {'passingYear': 'Invalid passing year'}
            if not item.get('percentage'):
                errors[f'otherEducation-{i}'] = {'percentage': 'percentage is required'}
            elif not item.get('percentage').isdigit() or not (0 <= int(item.get('percentage')) <= 100):
                errors[f'otherEducation-{i}'] = {'percentage': 'invalid percentage'}
            if not item.get('degreeName'):
                errors[f'otherEducation-{i}'] = {'degreeName': 'degree name is required'}
            elif len(item.get('degreeName')) > 20:
                errors[f'otherEducation-{i}'] = {'degreeName': 'degree name should not exceed 20 characters'}
            elif not item.get('degreeName').isalpha():
                errors[f'otherEducation-{i}'] = {'degreeName': 'degree name should contain alphabets only'}

    return errors

def validate_experience_form_data(data):
    errors = {}
    
    company_name = data.get('companyName')
    if not company_name or len(company_name) > 20:
        errors['companyName'] = 'company name must be between 1 and 20 characters'
    
    designation = data.get('designation')
    if not designation or not re.match(r'^[A-Za-z\s]+$', designation) or len(designation) > 20:
        errors['designation'] = 'designation must only contain alphabets and be between 1 and 20 characters'
    
    entry_date = data.get('entryDate')
    exit_date = data.get('exitDate')    

    if entry_date and exit_date:                        
        if entry_date > exit_date:
            errors['entryDate'] = 'entry date cannot be greater than exit date'
    
    reference_mail = data.get('referenceMail')
    if not reference_mail or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', reference_mail):
        errors['referenceMail'] = 'invalid reference email format'

    return errors

education_required_fields = {'degreeName', 'schoolName', 'percentage', 'passingYear'}
experience_required_fields = {'companyName', 'designation', 'entryDate', 'exitDate', 'referenceMail'}

@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        form_data_json = request.form.get('formData')
        form_data = json.loads(form_data_json)
        profile_picture = request.files.get('profilePicture')
        resume_file = request.files.get('resumeFile')

        if not form_data:
            return make_response(jsonify({'error': 'form data is missing'}), 400)
        
        try:
            basic_info_schema = BasicInfoSchema(unknown='exclude')
            basic_info_data = basic_info_schema.load(form_data['basicInfo'])
        except ValidationError as e:            
            return jsonify({'errors': e.messages}), 400

        if not basic_info_data or not all(key in basic_info_data for key in ['name', 'gender', 'email', 'phone', 'address']):
            return make_response(jsonify({'error': 'invalid basicInfo data'}), 400)        
        basic_info = basicinfo(**basic_info_data)
        db.session.add(basic_info)
        db.session.commit()

        education_data = form_data['educationForm']
        if not education_data:
            return make_response(jsonify({'error': 'educational background data is required'}), 400)
        
        errors  = validate_educational_form_data(education_data)
        if errors:
            return jsonify(errors ), 400

        for education_level in ['tenth', 'twelfth', 'graduation']:            
            education_data = form_data['educationForm'][education_level]
            if not all(key in education_data for key in ['schoolName', 'passingYear', 'percentage']):
                return make_response(jsonify({'error': f'{education_level} data is incomplete'}), 400)
            degree_name = education_level.capitalize()
            if education_data:
                education_data['degreeName'] = degree_name
                filtered_education_data = {}
                filtered_education_data = {key: education_data[key] for key in education_required_fields}
                filtered_education_data['basic_info_id'] = int(basic_info.id)
                educational_background = educationalbackground(
                    **filtered_education_data)
                db.session.add(educational_background)
                db.session.commit()

        other_education_data = form_data['educationForm']['otherEducation']
        if other_education_data:
            for other_education in other_education_data:
                if not all(key in other_education for key in ['schoolName', 'passingYear', 'percentage', 'degreeName']):
                    return make_response(jsonify({'error': 'other education data is incomplete'}), 400)
                filtered_education_data = {}
                filtered_education_data = {key: other_education[key] for key in education_required_fields}
                filtered_education_data['basic_info_id'] = int(basic_info.id)
                educational_background = educationalbackground(
                    **filtered_education_data)
                db.session.add(educational_background)
                db.session.commit()

        experience_data = form_data['experienceForm']['experience']
        if experience_data:
            for experience in experience_data:
                if not all(key in experience for key in ['companyName', 'designation', 'entryDate', 'exitDate', 'referenceMail']):
                    return make_response(jsonify({'error': 'invalid professional experience data'}), 400)
                experience['entryDate'] = datetime.strptime(
                    experience['entryDate'], '%Y-%m-%dT%H:%M:%S.%fZ').date()
                experience['exitDate'] = datetime.strptime(
                    experience['exitDate'], '%Y-%m-%dT%H:%M:%S.%fZ').date()
                print("before errors")
                errors  = validate_experience_form_data(experience)
                if errors:
                    return jsonify(errors ), 400
                print("after errors")
                filtered_experience_data = {}
                filtered_experience_data = {key: experience[key] for key in experience_required_fields}

                filtered_experience_data['basic_info_id'] = int(basic_info.id)
                professional_experience = professionalexperience(**filtered_experience_data)
                db.session.add(professional_experience)
                db.session.commit()

        if (profile_picture or resume_file):
            folder_path = os.path.join(
                app.config['UPLOAD_FOLDER'], str(basic_info.id))
            os.makedirs(folder_path)

        if profile_picture:
            profile_picture_filename = secure_filename(
                profile_picture.filename)
            profile_picture.save(os.path.join(
                folder_path, profile_picture_filename))

        if resume_file:
            resume_filename = secure_filename(resume_file.filename)
            resume_file.save(os.path.join(folder_path, resume_filename))

        return jsonify({'message': 'Form data saved successfully', 'inserted_document_id': basic_info.id}), 200
    except Exception as e:
        print('error occurred while submitting form data:', str(e))
        return make_response(jsonify({'error': 'error occurred while submitting the form data'}), 500)