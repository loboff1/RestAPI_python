# RestAPI_python

This is a REST API built using Flask and SQLAlchemy. 

Setup 
----------------

1. Create a PostgreSQL database called "mydatabase" with a username and password .
2. Update the SQLALCHEMY_DATABASE_URI in the code.

Running the API
----------------
To run the API, follow these steps:

1. Install the required dependencies by running: 

          pip install flask flask_sqlalchemy.
    
2. Run the code by executing the api.py file.

3. The API will be accessible at http://localhost:5000


API
----------------

**Get Employees**

  - Path: /employees
  
  - Method: GET
  
  - Response: Returns a list of all employees.

**Get Positions**

  - Path: /positions
  
  - Method: GET
  
  - Response: Returns a list of all positions.

**Get Departments**

  - Path: /departments
  
  - Method: GET
  
  - Response: Returns a list of all departments.

**Get Employee by ID**

  - Path: /employees/{id}
  
  - Method: GET
  
  - Response: Returns the details of an employee with the given ID.

**Get All Employees**

  - Path: /employees/all
  
  - Method: GET
  
  - Response: Returns a list of all employees with their positions and departments.

**Add Employee**

  - Path: /employees
  
  - Method: POST
  
  - Request Body: JSON object with the fields: first_name, last_name, position_id, department_id
  
- Response: Returns a message indicating the success of adding the employee.
