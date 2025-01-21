## MCA Project Report: K-Connect Group Messaging Application

### 1. Introduction

K-Connect is a group messaging application built using Django and Django REST Framework. It allows users to create and join groups, send messages within groups, and manage group memberships.  The application utilizes email-based OTP verification for secure login.  This report details the design and implementation of the K-Connect API.

### 2. System Architecture

The KConnect application follows a Model-View-Controller (MVC) architecture, facilitated by Django's framework.  The key components are:

* **Models (`models.py`):** Define the data structures for users, groups, group members, and messages.
* **Serializers (`serializers.py`):**  Transform model instances into JSON format for API responses and validate incoming data for API requests.
* **Views (`views.py`):** Handle API requests, interact with models and serializers, and return API responses.
* **URLs (`urls.py`):** Map API endpoints to corresponding views.
* **Utilities (`utils.py`):** Contain helper functions for tasks like sending OTP emails and adding group members.

### 3. Data Model

The application's data model consists of the following entities:

* **User (`User`):** Stores user information (name, email, phone, password, OTP secret).  Uses a custom user manager for email-based authentication.
* **Group (`Group`):** Represents a messaging group (name, description, icon, created by).
* **Group_member (`Group_member`):**  Links users to groups and tracks membership status (is_admin, is_suspend).
* **Message (`Message`):** Stores message data (group, sender, message content, sent time, message type).

### 4. API Endpoints

The following API endpoints are available:

| Endpoint | Method | Description | Authentication |
|---|---|---|---|
| `/login/` | POST | Initiates login by sending an OTP to the user's email. | None |
| `/login/verify/` | POST | Verifies the OTP and logs in the user. | None |
| `/account/` | GET | Lists all user accounts (excluding admins). | Any |
| `/account/` | POST | Creates a new user account. | Admin |
| `/account/d/<int:u_id>/` | DELETE | Deletes a user account (excluding superuser). | Admin |
| `/profile/` | GET | Retrieves the current user's profile. | Authenticated |
| `/profile/` | PUT | Updates the current user's profile. | Authenticated |
| `/group/` | GET | Lists all groups. | Admin |
| `/group/` | POST | Creates a new group. | Admin |
| `/group/<uuid:g_id>/` | GET | Retrieves group details. | Authenticated |
| `/group/add-member/` | POST | Adds members to a group. | Authenticated |
| `/group/messages/` | POST | Retrieves messages for a specific group. | Authenticated |
| `/message/c/` | POST | Creates a new message. | Authenticated |
| `/logout/` | POST | Logs out the current user. | Authenticated |


### 5. Security

K-Connect employs the following security measures:

* **OTP Verification:** Two-factor authentication using email-based OTPs enhances login security.
* **Password Hashing:** User passwords are securely stored using Django's built-in password hashing mechanisms.
* **Permission Control:** API endpoints are protected using Django REST Framework's permission classes (IsAuthenticated, IsAdminUser, AllowAny) to restrict access based on user roles.

### 6. Future Enhancements

* **Real-time Messaging:** Implement WebSockets for real-time message delivery.
* **File Sharing:**  Enhance message functionality to support file attachments.
* **Push Notifications:**  Notify users of new messages through push notifications.
* **Group Management Features:**  Allow group admins to manage members (suspend, remove, promote).
* **Improved Search:** Implement search functionality for messages and users.

### 7. Conclusion

K-Connect provides a basic but functional group messaging platform. The application demonstrates effective use of Django and Django REST Framework for building secure and scalable APIs. Future enhancements will focus on improving the user experience and adding more advanced features.
