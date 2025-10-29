# WildOps: Wildlife Conservation Drone Operations Management System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/django-4.2-green.svg)](https://www.djangoproject.com/)

**WildOps** is a comprehensive web-based platform designed to streamline and enhance drone operations for wildlife conservation projects. Developed to support unmanned aircraft system (UAS) operations in protected wildlife areas, this system provides tools for operation planning, standardized procedures generation, weather monitoring, and airspace management.

## 🌟 Features

### 📋 Operation Planning & Management
- **Operation Request System**: Create and manage drone operation requests with detailed parameters
- **Geospatial Mapping**: Interactive map interface for defining operation areas with coordinates and radius
- **Temporal Scheduling**: Define operation time windows with automatic activation state management
- **Multi-User Support**: Role-based access control for pilots, administrators, and viewers
- **Operation Status Tracking**: Monitor request status (requested, approved, declined) and activation state (active, inactive, expired)

### 📄 Standardized Procedures (WildProcedures)
- **Dynamic Checklist Generation**: Automatically generate flight-specific checklists based on:
  - Operation type (VLOS, BVLOS)
  - Drone platform (DJI, Autel, etc.)
  - Number of drones (single, multiple)
- **Comprehensive Coverage**: Checklists include all operational phases:
  - Operation planning
  - Pre-operation checks
  - Packing and equipment
  - First flight procedures
  - Pre-flight, in-flight, and post-flight operations
  - Post-operation procedures
  - Contingency and emergency procedures
- **PDF Export**: Generate professional PDF checklists for field use

### 🌤️ Weather Monitoring
- **Real-time Weather Data**: Integration with WeatherAPI for current conditions
- **Location-based Forecasts**: Automatic weather retrieval based on operation coordinates
- **Safety Thresholds**: Configurable weather limits for safe drone operations
- **GeoDB Cities Integration**: Location search and coordinates lookup

### 🗺️ Airspace Visualization
- **Flight Cylinders Display**: 3D visualization of active operation zones
- **UTM Integration**: Unmanned Traffic Management system compatibility
- **Conflict Detection**: Identify overlapping operations in time and space
- **Interactive Dashboard**: Real-time view of all active operations

### 👥 User Management
- **Authentication System**: Secure login and user registration
- **Permission Groups**: Customizable user roles and permissions
- **Activity Tracking**: Monitor who created which operations

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- pip (Python package installer)
- Git
- Virtual environment tool (venv or virtualenv)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YourUsername/wildops_public.git
   cd wildops_public
   ```

2. **Create and activate a virtual environment**
   ```bash
   # On Linux/macOS
   python3 -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env

   # Edit .env and add your configuration
   nano .env  # or use your preferred editor
   ```

   Required environment variables:
   - `SECRET_KEY`: Django secret key (generate a new one!)
   - `DEBUG`: Set to `False` in production
   - `ALLOWED_HOSTS`: Your domain names or IP addresses
   - `WEATHERAPI_KEY`: Get from [WeatherAPI](https://www.weatherapi.com/)
   - `RAPIDAPI_KEY`: Get from [RapidAPI GeoDB Cities](https://rapidapi.com/wirefreethought/api/geodb-cities/)

5. **Generate a new Django secret key**
   ```bash
   python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   ```
   Copy the output and set it as your `SECRET_KEY` in `.env`

6. **Navigate to the project directory**
   ```bash
   cd WildOpsProject
   ```

7. **Apply database migrations**
   ```bash
   python manage.py migrate
   ```

8. **Create user groups and permissions**
   ```bash
   python manage.py create_groups
   ```

9. **Create a superuser account**
   ```bash
   python manage.py createsuperuser
   ```

10. **Run the development server**
    ```bash
    python manage.py runserver
    ```

11. **Access the application**
    - Open your browser and go to: `http://127.0.0.1:8000/`
    - Admin panel: `http://127.0.0.1:8000/admin/`

## 📖 Usage

### Creating a New Operation

1. Log in to the system
2. Navigate to the Operations page
3. Fill in the operation details:
   - Remote Pilot in Command (RPIC)
   - UAS platform and ID
   - Location (latitude, longitude, radius)
   - Date and time window
   - Operation type (VLOS/BVLOS)
   - Drone platform and number of drones
4. Submit for approval

### Generating Procedures Checklist

1. Go to the WildProcedures section
2. Select your operation parameters:
   - Operation type
   - Drone platform
   - Number of drones
3. Click "Generate Checklist"
4. Review the comprehensive checklist
5. Download as PDF for field use

### Checking Weather Conditions

1. Access the Weather Check module
2. Enter the operation location or select from existing operations
3. View current weather conditions
4. Check if conditions meet safety thresholds
5. Make go/no-go decisions based on data

### Managing Operations (Administrators)

1. Access the admin panel
2. Review pending operation requests
3. Approve or decline based on airspace availability
4. Monitor active operations
5. View operation history and analytics

## 🛠️ Configuration

### Weather Thresholds

Edit `WildOpsProject/weather_check/data/json/weather_thresholds.json` to customize safe operating limits:
- Wind speed
- Temperature ranges
- Visibility requirements
- Precipitation limits

### User Permissions

The system includes four default permission groups:
- **Pilots**: Can create and view their own operations
- **Operations Managers**: Can approve/decline operations
- **Administrators**: Full system access
- **Viewers**: Read-only access to operation data

Customize groups using the Django admin panel.

### Scheduled Tasks

Set up automatic operation state updates:

```bash
# Edit crontab
crontab -e

# Add this line to run every minute
* * * * * /path/to/wildops_public/WildOpsProject/scripts/run_update_activation_state.sh
```

This automatically updates operation activation states (active/inactive/expired) based on current time.

## 📁 Project Structure

```
wildops_public/
├── WildOpsProject/          # Main Django project directory
│   ├── accounts/            # User authentication and management
│   ├── MapApp/              # Operation mapping and visualization
│   ├── WildProcedures/      # Checklist generation module
│   ├── weather_check/       # Weather monitoring module
│   ├── shared/              # Shared constants and utilities
│   ├── WildOpsProject/      # Core settings and configuration
│   ├── templates/           # HTML templates
│   ├── static/              # Static files (CSS, JS, images)
│   ├── media/               # User-uploaded files
│   ├── scripts/             # Automation scripts
│   └── manage.py            # Django management script
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
├── README.md               # This file
├── LICENSE                 # MIT License
└── CONTRIBUTING.md         # Contribution guidelines
```

## 🔧 Development

### Running Tests

```bash
cd WildOpsProject
python manage.py test
```

### Database Migrations

When modifying models:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting Static Files

For production deployment:

```bash
python manage.py collectstatic
```

## 🌍 Deployment

### Production Checklist

- [ ] Set `DEBUG = False` in environment variables
- [ ] Generate and set a strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Set up a production database (PostgreSQL recommended)
- [ ] Configure a web server (Nginx, Apache)
- [ ] Set up WSGI server (Gunicorn, uWSGI)
- [ ] Enable HTTPS with SSL certificates
- [ ] Configure static and media file serving
- [ ] Set up automated backups
- [ ] Configure logging and monitoring
- [ ] Set up the cron job for automatic state updates

### Example Deployment with Gunicorn

```bash
# Install gunicorn
pip install gunicorn

# Run gunicorn
gunicorn --bind 0.0.0.0:8000 WildOpsProject.wsgi:application
```

For detailed deployment instructions, see Django's [deployment documentation](https://docs.djangoproject.com/en/4.2/howto/deployment/).

## 🤝 Contributing

We welcome contributions from the community! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Start for Contributors

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests to ensure everything works
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 Citation

If you use WildOps in your research or project, please cite:

```bibtex
@software{wildops2025,
  author = {Maalouf, Guy},
  title = {WildOps: Wildlife Conservation Drone Operations Management System},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/YourUsername/wildops_public}
}
```

## 🙏 Acknowledgments

- Developed for wildlife conservation drone operations
- Inspired by best practices in UAS operations and safety management
- Thanks to all contributors and the open-source community

## 📞 Contact & Support

- **Issues**: Please report bugs and request features through [GitHub Issues](https://github.com/YourUsername/wildops_public/issues)
- **Discussions**: Join our [community discussions](https://github.com/YourUsername/wildops_public/discussions)

## 🗺️ Roadmap

- [ ] Mobile application for field operations
- [ ] Real-time flight tracking integration
- [ ] Advanced weather forecasting with machine learning
- [ ] Multi-language support
- [ ] API for third-party integrations
- [ ] Enhanced reporting and analytics
- [ ] Integration with additional UAS platforms

## ⚠️ Disclaimer

This software is provided as-is for drone operation management. Users are responsible for ensuring compliance with local aviation regulations, obtaining necessary permits, and following all applicable safety guidelines. The developers assume no liability for improper use or accidents.

---

**Made with ❤️ for wildlife conservation**
