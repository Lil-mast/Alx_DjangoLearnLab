# Django Blog Authentication System

## Overview

This Django blog application features a complete user authentication system with registration, login, logout, and profile management functionality. The system extends Django's built-in authentication with custom forms and additional user profile fields.

## Features

- **User Registration**: Custom registration form with email validation
- **User Login/Logout**: Secure session-based authentication
- **Profile Management**: Extended user profiles with bio and profile picture
- **CSRF Protection**: All forms include CSRF token protection
- **Password Security**: Uses Django's built-in PBKDF2 hashing algorithm
- **Responsive Design**: Styled templates with CSS
- **Flash Messages**: User feedback for successful operations and errors

## Technology Stack

- **Backend**: Django 4.2+
- **Database**: SQLite (default), PostgreSQL/MySQL ready
- **Templates**: Django Template Language (DTL)
- **Static Files**: CSS, JavaScript
- **Authentication**: Django built-in auth with custom extensions

## Installation & Setup

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtualenv (recommended)

### Installation Steps

1. **Clone the repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd django_blog