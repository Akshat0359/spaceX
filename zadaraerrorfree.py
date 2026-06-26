import re
from collections import defaultdict

def parse_logs(filepath):
    lines = []

    with open(filepath, 'r') as f:
        for line in f:
            lines.append(process_line(line)) #used with statement

    return lines

def process_line(line):
    parts = line.strip().split(' ', 3)
    if len(parts) < 4:
        raise ValueError(f"Malformed line: {line!r}")
    return {
        'timestamp': parts[0] + ' ' + parts[1],
        'level':     parts[2].strip('[]'),
        'message':   parts[3]
    }

from collections import defaultdict
import re

def filter_errors(lines, threshold=0):
    error_counts = defaultdict(int)

    for entry in lines:
        try:
            if entry['level'] == 'ERROR':
                match = re.search(r'(\w+)', entry['message'])
                if match:
                    error_counts[match.group(1)] += 1

        except (KeyError, TypeError):
            # Skip malformed log entries
            continue
    filtered = {
        error: count
        for error, count in error_counts.items()
        if count > threshold
    }
    return filtered 

    #removed the aggregate functions - gives the same result without.


def main():
    lines = parse_logs("app.log")
    filtered = filter_errors(lines)

    # Sort by count in descending order
    report = dict(sorted(filtered.items(), key=lambda x: x[1], reverse=True))

    print("Error report (highest frequency first):")

    for error, count in report.items():
        print(f"  {error}: {count}")


main()