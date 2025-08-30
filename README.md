# PokéType Calculator 🎮⚡

A comprehensive Pokémon type effectiveness calculator that supports dual-type Pokémon and provides detailed damage multiplier calculations through both a REST API and interactive terminal interface.

## ✨ Features

- **Dual-Type Support**: Calculate effectiveness for Pokémon with multiple types (e.g., Charizard Fire/Flying)
- **Real-time API**: RESTful API endpoint for type calculations
- **Interactive Terminal**: Command-line interface for multiple Pokémon lookups
- **Comprehensive Analysis**: Shows weaknesses, resistances, and immunities
- **Live Data**: Fetches Pokémon data from PokeAPI
- **Type Matrix**: Complete type effectiveness chart

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Internet connection (for PokeAPI access)

### Installation
```bash
git clone https://github.com/yourusername/poketype-calculator.git
cd poketype-calculator
pip install requests
```

### Running the Application
```bash
python pokichart_server.py
```

The server will start on `http://localhost:8000` and you can interact with it through the terminal.

## 📖 Usage

### Terminal Interface
1. Run the script
2. Enter a Pokémon name (e.g., `charizard`, `pikachu`)
3. View detailed type analysis
4. Enter another Pokémon or type `quit` to exit

### API Endpoints

#### Get Type Effectiveness
