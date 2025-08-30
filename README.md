# PokéType Calculator 🎮⚡

A comprehensive Pokémon type effectiveness calculator that supports dual-type Pokémon and provides detailed damage multiplier calculations through both a REST API and interactive terminal interface. Includes powerful Pokémon data collection tools for building custom databases.

## ✨ Features

- **Dual-Type Support**: Calculate effectiveness for Pokémon with multiple types (e.g., Charizard Fire/Flying)
- **Real-time API**: RESTful API endpoint for type calculations
- **Interactive Terminal**: Command-line interface for multiple Pokémon lookups
- **Comprehensive Analysis**: Shows weaknesses, resistances, and immunities
- **Live Data**: Fetches Pokémon data from PokeAPI
- **Type Matrix**: Complete type effectiveness chart
- **Pokémon Database Builder**: Collect and store comprehensive Pokémon data including abilities, types, and legendary status
- **Data Export**: Generate JSON databases with custom Pokémon information

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Internet connection (for PokeAPI access)

### Installation
```bash
git clone https://github.com/Kushagra-Agnihotri/Poke-Type-Calculator.git
cd Poke-Type-Calculator
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

### Pokémon Data Collection
Build custom Pokémon databases with comprehensive information:

```bash
python pokiapi_pokemon_list.py output_database.json
```

**What it collects:**
- Pokémon ID and name
- Type information (single or dual types)
- Abilities list
- Legendary status
- Mythical status

**Input:** `pokemon.txt` file with Pokémon names (one per line)
**Output:** Structured JSON database

### API Endpoints

#### Get Type Effectiveness
