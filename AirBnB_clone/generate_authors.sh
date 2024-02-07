#!/bin/bash

# Generate a list of authors in the Git repository

# Run git shortlog to get a summary of git log output, displaying the author emails
# along with the number of commits they've made
git shortlog -se |
  # Use Perl to remove the leading commit counts from each line
  perl -spe 's/^\s+\d+\s+//' |
  # Use sed to filter out any lines containing a specific pattern, such as "CommitSyncScript"
  sed -e '/^CommitSyncScript.*$/d' \
  # Write the filtered list of authors to a file named AUTHORS
  > AUTHORS
