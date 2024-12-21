# Court Management System

A comprehensive Django-based system for managing court bookings, schedules, and resources.

## Branches

The project has two main branches:

### 1. SQLite Branch (main-sqlite)
- Uses SQLite as the database
- Simplified Docker setup
- Ideal for development and testing
- Easier to get started
- All services run in a single container

### 2. MySQL Branch (main-mysql)
- Uses MySQL as the database
- Production-ready setup
- Separate containers for each service
- More complex but more scalable
- Better for production deployment

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

- Docker and Docker Compose
- Git
- Redis (for Celery task queue)
- Stripe CLI (for webhook testing)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd CourtManagementSystem
   ```

2. Choose your branch:

   For SQLite (simpler setup):
   ```bash
   git checkout main-sqlite
   ```

   For MySQL (production setup):
   ```bash
   git checkout main-mysql
   ```

3. Create a `.env` file in the root directory with the following variables:
   ```
   DEBUG=True
   SECRET_KEY=your_secret_key
   STRIPE_SECRET_KEY=your_stripe_secret_key
   STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
   ```

4. Build and run the containers:

   For SQLite branch:
   ```bash
   docker-compose up --build
   ```
   This will start:
   - Combined Django web application and Celery worker
   - Redis server
   - Stripe CLI for webhook testing

   For MySQL branch:
   ```bash
   docker-compose up --build
   ```
   This will start:
   - Django web application
   - MySQL database
   - Redis server
   - Celery worker
   - Stripe CLI for webhook testing

5. The application will be available at:
   - Web interface: http://localhost:8000
   - Admin panel: http://localhost:8000/admin

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
├── docker/               # Docker configuration files
├── requirements.txt      # Python dependencies
├── docker-compose.yml    # Docker services configuration
├── Dockerfile           # Docker build instructions
└── manage.py            # Django management script
```

## Configuration

### SQLite Branch
- Database: SQLite (file-based)
- Configuration is minimal
- Database file is stored in the container
- Redis for Celery task queue
- Stripe CLI for payment webhook testing

### MySQL Branch
- Database: MySQL
- Requires additional environment variables for database configuration
- Separate database container
- Persistent volume for database data
- Redis for Celery task queue
- Stripe CLI for payment webhook testing

## Development vs Production

### Development (SQLite Branch)
- Quick to set up
- No database configuration needed
- Single container deployment
- Ideal for development and testing

### Production (MySQL Branch)
- Scalable architecture
- Better performance for concurrent users
- Separate services for better resource management
- Proper service isolation
- Data persistence with volumes

## Manual Installation

If you prefer to run the application without Docker, please refer to our [Manual Installation Guide](docs/manual-installation.md).

## Development

- Follow PEP 8 style guide
- Write tests for new features
- Update requirements.txt when adding new dependencies

## Testing

Run the test suite:
```bash
python manage.py test
```

## Contributing

Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
