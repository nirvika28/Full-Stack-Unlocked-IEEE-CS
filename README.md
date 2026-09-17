College Event Tracker — ZIP Description

The ZIP contains a simple full-stack College Event Tracker application built using HTML, CSS, JavaScript, Python Flask, and SQLite.

The project is divided into two main parts:

Frontend
index.html — structure of the event tracker and create-event form
style.css — styling for the application
script.js — handles API requests, displaying events, creating events, and registrations
Backend
app.py — Flask server containing the API routes and application logic
events.db — SQLite database storing event information
.env — backend environment configuration
Main functionality

The application allows users to:

View upcoming college events
Create a new event
Store event details in SQLite
Register for an event
Update the registration count

Backend flow
User
  ↓
HTML/CSS/JavaScript
  ↓
Flask API
  ↓
SQLite (events.db)
  ↓
JSON response
  ↓
Frontend# Full-Stack-Unlocked-IEEE-CS
