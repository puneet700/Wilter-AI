# Add steps/actions here:

1. step 1
Refactor from count to for_each
By switching from count to for_each, each resource instance is tied to an explicit identifier (e.g., "0", "2", "3", "4") rather than a consecutive array index.

variable "files" {
  type    = set(string)
  default = ["0", "2", "3", "4"]
}

resource "local_file" "foo" {
  for_each = var.files
  content  = "# Some content for file ${each.key}"
  filename = "file${each.key}.txt"
}

3. step 2
Migrate the Existing State
Map the existing count instances in state to the new for_each keys:

Bash
terraform state mv 'local_file.foo[0]' 'local_file.foo["0"]'
terraform state mv 'local_file.foo[2]' 'local_file.foo["2"]'
terraform state mv 'local_file.foo[3]' 'local_file.foo["3"]'
terraform state mv 'local_file.foo[4]' 'local_file.foo["4"]'


3. Step 3
Remove the 2nd Resource from State and Disk

Bash
terraform state rm 'local_file.foo[1]'
rm file1.txt


4. Step 4
Verify
Run terraform apply. Because all remaining files match their new keys in state and code, Terraform will report:


"No changes. Your infrastructure matches the configuration."
