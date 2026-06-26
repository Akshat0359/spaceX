
import re
from collections import defaultdict


def parse_logs(filepath):
    f = open(filepath, 'r')
    lines = []
    for line in f:
        lines.append(process_line(line))
    f.close() 
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


def filter_errors(lines, threshold=0):
    error_counts = defaultdict(int)

    for entry in lines:
        try:
            if entry['level'] == 'ERROR':
                match = re.search(r'(\w+)', entry['message'])
                if match:
                    error_counts[match.group(1)] += 1
        except Exception:    
            pass

    filtered = {
        error: count
        for error, count in error_counts.items()
        if count > threshold
    }
    return filtered





def main():
    lines = parse_logs("app.log")
    filtered = filter_errors(lines)

    report = filtered

    print("Error report (highest frequency first):") 
    for error, count in report.items():
        print(f"  {error}: {count}")


main()

