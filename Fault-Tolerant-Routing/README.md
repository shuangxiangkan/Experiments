# Augmented k-ary n-Cube Fault-Tolerant-Routing

## Setup

1. Create a virtual environment:

   ```sh
   python -m venv venv
   ```

2. Activate the virtual environment:

   - On Windows:

     ```sh
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```sh
     source venv/bin/activate
     ```

3. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

## Code Structure

- **`AugmentedKAryNCube.py`**: Contains the main logic for the augmented k-ary n-cube diagnosis algorithm.
- **`evaluation.py`**: Implements the experimental code to evaluate the algorithm's performance.

## Usage

Run the evaluation script to test the algorithm:

```sh
python3 evaluation.py
```