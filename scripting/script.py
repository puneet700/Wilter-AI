import json
import sys
import os


def check_dict_diff(before: dict, after: dict):
    """Returns a set of keys that differ between two dictionaries."""
    before = before or {}
    after = after or {}
    all_keys = set(before.keys()).union(set(after.keys()))
    
    modified_keys = set()
    for key in all_keys:
        if before.get(key) != after.get(key):
            modified_keys.add(key)
    return modified_keys

def validate_tfplan(plan_file_path: str) -> bool:
    if not os.path.exists(plan_file_path):
        print(f"Error: File '{plan_file_path}' not found.")
        return False

    try:
        with open(plan_file_path, "r", encoding="utf-8") as f:
            plan_data = json.load(f)
    except Exception as e:
        print(f"Error reading/parsing JSON: {e}")
        return False

    resource_changes = plan_data.get("resource_changes", [])
    violations = []

    for rc in resource_changes:
        address = rc.get("address", "unknown_resource")
        change = rc.get("change", {})
        actions = change.get("actions", [])

        # 1. Ignore 'no-op' and 'read' operations (e.g., data sources)
        if actions == ["no-op"] or actions == ["read"]:
            continue

        # 2. Check for create action
        if actions == ["create"]:
            continue

        # 3. Check for delete / destroy actions
        if "delete" in actions:
            violations.append(
                f"[DENIED] Resource '{address}' has action '{','.join(actions)}'. Deletions are forbidden."
            )
            continue

        # 4. Check for update / modify actions
        if actions == ["update"]:
            before = change.get("before") or {}
            after = change.get("after") or {}

            changed_attrs = check_dict_diff(before, after)

            # Rule: Only 'tags' (or 'tags_all') can be modified
            disallowed_attrs = [attr for attr in changed_attrs if attr not in ("tags", "tags_all")]
            if disallowed_attrs:
                violations.append(
                    f"[DENIED] Resource '{address}' modifies non-tag attributes: {disallowed_attrs}."
                )
                continue

            # If tags were modified, verify that ONLY 'GitCommitHash' changed
            for tag_attr in ("tags", "tags_all"):
                if tag_attr in changed_attrs:
                    before_tags = before.get(tag_attr) or {}
                    after_tags = after.get(tag_attr) or {}
                    changed_tag_keys = check_dict_diff(before_tags, after_tags)

                    disallowed_tags = [k for k in changed_tag_keys if k != "GitCommitHash"]
                    if disallowed_tags:
                        violations.append(
                            f"[DENIED] Resource '{address}' modifies unauthorized tag keys: {disallowed_tags}. Only 'GitCommitHash' is allowed."
                        )
            continue

        # Any other action pattern (e.g. replace -> ["delete", "create"])
        violations.append(
            f"[DENIED] Resource '{address}' requires an unsupported action flow: {actions}."
        )

    # Print summary & action decision
    print("=" * 60)
    print(f"Plan Evaluation: {os.path.basename(plan_file_path)}")
    print("=" * 60)

    if violations:
        print("\nACTION REQUIRED: DO NOT PROCEED WITH TERRAFORM APPLY\n")
        print("Violations:")
        for violation in violations:
            print(f"  - {violation}")
        print("\nResult: Apply Rejected [REJECTED]\n")
        return False
    else:
        print("\nACTION REQUIRED: PROCEED WITH TERRAFORM APPLY\n")
        print("Result: Apply Approved [APPROVED]\n")
        return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <path_to_tfplan.json>")
        sys.exit(1)

    plan_path = sys.argv[1]
    is_valid = validate_tfplan(plan_path)
    sys.exit(0 if is_valid else 1)
