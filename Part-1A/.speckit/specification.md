# Feature Specification: Smart Todo & Task CLI

## Requirements

### 1. Task CRUD Operations:
- `add <title> [--tags t1,t2] [--priority low|med|high]`: Creates a task with a sequential integer ID. Default status is `pending`.
- `list [--status pending|done] [--tag ] [--sort priority|id]`: Displays filtered and sorted tasks.
- `update [--status pending|done] [--priority low|med|high]`: Updates designated task attributes.
- `delete `: Removes the specified task from the store.

### 2. JSON Persistence:
- Task records must persist in structured format within `tasks.json`.

### 3. Deterministic Exit Codes:
- `0`: Successful execution.
- `1`: Validation error, non-existent task ID, or invalid argument.

## Acceptance Criteria
- **AC1**: Adding a task must save it immediately with status `pending`.
- **AC2**: Filter by status and tag must return exact matches.
- **AC3**: Sorting by priority must strictly follow ordering: `HIGH > MED > LOW`.
- **AC4**: Updating a non-existent task must exit with code 1 and return a descriptive error.
