# Personal Finance Manager 💰

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-red.svg)](https://streamlit.io/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.27-green.svg)](https://www.sqlalchemy.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A modern, user-friendly personal finance management application built with Python and Streamlit. Track your income and expenses, visualize your financial data, and make informed financial decisions.

![Dashboard Preview](docs/images/dashboard.png)

## ✨ Features

- 📊 Interactive dashboard with financial metrics
- 💰 Track income and expenses with categories
- 📈 Visual financial trends and analytics
- 🗓️ Monthly and yearly financial reports
- 📱 Responsive design for all devices
- 💾 Local SQLite or cloud MongoDB storage
- 📤 Export data to CSV or Excel
- 🔒 Secure data handling

## 🖥️ Screenshots

<table>
  <tr>
    <td><img src="docs/images/dashboard.png" alt="Dashboard" width="400"/></td>
    <td><img src="docs/images/transactions.png" alt="Transactions" width="400"/></td>
  </tr>
  <tr>
    <td><img src="docs/images/reports.png" alt="Reports" width="400"/></td>
    <td><img src="docs/images/add_transaction.png" alt="Add Transaction" width="400"/></td>
  </tr>
</table>

## 🚀 Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/finance_manager.git
cd finance_manager
```

2. Create and activate virtual environment:
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment:
```bash
# Windows
copy .env.example .env

# Linux/macOS
cp .env.example .env
```

5. Run the application:
```bash
streamlit run src/app.py
```

## 🏗️ Project Structure

```
finance_manager/
├── src/
│   ├── database/          # Database models and management
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── db_manager.py
│   ├── utils/            # Utility functions
│   │   ├── __init__.py
│   │   └── helpers.py
│   ├── views/            # UI components
│   │   ├── __init__.py
│   │   ├── dashboard.py
│   │   ├── transactions.py
│   │   └── reports.py
│   └── app.py           # Main application
├── data/                # Database storage
├── tests/              # Test files
├── docs/              # Documentation
│   └── images/       # Screenshots and images
├── .env.example     # Environment template
└── requirements.txt # Dependencies
```

## 🔧 Configuration

The application can be configured using environment variables in `.env`:

```ini
# Database Configuration
USE_MONGODB=false
MONGODB_URI=mongodb://localhost:27017/
DB_NAME=finance_manager

# Application Settings
DEBUG=true
EXPORT_PATH=./exports
SECRET_KEY=your-secret-key-here
```

## 📊 Features in Detail

### Dashboard
- Overview of income and expenses
- Category-wise distribution
- Monthly trends
- Net savings calculator

### Transaction Management
- Add/Edit/Delete transactions
- Categorize transactions
- Add notes and dates
- Filter by date range

### Reports
- Monthly financial reports
- Category-wise analysis
- Export to CSV/Excel
- Custom date range reports

## 🧪 Testing

Run the test suite:
```bash
pytest tests/
```

## 🛠️ Development

1. Fork the repository
2. Create a feature branch
```bash
git checkout -b feature/amazing-feature
```
3. Commit your changes
```bash
git commit -m 'Add amazing feature'
```
4. Push to the branch
```bash
git push origin feature/amazing-feature
```
5. Open a Pull Request

## 📝 Code Style

This project uses:
- Black for code formatting
- Flake8 for linting

Format code before committing:
```bash
black .
flake8
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing framework
- [SQLAlchemy](https://www.sqlalchemy.org/) for database ORM
- [Plotly](https://plotly.com/) for interactive visualizations

## 📬 Contact

Your Name - [@yourusername](https://twitter.com/yourusername)

Project Link: [https://github.com/yourusername/finance_manager](https://github.com/yourusername/finance_manager) 