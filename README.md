# python-static-site-generator

Another boot.dev tutorial for funsies

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd python-static-site-generator
   ```

2. **Create a Virtual Environment**:
   ```bash
   python3 -m venv .venv
   ```

3. **Activate the Virtual Environment**:
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run Tests**:
   ```bash
   ./test.sh
   ```

6. **Run the Application**:
   ```bash
   ./main.sh
   ```

## Project Structure

- `src/`: Contains the source code for the static site generator.
- `public/`: Output directory for the generated static site.
- `test.sh`: Script to run all tests.
- `main.sh`: Script to run the application.
- `requirements.txt`: Lists all Python dependencies.

## Notes

Ensure you always activate the virtual environment before running any scripts or commands to maintain consistency.
