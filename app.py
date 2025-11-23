from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Global in-memory storage (reset when app restarts)
# students stores strings: ["Alice", "Bob"]
# grades stores lists of numbers: [[90, 80], [100]]
students = []
grades = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/students', methods=['GET', 'POST'])
def students_page():
    if request.method == 'POST':
        # Handle adding a new student
        if 'student_name' in request.form:
            name = request.form.get('student_name')
            if name and name not in students:
                students.append(name)
                grades.append([]) # Initialize an empty grade list for this student
        
        # Handle adding a grade to an existing student
        elif 'grade_value' in request.form and 'student_index' in request.form:
            try:
                s_index = int(request.form.get('student_index'))
                g_value = float(request.form.get('grade_value'))
                grades[s_index].append(g_value)
            except ValueError:
                pass # Handle invalid input gracefully
                
        return redirect(url_for('students_page'))

    # Zip data so we can loop through names and their specific grades together in HTML
    # enumerate helps us track the index for the form submission
    student_data = zip(range(len(students)), students, grades)
    return render_template('students.html', student_data=student_data, students=students)

@app.route('/averages')
def averages_page():
    # Calculate averages on the fly
    results = []
    for i in range(len(students)):
        student_name = students[i]
        student_grades = grades[i]
        
        if len(student_grades) > 0:
            avg = sum(student_grades) / len(student_grades)
            avg = round(avg, 2)
        else:
            avg = "No grades"
            
        results.append({'name': student_name, 'average': avg})
        
    return render_template('averages.html', results=results)

if __name__ == '__main__':
    # Host='0.0.0.0' makes it accessible from outside the Docker container
    app.run(debug=True, host='0.0.0.0', port=5000)