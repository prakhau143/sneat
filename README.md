# Sneat Django Converted

A complete Django Jinja2 conversion of the Sneat-1.0.0 UI template with all original styling, components, and functionality preserved.

## 🎯 **Project Overview**

This project converts the original Sneat HTML admin template into a fully functional Django application using Jinja2 templating engine. All the original Sneat UI components, styling, and layout have been preserved while making them Django-compatible.

## ✨ **Features**

- **Exact UI Replication**: 100% identical to the original Sneat-1.0.0 template
- **Django Jinja2 Integration**: Full Django framework integration with Jinja2 templating
- **Responsive Design**: Bootstrap 5 responsive grid system
- **Modern Components**: Cards, forms, tables, modals, and more
- **Icon Support**: Boxicons integration for beautiful icons
- **Theme Support**: Light theme with customizable color schemes

## 🏗️ **Technology Stack**

- **Backend**: Django 5.0.2
- **Templating**: Jinja2 3.1.3
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Icons**: Boxicons
- **Charts**: ApexCharts
- **Database**: SQLite (default)

## 📁 **Project Structure**

```
sneat-django-converted/
├── sneat_project/           # Django project settings
│   ├── __init__.py
│   ├── settings.py          # Django configuration
│   ├── urls.py             # Main URL routing
│   ├── wsgi.py             # WSGI configuration
│   ├── asgi.py             # ASGI configuration
│   └── jinja2.py           # Jinja2 environment setup
├── sneat_app/              # Django application
│   ├── __init__.py
│   ├── apps.py             # App configuration
│   ├── views.py            # View functions
│   └── urls.py             # App URL routing
├── templates/               # Jinja2 templates
│   ├── base.html           # Base template with navigation
│   ├── dashboard.html      # Main dashboard
│   ├── auth/               # Authentication templates
│   │   ├── login.html      # Login page
│   │   └── register.html   # Registration page
│   ├── cards.html          # Cards components
│   ├── forms.html          # Form components
│   ├── tables.html         # Table components
│   ├── ui.html             # UI components
│   ├── pages.html          # Page examples
│   └── layouts.html        # Layout examples
├── static/                  # Static assets (copied from Sneat)
│   ├── assets/             # CSS, JS, images
│   │   ├── css/            # Stylesheets
│   │   ├── js/             # JavaScript files
│   │   ├── img/            # Images and icons
│   │   └── vendor/         # Third-party libraries
├── manage.py               # Django management script
└── requirements.txt        # Python dependencies
```

## 🚀 **Installation & Setup**

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### Installation Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd sneat-django-converted
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   - Main Application: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin

## 📱 **Available Pages**

### **Main Pages**
- **Dashboard** (`/`) - Main analytics dashboard with charts and statistics
- **Cards** (`/cards/`) - Various card components and layouts
- **Forms** (`/forms/`) - Form components and input examples
- **Tables** (`/tables/`) - Data table examples with actions
- **UI Components** (`/ui/`) - Buttons, badges, alerts, modals
- **Pages** (`/pages/`) - Account settings, notifications, security
- **Layouts** (`/layouts/`) - Layout options and grid system

### **Authentication Pages**
- **Login** (`/auth/login/`) - User authentication
- **Register** (`/auth/register/`) - User registration

## 🎨 **UI Components**

### **Cards**
- Transaction cards
- Revenue growth cards
- Sales overview cards
- Statistics cards

### **Forms**
- Basic input fields
- Input sizing options
- Checkboxes and radio buttons
- Input groups

### **Tables**
- Responsive data tables
- User management tables
- Order tracking tables
- Action dropdowns

### **UI Elements**
- Button variations (primary, secondary, outline)
- Badge styles and colors
- Alert components
- Progress bars
- Modal dialogs
- Tooltips and popovers

### **Layouts**
- Container vs fluid layouts
- Responsive grid system
- Flexbox utilities
- Spacing utilities

## 🔧 **Customization**

### **Adding New Pages**
1. Add a new view in `sneat_app/views.py`
2. Add URL pattern in `sneat_app/urls.py`
3. Create a new template in `templates/` directory
4. Extend `base.html` for consistent layout

### **Modifying Styles**
- CSS files are located in `static/assets/css/`
- Main styles: `static/assets/vendor/css/core.css`
- Theme styles: `static/assets/vendor/css/theme-default.css`
- Custom styles: `static/assets/css/demo.css`

### **Adding JavaScript**
- JavaScript files are in `static/assets/js/`
- Main scripts: `static/assets/js/main.js`
- Dashboard scripts: `static/assets/js/dashboards-analytics.js`

## 📱 **Responsive Design**

The template is fully responsive and includes:
- Mobile-first approach
- Bootstrap 5 grid system
- Responsive navigation
- Touch-friendly interfaces
- Optimized for all screen sizes

## 🌐 **Browser Support**

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Internet Explorer 11+

## 📚 **Documentation**

For more information about the original Sneat template:
- [Sneat Documentation](https://themeselection.com/demo/sneat-bootstrap-html-admin-template/documentation/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.0/)
- [Django Documentation](https://docs.djangoproject.com/)

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 **License**

This project is based on the Sneat template by ThemeSelection. Please refer to the original template's license for usage terms.

## 🙏 **Acknowledgments**

- **ThemeSelection** for the original Sneat template
- **Bootstrap** team for the excellent CSS framework
- **Django** team for the powerful web framework
- **Jinja2** team for the templating engine

## 📞 **Support**

For support and questions:
- Check the documentation
- Review the code examples
- Open an issue on the repository

---

**Note**: This is a UI-only conversion. All backend functionality (authentication, database operations, etc.) needs to be implemented according to your specific requirements.
