# Election Systems Simulation

This project simulates various voting systems to compare their outcomes based on a set of candidates and voter
preferences. It allows for the exploration of different electoral processes, including popular vote, ranked-choice,
redistribution, and last-remaining candidate systems, as well as a weighted system that combines results from others.

## Installation

To set up the project, it is recommended to use a virtual environment to manage dependencies.

1.  **Navigate to the project directory**:
    ```bash
    cd py/elections
    ```

2.  **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    ```

3.  **Activate the virtual environment**:
    *   On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```

4.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the simulation from the project root directory.

```bash
python main.py [OPTIONS]
```

### Arguments

You can specify one or more voting systems to run, or omit them to run all systems by default.

*   `--debug`: Turns on debug logging for more verbose output.
*   `--noise`: Introduces random noise into the simulation, affecting voter behavior or candidate attributes.
*   `--no_log`: Disables all logging output to the console and log files.
*   `--weighted`: Runs the weighted voting system, which combines results from other systems. This system will only run
                    if at least one other voting system is also selected or if all systems are run by default.

**Individual Voting Systems (can be combined):**

*   `--popular`: Runs the Popular Voting System.
*   `--ranked`: Runs the Ranked Choice Voting System.
*   `--redist`: Runs the Redistribution Voting System.
*   `--remaining`: Runs the Last Remaining Candidate Voting System.

**Example:**

To run only the ranked-choice and weighted systems with debug logging:

```bash
python main.py --ranked --weighted --debug
```

To run all voting systems with noise:

```bash
python main.py --noise
```
