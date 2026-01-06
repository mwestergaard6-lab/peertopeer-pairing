<img width="1416" height="772" alt="Screenshot 2026-01-05 at 7 42 25 PM" src="https://github.com/user-attachments/assets/7fc1afc0-3dd8-408c-8a87-334cd2ed41f7" /># Peer-to-Peer Pairing

## About the Peer-to-Peer Program

Peer-to-Peer is a student-run tutoring program at my school that connects students who need academic support with classmates who are able to help. The program is built around the idea that learning is often most effective when it happens between peers — students who understand the coursework, the pace of classes, and the challenges of balancing school with life.

Before this project, the program relied heavily on manual coordination: collecting responses through forms, sorting students by subject, and trying to create fair mentor–mentee matches by hand. As participation grew, this process became time-consuming and difficult to update when students joined late, changed availability, or needed help in new subjects.

This project is an attempt to turn Peer-to-Peer into a system that is easier to manage, more transparent, and more adaptable as the program grows.

---

## Why I Built This App

I built this app because I’ve been directly involved in Peer-to-Peer and saw how much effort went into tasks that should be simple: matching students by subject, regenerating pairs, and keeping track of who is helping whom.

At the same time, I was learning backend development and wanted to build something that was not just a demo, but actually connected to a real problem in my school community. This project allowed me to combine:

- my interest in building tools that improve access to academic support,
- my experience working with peer tutoring programs,
- and my growing skills in Python, APIs, and frontend-backend integration.

Rather than designing an abstract app, I focused on a real workflow: **students → subjects → mentor/mentee pairings**. Every design choice in this project reflects that goal.

---

## How the App Works (System Overview)

The application has three main parts:

1. A **FastAPI backend** that handles student data, pairing logic, and API endpoints  
2. A **simple frontend** (HTML, CSS, JavaScript) that allows users to interact with the system  
3. A **database layer** that stores students and generated mentor–mentee pairs  

Students are created with identifying information (name, school, subject, and role). Based on subject compatibility, the backend can generate mentor–mentee pairs and return them in a readable format. The frontend then displays this information so it can be reviewed or regenerated as needed.

---

## Backend & API Design (FastAPI)

The backend is built using **FastAPI**, which allowed me to:

- clearly define request and response structures
- validate incoming data using Pydantic models
- automatically generate interactive documentation

FastAPI’s built-in documentation was especially useful while developing and testing the API, because it made it easy to see exactly what data was being sent and returned.

### FastAPI Interactive Documentation

Below is a screenshot of the automatically generated FastAPI documentation (`/docs`). This interface allowed me to test endpoints directly in the browser and confirm that the backend behaved correctly before connecting it to the frontend.
<img width="1621" height="638" alt="Screenshot 2026-01-05 at 7 36 02 PM" src="https://github.com/user-attachments/assets/6dfb6952-de5f-4f18-9a54-04642ca6c9ec" />

---

## Student Data & Request Models

Students are represented using a structured data model that defines required fields such as name, school, and subject. This ensures that all student data entering the system is consistent and valid.

By enforcing structure at the API level, the app avoids common issues like missing fields or incorrect data types, which is especially important when the system is later used to generate pairings automatically.
<img width="1416" height="772" alt="Screenshot 2026-01-05 at 7 42 25 PM" src="https://github.com/user-attachments/assets/155f88e0-40ed-41d4-a180-d8836584e83f" />

---

## Pairing Logic

One of the core features of the app is the ability to generate mentor–mentee pairs based on subject compatibility. When the pairing endpoint is triggered:

- existing pairings are cleared
- students are grouped by subject
- mentors and mentees are matched accordingly
- the results are stored and returned in a readable format

This makes it easy to regenerate pairings whenever the student list changes, without manually redoing the entire process.
<img width="1594" height="624" alt="Screenshot 2026-01-05 at 7 45 42 PM" src="https://github.com/user-attachments/assets/e2905996-ba8b-4416-986d-54f7daebec11" />

---

## Frontend Integration

The frontend is intentionally simple, focusing on clarity and functionality. It allows users to:

- create new students through a form
- trigger pairing generation
- view current mentor–mentee pairs

JavaScript is used to send requests to the FastAPI backend and dynamically update the page based on the API responses. This helped me understand how frontend interfaces communicate with backend services in real applications.
<img width="1072" height="882" alt="Screenshot 2026-01-05 at 7 47 37 PM" src="https://github.com/user-attachments/assets/ad83adc9-6eb5-4e54-87c4-4696c5f018dc" />


---

## What This Project Taught Me

This project helped me understand how real systems are built across multiple layers:

- designing data models that reflect real-world constraints  
- building APIs that are clear, testable, and reusable  
- connecting backend logic to a user-facing interface  
- debugging across the stack when things didn’t work as expected  

More importantly, it showed me how software can directly support educational access and peer collaboration — values that are central to why I’m interested in computer science.
## Future Features & Planned Improvements

While the current version of Peer-to-Peer focuses on core functionality and clarity, there are several features I plan to add to make the platform more engaging, useful, and reflective of how students actually interact.

### Stronger & More Engaging UI
I plan to continue improving the visual design of the frontend to make the platform feel more welcoming and intuitive for students. This includes:
- a more polished layout with consistent spacing and typography  
- clearer visual hierarchy for forms, buttons, and pairing results  
- improved color schemes and interactive feedback (hover states, transitions)

A stronger UI would make the platform feel less like a tool and more like a community space students enjoy using.

### Messaging Between Mentors and Mentees
A key planned feature is a built-in messaging system that allows mentors and mentees to communicate directly through the platform. This would allow students to:
- coordinate meeting times
- ask quick questions outside of sessions
- clarify expectations before working together

From a technical perspective, this would involve designing new database tables for messages, creating authenticated endpoints, and managing message retrieval in a clean and secure way.

### More Flexible Pairing Logic
Future versions could support:
- students helping with multiple subjects
- preference-based matching (availability, grade level)
- smarter pairing algorithms to balance workload across mentors

These improvements would allow the system to better reflect the complexity of real peer tutoring programs.

---

## Long-Term Vision

The long-term goal of Peer-to-Peer is to create a platform that lowers the barrier to academic support and encourages collaboration between students. By combining thoughtful backend design with an approachable frontend, I hope to continue building tools that support learning, equity, and student-led initiatives within schools.
