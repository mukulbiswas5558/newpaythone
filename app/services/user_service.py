from app.database import db
from app.models.user_model import CreateUser, LoginUser,UpdateUser
from app.utils.auth import create_access_token, verify_password, get_password_hash
from datetime import datetime


# User service function for creating a user
async def create_user_service(user: CreateUser):
    # Check if the username already exists in the database
    query_check = "SELECT id FROM users WHERE username = $1"
    existing_user = await db.fetch_one(query_check, user.username)

    # If the username exists, raise an exception
    if existing_user:
       
       return {"message": "Username already exists. Please login."}

    # Hash the password using the method in CreateUser model
    hashed_password = get_password_hash(user.password)

    # Insert the new user into the database with hashed password
    query = """
    INSERT INTO users (name, username, password, role) 
    VALUES ($1, $2, $3, $4) 
    RETURNING id, name, username, role;
    """
    result = await db.fetch_one(query, user.name, user.username, hashed_password, user.role)

    # Create the access token after successful registration
    user_data = {
        "username": user.username,
        "role": user.role
    }

    # Create a token with an expiry time of 30 minutes
  
    access_token = create_access_token(data=user_data)

    return {"user": dict(result), "access_token": access_token}

async def login_user_service(user: LoginUser):
    # Fetch the user from the database
    query = "SELECT id, username, password, role FROM users WHERE username = $1"
    db_user = await db.fetch_one(query, user.username)

    if not db_user:
        return {"message": "Invalid username or password"}

    # Verify the password
    if not verify_password(user.password, db_user['password']):

        return {"message": "Invalid username or password"}

    # Prepare JWT payload
    user_data = {
        "username": db_user['username'],
        "role": db_user['role']
    }
    access_token = create_access_token(data=user_data)

    # Return user information and token
    return {
        "user": {
            "id": db_user['id'],
            "username": db_user['username'],
            "role": db_user['role']
        },
        "access_token": access_token
    }


async def update_user_service(username: str, user_data: UpdateUser):
    """
    Update a user's details in the database using static SQL.

    Args:
        username (str): The username of the user to update.
        user_data (UpdateUser): The new data for the user.

    Returns:
        dict: Updated user information or an error message.
    """
    try:
        # Static SQL Query to update all fields
        query = """
        UPDATE users
        SET phone = $1, department = $2, shift_information = $3, employee_type = $4, 
            job_position = $5, reporting_manager = $6, work_location = $7, work_type = $8, 
            salary = $9, company = $10, bank_name = $11, branch = $12, bank_address = $13, 
            bank_code_1 = $14, bank_code_2 = $15, account_number = $16, bank_country = $17, 
            address_line_1 = $18, address_line_2 = $19, city = $20, district = $21, 
            state = $22, country = $23, postal_code = $24, updated_at = CURRENT_TIMESTAMP
        WHERE username = $25
        RETURNING id, username, phone, department, shift_information, employee_type, job_position, 
                  reporting_manager, work_location, work_type, salary, company, bank_name, branch, 
                  bank_address, bank_code_1, bank_code_2, account_number, bank_country, address_line_1, 
                  address_line_2, city, district, state, country, postal_code, updated_at;
        """

        # Values for the query (order of fields must match the query placeholders)
        values = [
            user_data.phone, user_data.department, user_data.shift_information, user_data.employee_type,
            user_data.job_position, user_data.reporting_manager, user_data.work_location, user_data.work_type,
            user_data.salary, user_data.company, user_data.bank_name, user_data.branch, user_data.bank_address,
            user_data.bank_code_1, user_data.bank_code_2, user_data.account_number, user_data.bank_country,
            user_data.address_line_1, user_data.address_line_2, user_data.city, user_data.district,
            user_data.state, user_data.country, user_data.postal_code, username
        ]

        # Execute the query and get the updated user
        updated_user = await db.fetch_one(query, *values)

        if not updated_user:
            return {"message": "User not found or update failed."}

        return {
            "message": "User updated successfully.",
            "user": updated_user
        }

    except Exception as e:
        print(f"Error while updating user: {e}")
        return {"message": "An error occurred while updating the user."}

