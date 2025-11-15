🚨 SwiftAid – Disaster Management System
DSA-based Flask Project using Priority Queue & Linked List

SwiftAid is a smart Disaster Reporting & Volunteer Management System built using:

Flask (Python Backend)

HTML, CSS, JS (Frontend)

Data Structures (Priority Queue + Linked List) for managing disasters & volunteers

Role-based users (Admin, Citizens, Volunteers)

This system allows users to report disasters, track volunteer responses, and manage tasks based on severity and priority.

📂 Project Structure
SwiftAid/
│── backend/
│     ├── app.py                     # Flask server
│     ├── disaster_system_dsa.py     # Core DSA logic (Priority Queue + Linked List)
│     ├── templates/                 # HTML templates served by Flask (if any)
│
│── frontend/
│     ├── index.html                 # Main UI
│     ├── temp.html                  # Experimental UI/testing
│
│── Datastructures/
│     ├── (DSA implementations used during development)
│
│── README.md
│── .gitignore

🚀 Features
👥 User Roles
Role	Description
Admin	Manages disasters, resolves cases, assigns volunteers
Citizen	Reports disasters with photo proof
Volunteer	Accepts tasks, updates status, shares live location
🧠 Core DSA Used
1️⃣ Priority Queue (Max-Heap / Custom PQ)

Used for sorting disasters based on:

severity

emergency level

timestamp

Ensures most severe disaster is handled first.

2️⃣ Linked List

Used for:

Storing volunteer update logs

Storing historical disaster records

Storing supply requirement lists

3️⃣ Hash Map

Used for:

Storing user credentials

Storing volunteer locations

Quick lookup of volunteers & reports

🔗 Backend API Endpoints (Flask)
Authentication
Method	Route	Purpose
POST	/api/login	User login
Disaster Reporting
Method	Route	Purpose
POST	/api/report	Report a disaster
GET	/api/view	View disasters
POST	/api/resolve	Resolve disaster with photo proof
POST	/api/delete-disaster	Delete own disaster
Volunteer Management
Method	Route	Purpose
GET	/api/volunteers	View all volunteers
POST	/api/assign	Assign volunteer manually
POST	/api/auto-assign	Auto assign based on availability
POST	/api/volunteer-update	Volunteer sends status update
POST	/api/location	Live location update
🏗️ How to Run the Project
1️⃣ Install Dependencies
pip install flask

2️⃣ Run Flask Backend

Go to backend folder:

cd backend
python app.py


Server will start at:

http://127.0.0.1:5000/

3️⃣ Open Frontend

Open manually:

frontend/index.html


OR
Connect frontend → backend using fetch() calls.


👨‍💻 Team Members

Sayam Bahuguna (B.Tech CSE, GEHU Dehradun)
Shubham Bhatt (B.Tech CSE, GEHU Dehradun)
Tanishq Rawat(B.Tech CSE, GEHU Dehradun)
Ayush Bhatt(B.Tech CSE, GEHU Dehradun)

📝 License

This project is for academic and educational use.
