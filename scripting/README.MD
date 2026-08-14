# Terraform Plan Safety Validator

A Python-based validation tool developed and tested within **Jupyter Notebook** to inspect Terraform JSON execution plans (`tfplan.json`) and strictly enforce deployment safety policies before `terraform apply` is executed.

---

# Project Overview

When running automated CI/CD pipelines or manual infrastructure updates, changes must often adhere to strict governance guardrails. This project verifies that:
1. The plan only contains **`create`** or **`update`** operations.
2. If an **`update` (modify)** occurs, it is **strictly limited to the `tags` (or `tags_all`) attribute**.
3. Within `tags`, **only the `GitCommitHash` key is permitted to change**.
4. If any resource is marked for **`delete`**, **`replace`**, or modifies any other infrastructure attribute, the apply is blocked and specific violation details are displayed.

---

# How It Was Built

The script was developed interactively using a **Jupyter Notebook** environment:
- **`%%writefile` Command:** Used inside the notebook to generate and maintain `scripting/script.py`.
- **JSON Parsing & Diff Logic:** Standard library `json` module parses the Terraform plan schema (`resource_changes`), comparing `before` and `after` dictionary states.
- **Cross-Platform Output Compatibility:** Formatted output with plain-text status markers (`[APPROVED]` / `[REJECTED]`) to prevent encoding issues (`cp1252`) across Windows and Unix-like environments.

---



# How to Run

### Method 1: Command Line (CLI)

Run the script directly by passing the path to the converted Terraform plan file:

```bash
# Single plan check
python scripting/script.py scripting/tfplan-1.json
```


### Method 2: Inside Jupyter Notebook

You can write and execute the script directly inside notebook cells:

1. **Write/Update Script File:**
   ```python
   %%writefile scripting/script.py
   # (Validation script code)
   ```

2. **Execute and Validate:**
   ```python
   !python scripting/script.py scripting/tfplan-1.json
   ```

---

## Example Output

### Approved Plan Example
```text
============================================================
Plan Evaluation: tfplan-1.json
============================================================

ACTION REQUIRED: PROCEED WITH TERRAFORM APPLY

Result: Apply Approved [APPROVED]
```

### Rejected Plan Example
```text
============================================================
Plan Evaluation: tfplan-delete-sample.json
============================================================

ACTION REQUIRED: DO NOT PROCEED WITH TERRAFORM APPLY

Violations:
  - [DENIED] Resource 'azurerm_resource_group.rg' has action 'delete'. Deletions are forbidden.
  - [DENIED] Resource 'azurerm_data_factory.main' modifies non-tag attributes: {'location'}.

Result: Apply Rejected [REJECTED]
