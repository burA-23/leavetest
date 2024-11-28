from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
import dbexec

# My first Monolithic app.
app = Flask(__name__)

# Simple in-memory data store for leave information
leave_data = {}

def is_weekend(date):
    return date.weekday() >= 5  # Saturday or Sunday

def is_holiday(date, holidays):
    month_holidays = holidays.get(date.month, [])
    return date.day in month_holidays

def calculate_leave_end_date(start_date, leave_duration, holidays):
    current_date = start_date
    leave_days =0

    while leave_days < leave_duration:
        if not is_weekend(current_date) and not is_holiday(current_date, holidays):
            leave_days += 1
        current_date += timedelta(days=1)
    return current_date - timedelta(days=1)

def calculate_report_date(end_date,holidays):
    current_date=end_date + timedelta(days=1)
    while is_weekend(current_date) or is_holiday(current_date,holidays):
        current_date += timedelta(days=1)
   
    return current_date  
    #


# Example of a holiday dictionary
holidays_dict = {
    1: [1],        # January: New Year's Day
    5: [1],        # Labour Day
    6: [1],        # Madaraka Day
    10: [10, 20],
    12: [12, 25, 26],   # December: Christmas Day, Boxing Day
    # Add more months and holidays as needed
}

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/leave_form', methods=['GET', 'POST'])
def leave_form():
    if request.method == 'POST':
        # Get data from the form
        username = request.form.get('username')
        designation=request.form.get('Designation')
        personal_Number = request.form.get('Personal Number')
        start_date_input = request.form.get('start_date')
        leave_duration = int(request.form.get('leave_duration'))

        # Convert start date input to datetime
        start_date = datetime.strptime(start_date_input, '%Y-%m-%d')

        # Calculate the end date of leave considering weekends and holidays
        end_date = calculate_leave_end_date(start_date, leave_duration, holidays_dict)
        #Calculate the report date '"   "
        report_date = calculate_report_date(end_date,holidays_dict)

        # Insert data into the db
        dbexec.insert_leave_request(
                username, designation, personal_Number,
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d"),
                report_date.strftime("%Y-%m-%d")
        )
        return redirect(url_for('leave_status'))

        # Update leave_data dictionary
       # leave_data[username] =(designation,personal_Number,start_date.strftime("%Y/%m/%d"),end_date.strftime("%Y/%m/%d"),report_date.strftime("%Y/%m/%d")) # This worked.
        #{'PersonalNumber': personal_Number,'End date': end_date}- (This produced a bug about string formatting in relation to the datetime module.)

        #return render_template('leave_status.html', leave_data=leave_data)

    return render_template('leave_form.html')

@app.route('/leave_status')
def leave_status():
    leave_data= dbexec.fetch_all_leave_requests()
    return render_template('leave_status.html',leave_data=leave_data)

#@app.route('/Sick_leave',methods=['GET','POST'])
#def sick_leave_form():
   # if request.method == 'POST':
    #    username =request.form.get('username')
     #   designation=request.form.get('Designation')
       # pesrsonal_Number

if __name__ == '__main__':
    dbexec.initialize_db()
    app.run(host="0.0.0.0",port=8080,debug=True)
