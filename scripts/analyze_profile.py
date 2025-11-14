#!/usr/bin/env python3
"""Analyze profile.stats to identify top bottleneck functions."""

import pstats
from pstats import SortKey

# Load profile stats
p = pstats.Stats('profile.stats')

# Get comprehensive data for top bottlenecks
print('=' * 100)
print('DETAILED BOTTLENECK ANALYSIS - TOP 10 BY CUMULATIVE TIME')
print('=' * 100)
print()

stats = p.stats
items = sorted(stats.items(), key=lambda x: x[1][3], reverse=True)[:20]

print(f"{'File:Line (Function)':<70} {'Calls':<10} {'TotTime':<12} {'CumTime':<12} {'Type':<10}")
print('=' * 100)

for func, (cc, nc, tt, ct, callers) in items[:10]:
    filename, line, funcname = func

    # Shorten long paths
    if len(filename) > 50:
        parts = filename.split('\\')
        if len(parts) > 3:
            filename = '...' + '\\'.join(parts[-3:])

    # Categorize as CPU-bound or I/O-bound
    if 'psutil' in filename or 'ppid_map' in funcname:
        category = 'I/O'
    elif 'threading' in filename or 'queue' in filename or '_on_queue' in funcname:
        category = 'I/O'
    elif 'process.py' in filename or 'futures' in filename:
        category = 'I/O'
    elif 'nt.stat' in funcname or 'open_code' in funcname or 'read' in funcname:
        category = 'I/O'
    elif 'compile' in funcname or 'marshal' in funcname or 'exec' in funcname:
        category = 'CPU'
    elif 'extract' in funcname or 'process' in funcname:
        category = 'CPU'
    else:
        category = 'Mixed'

    location = f'{filename}:{line} ({funcname})'
    if len(location) > 70:
        location = location[:67] + '...'

    print(f'{location:<70} {nc:<10} {tt:<12.6f} {ct:<12.6f} {category:<10}')

print()
print('=' * 100)
print('CATEGORIZATION SUMMARY')
print('=' * 100)
print('CPU-bound: Functions performing computation (compilation, execution, parsing)')
print('I/O-bound: Functions waiting for resources (file I/O, process management, threading)')
print('Mixed: Functions with both CPU and I/O characteristics')
