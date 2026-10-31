# Clarifications

- **Q1: What is the format for Task IDs?**
  - **Resolution**: Sequential integer IDs (1, 2, 3...) must be used.
- **Q2: What is the expected behavior when the storage file is missing?**
  - **Resolution**: If `tasks.json` does not exist, the system initializes with an empty list and creates the file upon saving.
