# Feature Specification: Smart Todo & Task CLI

## Requirements
1. Task CRUD Operations:
   - add <title> [--tags t1,t2] [--priority low|med|high]: Task create karega sequential ID ke sath. Default status pending.
   - list [--status pending|done] [--tag <tag>] [--sort priority|id]: Filtered aur sorted tasks print karega.
   - update <id> [--status pending|done] [--priority low|med|high]: Task fields update karega.
   - delete <id>: Specified task delete karega.
2. JSON Persistence:
   - Data tasks.json file me structured format me persist hoga.
3. Deterministic Exit Codes:
   - 0: Successful execution.
   - 1: Validation error / non-existent task ID / invalid argument.

## Acceptance Criteria
- AC-1: Empty title dene par CLI error output aur exit code 1 dega.
- AC-2: Existing tasks ko tag aur status dono ke basis par filter kiya ja sakega.
- AC-3: Priority sorting strictly high > med > low order follow karegi.
- AC-4: Non-existent ID par update ya delete call karne par exit code 1 aayega.
