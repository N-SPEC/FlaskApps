from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import area, position, areapositionxref
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('home.html', user=current_user)

@views.route('/area', methods=['GET', 'POST'])
@login_required
def show_area():
    if request.method == 'POST':
        area_id = request.form.get('area_id')
        area_name = request.form.get('area_name')
        if area_id and area_name:
            # Check if the area ID is unique
            existing_area = area.query.filter_by(area_id=area_id).first()
            if existing_area:
                flash('Area ID already exists!', category='error')
            else:
                new_area = area(area_id=area_id, area_name=area_name)
                db.session.add(new_area)
                db.session.commit()
                flash('Area Added Successfully!', category='success')
        else:
            flash('Both Area ID and Area name are required!', category='error')
        return redirect(url_for('views.show_area'))  # Redirect to the same page after adding the area
    else:
        area_list = area.query.all()
        return render_template('area.html', areas=area_list)

@views.route('/position', methods=['GET', 'POST'])
@login_required
def show_position():
    if request.method == 'POST':
        position_id = request.form.get('position_id')  
        position_name = request.form.get('position_name')
        area_id = request.form.get('area_id')

        if position_id and position_name and area_id:
            existing_position = position.query.filter_by(position_id=position_id, area_id=area_id).first()
            if existing_position:
                flash('Position ID already exists for this Area ID!', category='error')
            else:
                new_position = position(position_id=position_id, position_name=position_name, area_id=area_id)
                db.session.add(new_position)
                db.session.commit()
                flash('Position Added Successfully!', category='success')
        else:
            flash('Position ID, Position Name, and Area ID are required!', category='error')
        return redirect(url_for('views.show_position'))  
    else:
        position_list = position.query.all()
        return render_template('position.html', positions=position_list)

from flask import jsonify

@views.route('/area_position', methods=['GET', 'POST'])
@login_required
def area_position():
    if request.method == 'POST':
        category_id = request.form['category_id']
        positions = position.query.filter_by(area_id=category_id).order_by(position.name.asc()).all()

        # Prepare output for JSON response
        output_array = []
        for pos in positions:  # Change variable name to avoid conflicts
            output_obj = {
                'id': pos.area_id,
                'name': pos.area_name  # Access 'name' attribute, not 'area_name'
            }
            output_array.append(output_obj)

        # Return JSON response for POST request
        return jsonify(output_array)

    # Handle GET requests (optional)
    return jsonify([])  # Return an empty JSON array for GET requests

