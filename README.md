# IT-403---Group-1-Project
TaskFlow a Project Management web-app using django framework

TaskFlow is a collaborative project management web application designed to streamline task allocation, project tracking, and team collaboration. Built with Django, TaskFlow integrates essential features like user authentication, task scheduling, Gantt chart visualizations, and a Kanban board for efficient project handling.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Development Team](#development-team)
- [Milestones](#milestones)
- [Setup Instructions](#setup-instructions)
- [Contributing](#contributing)

---

## Features

1. **Member Management**  
   - Role: Project Manager  
   - Manage user accounts (edit, delete, password changes).

2. **Authentication**  
   - Role: Authentication Developer  
   - Account registration, login/logout with validation.

3. **Project and Task Management**  
   - Role: Task & Project Management Specialist  
   - Create projects, schedule tasks, assign priorities.

4. **Task Visualization**  
   - Role: Visualization Expert  
   - Gantt chart integration and project reports.

5. **Notifications and File Sharing**  
   - Role: Notifications & File Sharing Developer  
   - Alerts for tasks and a secure file-sharing system.

6. **Kanban Board**  
   - Role: Kanban Specialist  
   - Drag-and-drop functionality for task visualization.

7. **User Interface**  
   - Role: Frontend Specialist  
   - Consistent layout with alerts and prompts for better UX.

---

## Project Structure

### Week 1: Setup and Core Feature Development
- Django project setup and database schema design.
- Development of core features:
  - Authentication (Flameño)
  - Layout and Navigation (Santiago)
  - Member Management (Raymundo)
  - Project and Task Management (Odiada)
- Basic integration and testing.

### Week 2: Advanced Features and Integration
- Implement advanced features:
  - User Profiles (Raymundo)
  - Notifications (Flameño)
  - Task Management (Mariano)
  - Gantt Chart Visualization (Samonte)
  - Kanban Board (Santos)
- Debugging and integration.

### Week 3: Finalization and Deployment
- Finalizing File Sharing and UI enhancements.
- Comprehensive testing and documentation.
- Deployment and presentation.

---

## Development Team

- **Raymundo (Project Manager):** Oversees progress, Member Management, User Profiles.
- **Santiago (Frontend Specialist):** UI/UX design and alerts.
- **Flameño (Authentication Developer):** Handles registration and login/logout.
- **Odiada (Task & Project Management Specialist):** Develops project and task management features.
- **Samonte (Visualization Expert):** Creates Gantt charts and reporting.
- **Flameño (Notifications & File Sharing Developer):** Builds notifications and file-sharing features.
- **Mariano (Task Management Developer):** Implements task management for members.
- **Santos (Kanban Specialist & Tester):** Designs the Kanban board and conducts testing.

---

## Milestones

### Week 1
- Core feature development and initial testing.

### Week 2
- Development of advanced features and integration.

### Week 3
- Finalization, testing, deployment, and presentation.

---

## Setup Instructions

**Clone the repository:**
   ```bash
   git clone https://github.com/Shorton04/TaskFlow.git
   cd project_management
   pip install -r requirements.txt
   python manage.py migrate
   Access the application at http://127.0.0.1:8000/login
```

## Contributing
We welcome contributions! Please fork this repository and create a pull request with your changes. Ensure your code adheres to the project's coding standards.
```bash
   git add .
   git commit -m "<describe-your-changes>"
   git checkout -b <your-branch-name> //this is for the ones who dont have their branch yet
   git push origin <your-branch-name>
```

## License and Copyright
© 2024 TaskFlow Development Team. All rights reserved.

