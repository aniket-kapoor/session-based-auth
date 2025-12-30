# session-based-auth
Secure session-based authentication API using FastAPI with cookie sessions, database-stored session tracking, and password hashing.

A production-style session-based authentication system built using FastAPI & SQLAlchemy.
Users authenticate via secure HTTP-only cookies, and active sessions are stored in the database with expiry timestamps — similar to how real-world web apps manage login sessions.


Features
--> Login with email + password
--> Secure session cookies (HttpOnly, Secure, SameSite)
--> Database-stored sessions with expiry
--> Logout with session revocation
--> User lookup from active session
--> Password hashing
--> Invalid & expired session handling
--> Proper HTTP status codes
--> Clean dependency-based authentication (get_current_user)


Tech Stack

Python
FastAPI
SQLAlchemy / ORM
PostgreSQL 
Passlib / bcrypt
Uvicorn
Pydantic
