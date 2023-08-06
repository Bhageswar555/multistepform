from datetime import datetime
import json
from flask import request, jsonify, make_response
from app import app, db
from app.models import basicinfo, educationalbackground, professionalexperience
import os
from werkzeug.utils import secure_filename


@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        form_data_json = request.form.get('formData')
        form_data = json.loads(form_data_json)
        profile_picture = request.files.get('profilePicture')
        resume_file = request.files.get('resumeFile')

        if not form_data:
            return make_response(jsonify({'error': 'form data is missing'}), 400)

        basic_info_data = form_data['basicInfo']
        if not basic_info_data or not all(key in basic_info_data for key in ['name', 'gender', 'email', 'phone', 'address']):
            return make_response(jsonify({'error': 'Invalid basicInfo data'}), 400)

        basic_info_data.pop('profilePictureUrl', None)
        basic_info = basicinfo(**basic_info_data)
        db.session.add(basic_info)
        db.session.commit()

        education_data = form_data['educationForm']
        if not education_data:
            return make_response(jsonify({'error': 'Educational background data is required'}), 400)

        for education_level in ['tenth', 'twelfth', 'graduation']:            
            education_data = form_data['educationForm'][education_level]
            if not all(key in education_data for key in ['schoolName', 'passingYear', 'percentage']):
                return make_response(jsonify({'error': f'{education_level} data is incomplete'}), 400)
            degree_name = education_level.capitalize()
            if education_data:
                education_data['degreeName'] = degree_name
                education_data['basic_info_id'] = int(basic_info.id)
                educational_background = educationalbackground(
                    **education_data)
                db.session.add(educational_background)
                db.session.commit()

        other_education_data = form_data['educationForm']['otherEducation']
        if other_education_data:
            for other_education in other_education_data:
                if not all(key in other_education for key in ['schoolName', 'passingYear', 'percentage', 'degreeName']):
                    return make_response(jsonify({'error': 'other education data is incomplete'}), 400)
                other_education['basic_info_id'] = int(basic_info.id)
                educational_background = educationalbackground(
                    **other_education)
                db.session.add(educational_background)
                db.session.commit()

        experience_data = form_data['experienceForm']['experience']
        if experience_data:
            for experience in experience_data:
                if not all(key in experience for key in ['companyName', 'designation', 'entryDate', 'exitDate', 'referenceMail']):
                    return make_response(jsonify({'error': 'Invalid professional experience data'}), 400)
                experience['basic_info_id'] = int(basic_info.id)
                experience['entryDate'] = datetime.strptime(
                    experience['entryDate'], '%Y-%m-%dT%H:%M:%S.%fZ').date()
                experience['exitDate'] = datetime.strptime(
                    experience['exitDate'], '%Y-%m-%dT%H:%M:%S.%fZ').date()
                professional_experience = professionalexperience(**experience)
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