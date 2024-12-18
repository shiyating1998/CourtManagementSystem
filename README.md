# Court Management System

A comprehensive Django-based system for managing court bookings, schedules, and resources.

## Features

- Court booking and reservation management
- User authentication and authorization
- Automated scheduling system
- Payment integration with Stripe
- Asynchronous task processing with Celery
- Email notifications
- Holiday management
- Administrative dashboard

## Prerequisites

- Python 3.12+
- MySQL
- Redis (for Celery)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd CourtManagementSystem
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory with the following variables:
   ```
   DEBUG=True
   SECRET_KEY=your_secret_key
   DATABASE_URL=mysql://user:password@localhost:3306/court_management
   STRIPE_SECRET_KEY=your_stripe_secret_key
   STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
   ```

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Start Redis server (required for Celery)

7. Start Celery worker:
   ```bash
   celery -A app worker -l info -P eventlet
   ```

8. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Project Structure

```
CourtManagementSystem/
├── app/                    # Main application directory
│   ├── management/        # Custom management commands
│   ├── migrations/        # Database migrations
│   ├── templates/         # HTML templates
│   ├── templatetags/      # Custom template tags
│   ├── models.py          # Database models
│   ├── views.py           # View controllers
│   ├── tasks.py          # Celery tasks
│   └── utils.py          # Utility functions
├── static/                # Static files (CSS, JS, images)
├── courtManagementSystem/ # Project settings
└── manage.py             # Django management script
```

## Development

- Follow PEP 8 style guide
- Write tests for new features
- Update requirements.txt when adding new dependencies

## Testing

Run the test suite:
```bash
python manage.py test
```

## License

[Your License Here]
