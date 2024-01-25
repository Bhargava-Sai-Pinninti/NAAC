from flask import Flask, request, render_template, redirect, url_for,session,flash
import secrets
import os
import pandas as pd
import shutil
import time



app = Flask(__name__)
# Generate a random and secure secret key
app.secret_key = secrets.token_hex(16)  # 16 bytes = 32 characters


# Function to read Excel file with retry mechanism
def read_excel_with_retry(file_path):
    df = None
    while True:
        try:
            df = pd.read_excel(file_path)
            time.sleep(0.1)
        except Exception as e:
            print(f"Error reading Excel file: {e}")
            # Handle the error (e.g., log, retry, or break out of the loop)
            pass
        else:
            break
    return df

# Function to write DataFrame to Excel file with retry mechanism
def write_excel_with_retry(df, file_path):
    while True:
        try:
            df.to_excel(file_path, index=False)
            time.sleep(0.1)
        except Exception as e:
            print(f"Error writing to Excel file: {e}")
            # Handle the error (e.g., log, retry, or break out of the loop)
            pass
        else:
            break


# Function to read CSV file with retry mechanism
def read_csv_with_retry(file_path):
    df = None
    while True:
        try:
            df = pd.read_csv(file_path)
            time.sleep(0.1)
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            # Handle the error (e.g., log, retry, or break out of the loop)
            pass
        else:
            break
    return df

# Function to write DataFrame to CSV file with retry mechanism
def write_csv_with_retry(df, file_path):
    while True:
        try:
            df.to_csv(file_path, index=False)
            time.sleep(0.1)
        except Exception as e:
            print(f"Error writing to CSV file: {e}")
            # Handle the error (e.g., log, retry, or break out of the loop)
            pass
        else:
            break

# Function to read the current value from 'config.txt' file with retry mechanism
def read_config_file():
    current_value = ""
    while True:
        try:
            with open('config.txt', 'r') as file:
                current_value = file.read().strip()
            time.sleep(0.1)
        except Exception as e:
            print(f"Error reading config.txt: {e}")
            # Handle the error (e.g., log, retry, or break out of the loop)
            pass
        else:
            break
    return current_value

# Function to write the selected folder to 'config.txt' file with retry mechanism
def write_config_file(selected_folder):
    while True:
        try:
            with open('config.txt', 'w') as file:
                file.write(selected_folder)
            time.sleep(0.1)
        except Exception as e:
            print(f"Error writing config.txt: {e}")
            # Handle the error (e.g., log, retry, or break out of the loop)
            pass
        else:
            break

# Function to read folder names from 'db' directory with retry mechanism
def read_folder_names():
    db_folder_path = 'db'
    folders = []
    while True:
        try:
            folders = [folder for folder in os.listdir(db_folder_path) if os.path.isdir(os.path.join(db_folder_path, folder))]
            time.sleep(0.1)
        except Exception as e:
            print(f"Error reading folders: {e}")
            # Handle the error (e.g., log, retry, or break out of the loop)
            pass
        else:
            break
    return folders


@app.route('/')
def welcome():
    session['admin'] = False
    return render_template('welcome/welcome.html')

@app.route('/home')
def home():
    session['admin'] = False
    return render_template('welcome/welcome.html')

@app.route('/about')
def about():
    return render_template('commonpages/about.html')

@app.route('/404_not_found')
def notfound():
    session['admin'] = False
    return render_template('commonpages/notfound.html')



# Admin Login route
@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    alert_message = None
    session['admin'] = False
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form.get('user_type')
        try:
            if user_type == "admins":
                # Read Excel file with retry mechanism
                file_path = "./static/admin/adminlogin.xlsx"
                df = read_excel_with_retry(file_path)

                user_exists = ((df['admin_id'] == username) & (df['admin_password'] == password)).any()
                df = None
                if user_exists:
                    session['adminname'] = username
                    session['admin'] = True
                    return redirect(url_for('admin_ui'))
                else:
                    alert_message = "Incorrect username or password"
        except Exception as e:
            print("Error:", e)
            alert_message = "Error occurred"

    return render_template('loginpages/adminlogin.html', alert_message=alert_message)

# Admin UI route
@app.route('/admin_ui', methods=['GET', 'POST'])
def admin_ui():
    username = session.get('adminname')
    admin = session.get('admin')
    if admin:
        db_folder_path = 'db'
        folders = []
        current_value = ""

        # Read the current value from the 'config.txt' file with retry mechanism
        while True:
            try:
                with open('config.txt', 'r') as file:
                    current_value = file.read().strip()
                time.sleep(0.1)
            except Exception as e:
                print(f"Error reading config.txt: {e}")
                # Handle the error (e.g., log, retry, or break out of the loop)
                pass
            else:
                break

        # Read folder names from the 'db' directory with retry mechanism
        while True:
            try:
                folders = [folder for folder in os.listdir(db_folder_path) if os.path.isdir(os.path.join(db_folder_path, folder))]
                time.sleep(0.1)
            except Exception as e:
                print(f"Error reading folders: {e}")
                # Handle the error (e.g., log, retry, or break out of the loop)
                pass
            else:
                break

        if request.method == 'POST':
            selected_folder = request.form.get('selected_folder')
            if selected_folder is not None:
                # Update the 'config.txt' file with the selected folder with retry mechanism
                while True:
                    try:
                        with open('config.txt', 'w') as file:
                            file.write(selected_folder)
                        time.sleep(0.1)
                    except Exception as e:
                        print(f"Error writing config.txt: {e}")
                        # Handle the error (e.g., log, retry, or break out of the loop)
                        pass
                    else:
                        break
                while True:
                    try:
                        with open('config.txt', 'r') as file:
                            current_value = file.read().strip()
                        time.sleep(0.1)
                    except Exception as e:
                        print(f"Error reading config.txt: {e}")
                        # Handle the error (e.g., log, retry, or break out of the loop)
                        pass
                    else:
                        break
                return render_template('adminpages/admin_ui.html', folders=folders, message=f'Current default value: {current_value}')
            else:
                # Handle the case when 'selected_folder' is None (not selected)
                return render_template('adminpages/admin_ui.html', folders=folders, message=f'Current default value: {current_value}')

        # If it's a GET request
        return render_template('adminpages/admin_ui.html', folders=folders, message=f'Current default value: {current_value}')
    else:
        return render_template('commonpages/notfound.html')


# Admin Management route
@app.route('/admin_management', methods=['GET', 'POST'])
def admin_management():
    admin = session.get('admin')
    if admin:
        file_path = "./static/admin/adminlogin.xlsx"
        df = read_excel_with_retry(file_path)
        
        if df is None:
            # Set a message for the template
            return render_template('adminpages/admin_management.html', file_not_found_message='File not found. No data to display.')

        if request.method == 'POST':
            try:
                if 'insert' in request.form:
                    # Get data from the form for inserting
                    adminid = request.form.get('adminid')
                    password = request.form.get('password')

                    # Check if the admin ID is unique before inserting
                    if adminid not in df['admin_id'].values:
                        # Append new data to the DataFrame
                        new_data = pd.DataFrame({'admin_id': [adminid], 'admin_password': [password]})
                        df = pd.concat([df, new_data], ignore_index=True)

                        # Write the updated DataFrame to the Excel file
                        write_excel_with_retry(df, file_path)
                        df = df.sort_values(by=['admin_id'])

                        # Set a success message
                        success_message = f"Admin ID '{adminid}' inserted successfully!"
                        return render_template('adminpages/admin_management.html', Admins=df.to_dict('records'), success_message=success_message)
                    else:
                        # Set an error message for duplicate admin ID
                        error_message = "Admin ID already exists. Please choose a unique ID."
                        return render_template('adminpages/admin_management.html', Admins=df.to_dict('records'), error_message=error_message)

                elif 'delete' in request.form:
                    # Get the user ID for deleting
                    userid_to_delete = request.form.get('adminid')

                    if len(df) <= 1:
                        error_message = "Cannot delete the last admin record."
                        return render_template('adminpages/admin_management.html', Admins=df.to_dict('records'), error_message=error_message)

                    # Check if the admin ID exists in the DataFrame
                    elif userid_to_delete in df['admin_id'].values:
                        # Remove the user with the specified ID
                        df = df[df['admin_id'] != userid_to_delete]

                        # Write the updated DataFrame to the Excel file
                        write_excel_with_retry(df, file_path)
                        df = df.sort_values(by=['admin_id'])
                        # Set a success message
                        success_message = f"Admin ID '{userid_to_delete}' deleted successfully!"
                        return render_template('adminpages/admin_management.html', Admins=df.to_dict('records'), success_message=success_message)
                    else:
                        # Set an error message for non-existent admin ID
                        error_message = f"Admin ID '{userid_to_delete}' does not exist."
                        return render_template('adminpages/admin_management.html', Admins=df.to_dict('records'), error_message=error_message)

            except Exception as e:
                print("Error:", e)
                # Set an error message
                error_message = 'An error occurred.'
                return render_template('adminpages/admin_management.html', Admins=df.to_dict('records'), error_message=error_message)

        return render_template('adminpages/admin_management.html', Admins=df.to_dict('records'))

# Admin New Academic Year route
@app.route('/admin_new_academic_year',methods=['GET', 'POST'])
def admin_new_academic_year():
    admin = session.get('admin')
    if admin:
        db_folder_path = 'db'
        folder_names = []

        while True:
            try:
                # Get folder names from the 'db' directory
                folder_names = [folder for folder in os.listdir(db_folder_path) if os.path.isdir(os.path.join(db_folder_path, folder))]
                time.sleep(0.1)
            except Exception as e:
                print(f"Error reading folder names: {e}")
                # Handle the error (e.g., log, retry, or break out of the loop)
                pass
            else:
                break

        return render_template('adminpages/admin_new_academic_year.html', folder_names=folder_names, db_folder_path=db_folder_path)

    return render_template('commonpages/notfound.html')


# Create Folder route
@app.route('/create_folder', methods=['POST'])
def create_folder():
    folder_name = request.form['folder_name']
    folder_path = os.path.join('db', folder_name)

    if os.path.exists(folder_path):
        db_folder_path = 'db'
        folder_names = [folder for folder in os.listdir(db_folder_path) if os.path.isdir(os.path.join(db_folder_path, folder))]
        message = f'The folder "{folder_name}" already exists.'
        return render_template('adminpages/admin_new_academic_year.html', message=message, folder_names=folder_names)

    # If the folder does not exist, create it
    os.makedirs(folder_path)

    # Process section data
    sections = ['Student', 'Employer', 'Faculty', 'Alumni']
    for section in sections:
        column_names = []
        column_names.append("RollNumber")
        column_names.append("Password")
        column_names.append("Department")
        column_names.append("Feedback")
        column_names.append("Name")
        column_names.append("MobileNumber")
        column_names.append("Email")
        column_names.append("Suggestion")

        input_prefix = section + "_"

        # Loop through input fields to get column names
        i = 0
        for key, value in request.form.items():
            if key.startswith(input_prefix):
                i = i + 1
                column_names.append(str(i) + "." + value)

        df = pd.DataFrame(columns=column_names)
        excel_file_path = os.path.join(folder_path, f'{section}.xlsx')
        
        # Write DataFrame to Excel file with retry mechanism
        write_excel_with_retry(df, excel_file_path)

    # Process 'Departments' data
    department_column_names = []

    for key, value in request.form.items():
        if key.startswith('Department'):
            department_column_names.append(value)

    # Create DataFrame for 'Departments' and save it as CSV with retry mechanism
    department_df = pd.DataFrame(columns=department_column_names)
    department_csv_path = os.path.join(folder_path, 'Departments.csv')
    write_csv_with_retry(department_df, department_csv_path)

    db_folder_path = 'db'
    folder_names = [folder for folder in os.listdir(db_folder_path) if os.path.isdir(os.path.join(db_folder_path, folder))]
    message = f'The folder "{folder_name}" and Excel files have been created successfully.'
    return render_template('adminpages/admin_new_academic_year.html', message=message, folder_names=folder_names)

# Delete Folder route
@app.route('/delete_folder', methods=['POST'])
def delete_folder():
    folder_name = request.form['delete_folder']
    folder_path = os.path.join('db', folder_name)

    if os.path.exists(folder_path):
        # Delete the folder and its contents
        shutil.rmtree(folder_path)
        db_folder_path = 'db'
        folder_names = [folder for folder in os.listdir(db_folder_path) if os.path.isdir(os.path.join(db_folder_path, folder))]
        message = f'The folder "{folder_name}" has been deleted.'
    else:
        message = f'The folder "{folder_name}" does not exist.'

    return redirect(url_for('admin_new_academic_year', message=message, folder_names=folder_names))


# Flask route - admin_set_defaults
@app.route('/admin_set_defaults', methods=['GET', 'POST'])
def admin_set_defaults():
    admin = session.get('admin')
    
    if admin:
        db_folder_path = 'db'
        folders = read_folder_names()

        # Read the current value from the 'config.txt' file
        current_value = read_config_file()

        if request.method == 'POST':
            selected_folder = request.form.get('selected_folder')
            if selected_folder is not None:
                # Update the 'config.txt' file with the selected folder
                
                write_config_file(selected_folder)
                current_value = selected_folder
                folders = read_folder_names()

                return render_template('adminpages/admin_ui.html', folders=folders, message=f'Current default value: {current_value}')
            else:
                # Handle the case when 'selected_folder' is None (not selected)
                return render_template('adminpages/admin_ui.html', folders=folders, message=f'Current default value: {current_value}')

        # If it's a GET request
        return render_template('adminpages/admin_ui.html', folders=folders, message=f'Current default value: {current_value}')
    
    return render_template('commonpages/notfound.html')



@app.route('/admin_new_stakeholder', methods=['GET', 'POST'])
def submit_manual_feedback():
    admin = session.get('admin')
    if admin:
        with open('config.txt', 'r') as file:
            current_value = file.read().strip()

        # Assuming the file path is db/current_value/Departments.csv
        departments_file_path = os.path.join('db', current_value, 'Departments.csv')

        # Read the 'DepartmentName' column using pandas
        departments = []
        try:
            # Use pandas to read CSV directly
            departments_df = pd.read_csv(departments_file_path)
            departments=departments_df.columns
            print(departments)
        except Exception as e:
            print(f"Error reading CSV file: {e}")



        if request.method == 'POST':
            roll_number = request.form.get('RollNumber')
            password = request.form.get('Password')
            department = request.form.get('Department')
            user_type = request.form.get('userType')

            status = process_submission(roll_number, password, department, user_type)


            return render_template('adminpages/admin_new_stakeholders.html', departments=departments, message=status)

        return render_template('adminpages/admin_new_stakeholders.html', departments=departments)
    else:
        return render_template('commonpages/notfound.html')

    


@app.route('/admin_new_stakeholder_drag', methods=['POST'])
def submit_drag_feedback():
    admin = session.get('admin')
    if admin:

        with open('config.txt', 'r') as file:
            current_value = file.read().strip()

        # Assuming the file path is db/current_value/Departments.csv
        departments_file_path = os.path.join('db', current_value, 'Departments.csv')

        # Read the 'DepartmentName' column using pandas
        departments = []
        try:
            # Use pandas to read CSV directly
            departments_df = pd.read_csv(departments_file_path)
            departments=departments_df.columns
            print(departments)
        except Exception as e:
            print(f"Error reading CSV file: {e}")
        try:
            if 'excelFile' in request.files:
                excel_file = request.files['excelFile']
                if excel_file.filename != '' and allowed_file(excel_file.filename):
                    df = pd.read_excel(excel_file)
                    entries = []

                    for index, row in df.iterrows():
                        roll_number = row['RollNumber']
                        password = row['Password']
                        user_type = row['UserType']
                        department = row['Department']

                        # Validate department name
                        if department not in departments:
                            status = f"Error: Department '{department}' not found in the list of valid departments."
                        else:
                            status = process_submission(roll_number, password, department, user_type)

                        entries.append({'RollNumber': roll_number, 'status': status, 'UserType': user_type})

                    return render_template('adminpages/admin_new_stakeholders.html', departments=departments, entries=entries, message="Excel file is inserted successfully. Check Status in Below Table.")

        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return render_template('adminpages/admin_new_stakeholders.html', departments=departments, message=e )

    else:
        return render_template('commonpages/notfound.html')
    
def process_submission(roll_number, password,Department, user_type):
    with open('config.txt', 'r') as file:
        current_value = file.read().strip()
    user_data_folder = os.path.join('db', current_value)

    # Validate, process, and store the data in the Excel file
    if (
        pd.notna(roll_number) and
        pd.notna(password) and
        pd.notna(Department) and
        pd.notna(user_type) and
        str(roll_number).strip() != "" and
        str(password).strip() != "" and
        str(Department).strip() != "" and
        str(user_type).strip() != ""
    ):
        user_data_file = os.path.join(user_data_folder, f'{user_type}.xlsx')

        # Check if the file exists
        if os.path.exists(user_data_file):
            # Read user data from the Excel file
            user_data = pd.read_excel(user_data_file)

            # Check if the RollNumber already exists
            if roll_number not in user_data['RollNumber'].values:
                # Create a new DataFrame with the provided data and 'Feedback' set to 'No'
                new_data = pd.DataFrame({'RollNumber': [roll_number], 'Password': [password],'Department':[Department], 'Feedback': ['No']})

                # Concatenate the new data with the existing DataFrame
                user_data = pd.concat([user_data, new_data], ignore_index=True)

                # Save the updated DataFrame back to the Excel file
                user_data.to_excel(user_data_file, index=False)
                return f"Data added successfully : {roll_number} in Department : {Department} "
            else:
                return f"This {roll_number} already exists in Department :- {Department} . Please choose a different one."

    return "Error: in form submission. Please provide valid values for all fields."




def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'xlsm', 'xlsb', 'csv', 'xltx', 'xltm', 'xls', 'xlt', 'xml', 'xlw', 'xlam', 'xla'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




@app.route('/AdminDashBoard', methods=['GET', 'POST'])
def AdminDashBoard():
    admin = session.get('admin')
    if admin:
        return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    alert_message = None
    if request.method == 'POST':
        userid = request.form['userid']
        password = request.form['password']
        user_type = request.form.get('user_type')

        with open('config.txt', 'r') as file:
            current_value = file.read().strip()

        user_data_folder = os.path.join('db', current_value)
        user_data_file = os.path.join(user_data_folder, f'{user_type}.xlsx')

        if os.path.exists(user_data_file):
            user_data = pd.read_excel(user_data_file)
         

            # Check if the provided username and password match any row in the DataFrame
            matching_user = user_data[(user_data['RollNumber'] == userid) & (user_data['Password'] == password)]

            if not matching_user.empty:
                feedback_status = matching_user['Feedback'].iloc[0]
                session['userid'] = True
                if feedback_status == 'Yes':
                    return render_template('feedbackpages/fbalreadydone.html',userid=userid,user_type=user_type)
                elif not matching_user.empty and user_type == 'Faculty':
                    return redirect(url_for('facultyfb',userid=userid,user_type=user_type))
                elif not matching_user.empty and user_type == 'Student':
                    return redirect(url_for('studentfb',userid=userid,user_type=user_type))
                elif not matching_user.empty and user_type == 'Alumni':
                    return redirect(url_for('alumnifb',userid=userid,user_type=user_type))
                elif not matching_user.empty and user_type == 'Employer':
                    return redirect(url_for('employerfb',userid=userid,user_type=user_type))
                else:
                    alert_message = "Incorrect username or password"
            else:
                alert_message = "Incorrect username or password"
        else:
            alert_message = "Invalid user type"

    return render_template('loginpages/login.html', alert_message=alert_message)





@app.route('/fbalreadydone', methods=['GET', 'POST'])
def fbalreadydone():
    if request.method == 'POST':
        # Assuming you have the necessary code to identify the user and update the feedback column
        userid = request.form['userid']
        user_type = request.form.get('user_type')

        with open('config.txt', 'r') as file:
            current_value = file.read().strip()

        user_data_folder = os.path.join('db', current_value)
        user_data_file = os.path.join(user_data_folder, f'{user_type}.xlsx')

        if os.path.exists(user_data_file):
            user_data = pd.read_excel(user_data_file)

            # Check if the provided username matches any row in the DataFrame
            matching_user = user_data[user_data['RollNumber'] == userid]

            if not matching_user.empty:
                # Update the Feedback column to 'No'
                user_data.loc[matching_user.index, 'Feedback'] = 'No'

                # Save the updated DataFrame back to the Excel file
                with pd.ExcelWriter(user_data_file) as writer:
                    user_data.to_excel(writer, index=False)
                # Redirect to the login route
                return redirect(url_for('login'))
            else:
                return  render_template('commonpages/notfound.html')
    else:
        return  render_template('commonpages/notfound.html')


@app.route('/facultyfb', methods=['GET', 'POST'])
def facultyfb():
    userid = request.args.get('userid')
    if session['userid'] == True:
        if request.method == 'POST':
            with open('config.txt', 'r') as file:
                current_value = file.read().strip()

            user_type = "Faculty"
            user_data_folder = os.path.join('db', current_value)
            user_data_file = os.path.join(user_data_folder, f'{user_type}.xlsx')
            df = pd.read_excel(user_data_file)

            # Specify names to be removed
            names_to_remove = ['RollNumber', 'Password','Department', 'Feedback', 'Name', 'MobileNumber', 'Email', 'Suggestion']

            # Remove specified names from the list of column names
            column_names = df.columns.tolist()
            for name in names_to_remove:
                if name in column_names:
                    column_names.remove(name)

            userid = request.form.get('userid')
            matching_row = df[df['RollNumber'] == userid]
            if not matching_row.empty:
                # Update the existing row with feedback values
                try:
                    feedback_data = {
                        'Name': request.form.get('Name'),
                        'MobileNumber': int(request.form.get('MobileNumber')),
                        'Email': request.form.get('Email'),
                        'Feedback': 'Yes',
                        'Suggestion': request.form.get('Suggestion')
                    }

                    for column_name in column_names:
                        feedback_value = request.form.get(column_name)
                        if feedback_value is not None:  # Skip columns not present in the form
                            # Explicitly convert to integer if possible
                            try:
                                feedback_data[column_name] = int(feedback_value)
                            except ValueError:
                                # If conversion to int fails, leave it as is
                                feedback_data[column_name] = feedback_value

                    # Create a new DataFrame with the updated values
                    updated_df = df.copy()

                    # Get the index of the matching row
                    index_to_update = matching_row.index[0]

                    # Update the row with feedback values
                    updated_df.loc[index_to_update, ['Name','MobileNumber','Email','Feedback','Suggestion'] + column_names] = feedback_data

                    try:
                        # Use pd.ExcelWriter to explicitly close the Excel file after writing
                        with pd.ExcelWriter(user_data_file) as writer:
                            updated_df.to_excel(writer, index=False)

                    except Exception as e:
                        print("Error writing to Excel file:", e)
                        return render_template('error.html')

                    return render_template('feedbackpages/fbdone.html')

                except Exception as e:
                    print("Error:", e)
                    return render_template('error.html')
            else:
                return render_template('error.html')

        try:
            with open('config.txt', 'r') as file:
                current_value = file.read().strip()

            userid = request.args.get('userid')
            user_type = "Faculty"
            user_data_folder = os.path.join('db', current_value)
            user_data_file = os.path.join(user_data_folder, f'{user_type}.xlsx')

            df = pd.read_excel(user_data_file)

            # Specify names to be removed
            names_to_remove = ['RollNumber', 'Password','Department', 'Feedback', 'Name', 'MobileNumber', 'Email', 'Suggestion']

            # Remove specified names from the list of column names
            column_names = df.columns.tolist()
            for name in names_to_remove:
                if name in column_names:
                    column_names.remove(name)

            return render_template('feedbackpages/facultysfb.html', userid=userid, column_names=column_names,
                                user_type=user_type)

        except Exception as e:
            print("Error:", e)
            return render_template('error.html')
    else:
        return render_template('loginpages/login.html', alert_message="UnAuthorized Login Attempt")
    





@app.route('/studentfb', methods=['GET', 'POST'])
def studentfb():
    userid = request.args.get('userid')
    if session['userid'] == True:
        if request.method == 'POST':
            with open('config.txt', 'r') as file:
                current_value = file.read().strip()

            user_type = "Student"
            user_data_folder = os.path.join('db', current_value)
            user_data_file = os.path.join(user_data_folder, f'{user_type}.xlsx')
            df = pd.read_excel(user_data_file)

            # Specify names to be removed
            names_to_remove = ['RollNumber', 'Password','Department', 'Feedback', 'Name', 'MobileNumber', 'Email', 'Suggestion']

            # Remove specified names from the list of column names
            column_names = df.columns.tolist()
            for name in names_to_remove:
                if name in column_names:
                    column_names.remove(name)

            userid = request.form.get('userid')
            matching_row = df[df['RollNumber'] == userid]
            if not matching_row.empty:
                # Update the existing row with feedback values
                try:
                    feedback_data = {
                        'Name': request.form.get('Name'),
                        'MobileNumber': int(request.form.get('MobileNumber')),
                        'Email': request.form.get('Email'),
                        'Feedback': 'Yes',
                        'Suggestion': request.form.get('Suggestion')
                    }

                    for column_name in column_names:
                        feedback_value = request.form.get(column_name)
                        if feedback_value is not None:  # Skip columns not present in the form
                            # Explicitly convert to integer if possible
                            try:
                                feedback_data[column_name] = int(feedback_value)
                            except ValueError:
                                # If conversion to int fails, leave it as is
                                feedback_data[column_name] = feedback_value

                    # Create a new DataFrame with the updated values
                    updated_df = df.copy()

                    # Get the index of the matching row
                    index_to_update = matching_row.index[0]

                    # Update the row with feedback values
                    updated_df.loc[index_to_update, ['Name','MobileNumber','Email','Feedback','Suggestion'] + column_names] = feedback_data

                    try:
                        # Use pd.ExcelWriter to explicitly close the Excel file after writing
                        with pd.ExcelWriter(user_data_file) as writer:
                            updated_df.to_excel(writer, index=False)
                        session['userid'] = False
                            
                    except Exception as e:
                        print("Error writing to Excel file:", e)
                        session['userid'] = False
                        return render_template('error.html')

                    return render_template('feedbackpages/fbdone.html')

                except Exception as e:
                    print("Error:", e)
                    session['userid'] = False
                    return render_template('error.html')
            else:
                session['userid'] = False
                return render_template('error.html')

        try:
            with open('config.txt', 'r') as file:
                current_value = file.read().strip()

            userid = request.args.get('userid')
            user_type = "Student"
            user_data_folder = os.path.join('db', current_value)
            user_data_file = os.path.join(user_data_folder, f'{user_type}.xlsx')

            df = pd.read_excel(user_data_file)

            # Specify names to be removed
            names_to_remove = ['RollNumber', 'Password','Department', 'Feedback', 'Name', 'MobileNumber', 'Email', 'Suggestion']

            # Remove specified names from the list of column names
            column_names = df.columns.tolist()
            for name in names_to_remove:
                if name in column_names:
                    column_names.remove(name)

            return render_template('feedbackpages/studentsfb.html', userid=userid, column_names=column_names,
                                user_type=user_type)

        except Exception as e:
            print("Error:", e)
            session['userid'] = False
            return render_template('error.html')
    else:
        session['userid'] = False
        return render_template('loginpages/login.html', alert_message="UnAuthorized Login Attempt")
    

@app.route('/alumnifb', methods=['GET', 'POST'])
def alumnifb():
    if session['userid'] == True:
        if request.method == 'POST':
            with open('config.txt', 'r') as file:
                current_value = file.read().strip()

            user_type = "Alumni"
            user_data_folder = os.path.join('db', current_value)
            user_data_file = os.path.join(user_data_folder, f'{user_type}.xlsx')
            df = pd.read_excel(user_data_file)

            # Specify names to be removed
            names_to_remove = ['RollNumber', 'Password','Department', 'Feedback', 'Name', 'MobileNumber', 'Email', 'Suggestion']

            # Remove specified names from the list of column names
            column_names = df.columns.tolist()
            for name in names_to_remove:
                if name in column_names:
                    column_names.remove(name)

            userid = request.form.get('userid')
            matching_row = df[df['RollNumber'] == userid]
            if not matching_row.empty:
                # Update the existing row with feedback values
                try:
                    feedback_data = {
                        'Name': request.form.get('Name'),
                        'MobileNumber': int(request.form.get('MobileNumber')),
                        'Email': request.form.get('Email'),
                        'Feedback': 'Yes',
                        'Suggestion': request.form.get('Suggestion')
                    }

                    for column_name in column_names:
                        feedback_value = request.form.get(column_name)
                        if feedback_value is not None:  # Skip columns not present in the form
                            # Explicitly convert to integer if possible
                            try:
                                feedback_data[column_name] = int(feedback_value)
                            except ValueError:
                                # If conversion to int fails, leave it as is
                                feedback_data[column_name] = feedback_value

                    # Create a new DataFrame with the updated values
                    updated_df = df.copy()

                    # Get the index of the matching row
                    index_to_update = matching_row.index[0]

                    # Update the row with feedback values
                    updated_df.loc[index_to_update, ['Name','MobileNumber','Email','Feedback','Suggestion'] + column_names] = feedback_data

                    try:
                        # Use pd.ExcelWriter to explicitly close the Excel file after writing
                        with pd.ExcelWriter(user_data_file) as writer:
                            updated_df.to_excel(writer, index=False)
                            session['userid'] = False
                            
                    except Exception as e:
                        print("Error writing to Excel file:", e)
                        session['userid'] = False
                        return render_template('error.html')

                    return render_template('feedbackpages/fbdone.html')

                except Exception as e:
                    print("Error:", e)
                    session['userid'] = False
                    return render_template('error.html')
            else:
                session['userid'] = False
                return render_template('error.html')

        try:
            with open('config.txt', 'r') as file:
                current_value = file.read().strip()

            userid = request.args.get('userid')
            user_type = "Alumni"
            user_data_folder = os.path.join('db', current_value)
            user_data_file = os.path.join(user_data_folder, f'{user_type}.xlsx')

            df = pd.read_excel(user_data_file)

            # Specify names to be removed
            names_to_remove = ['RollNumber', 'Password','Department', 'Feedback', 'Name', 'MobileNumber', 'Email', 'Suggestion']

            # Remove specified names from the list of column names
            column_names = df.columns.tolist()
            for name in names_to_remove:
                if name in column_names:
                    column_names.remove(name)

            return render_template('feedbackpages/alumnisfb.html', userid=userid, column_names=column_names,
                                user_type=user_type)

        except Exception as e:
            print("Error:", e)
            session['userid'] = False
            return render_template('error.html')
    else:
        session['userid'] = False
        return render_template('loginpages/login.html', alert_message="UnAuthorized Login Attempt")
    


@app.route('/employerfb', methods=['GET', 'POST'])
def employerfb():
    if session['userid'] == True:
        if request.method == 'POST':
            with open('config.txt', 'r') as file:
                current_value = file.read().strip()

            user_type = "Employer"
            user_data_folder = os.path.join('db', current_value)
            user_data_file = os.path.join(user_data_folder, f'{user_type}.xlsx')
            df = pd.read_excel(user_data_file)

            # Specify names to be removed
            names_to_remove = ['RollNumber', 'Password','Department', 'Feedback', 'Name', 'MobileNumber', 'Email', 'Suggestion']

            # Remove specified names from the list of column names
            column_names = df.columns.tolist()
            for name in names_to_remove:
                if name in column_names:
                    column_names.remove(name)

            userid = request.form.get('userid')
            matching_row = df[df['RollNumber'] == userid]
            if not matching_row.empty:
                # Update the existing row with feedback values
                try:
                    feedback_data = {
                        'Name': request.form.get('Name'),
                        'MobileNumber': int(request.form.get('MobileNumber')),
                        'Email': request.form.get('Email'),
                        'Feedback': 'Yes',
                        'Suggestion': request.form.get('Suggestion')
                    }

                    for column_name in column_names:
                        feedback_value = request.form.get(column_name)
                        if feedback_value is not None:  # Skip columns not present in the form
                            # Explicitly convert to integer if possible
                            try:
                                feedback_data[column_name] = int(feedback_value)
                            except ValueError:
                                # If conversion to int fails, leave it as is
                                feedback_data[column_name] = feedback_value

                    # Create a new DataFrame with the updated values
                    updated_df = df.copy()

                    # Get the index of the matching row
                    index_to_update = matching_row.index[0]

                    # Update the row with feedback values
                    updated_df.loc[index_to_update, ['Name','MobileNumber','Email','Feedback','Suggestion'] + column_names] = feedback_data

                    try:
                        # Use pd.ExcelWriter to explicitly close the Excel file after writing
                        with pd.ExcelWriter(user_data_file) as writer:
                            updated_df.to_excel(writer, index=False)
                            session['userid'] = False
                            
                    except Exception as e:
                        print("Error writing to Excel file:", e)
                        session['userid'] = False
                        return render_template('error.html')

                    return render_template('feedbackpages/fbdone.html')

                except Exception as e:
                    print("Error:", e)
                    session['userid'] = False
                    return render_template('error.html')
            else:
                session['userid'] = False
                return render_template('error.html')

        try:
            with open('config.txt', 'r') as file:
                current_value = file.read().strip()

            userid = request.args.get('userid')
            user_type = "Employer"
            user_data_folder = os.path.join('db', current_value)
            user_data_file = os.path.join(user_data_folder, f'{user_type}.xlsx')

            df = pd.read_excel(user_data_file)

            # Specify names to be removed
            names_to_remove = ['RollNumber', 'Password','Department', 'Feedback', 'Name', 'MobileNumber', 'Email', 'Suggestion']

            # Remove specified names from the list of column names
            column_names = df.columns.tolist()
            for name in names_to_remove:
                if name in column_names:
                    column_names.remove(name)

            return render_template('feedbackpages/employersfb.html', userid=userid, column_names=column_names,
                                user_type=user_type)

        except Exception as e:
            print("Error:", e)
            session['userid'] = False
            return render_template('error.html')
    else:
        session['userid'] = False
        return render_template('loginpages/login.html', alert_message="UnAuthorized Login Attempt")
    

@app.route('/FeedBackDone', methods=['GET', 'POST'])
def FeedBackDone():
    session['userid'] = False
    return render_template('feedbackpages/fbdone.html')

if __name__ == '__main__':
    app.run(debug=True)
