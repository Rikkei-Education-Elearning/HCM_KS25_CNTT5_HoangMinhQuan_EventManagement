import json

data = json.load(open('full_results.json', encoding='utf-8'))

output = '''# API Test Checklist

**Project:** FastAPI Backend (HCM_KS25_CNTT5_HoangMinhQuan_EventManagement)

## 1. Test Summary

- **Total test cases:** {total}
- **PASS:** {passed}
- **FAIL:** {failed}
- **BLOCKED:** 0
- **NOT TESTED:** 0

## 2. Detailed Test Results

| # | Module | Endpoint | Test case | Input | Expected result | Actual result | Status |
|---|---|---|---|---|---|---|---|
'''

total = len(data)
passed = sum(1 for d in data if d['result'] == 'PASS')
failed = total - passed

output = output.format(total=total, passed=passed, failed=failed)

for i, row in enumerate(data):
    actual = row['actual'].replace('\n', ' ')
    if len(actual) > 80:
        actual = actual[:77] + '...'
    output += f"| {i+1} | {row['module']} | API Endpoint | {row['case']} | {row['input']} | {row['expected']} | {actual} | **{row['result']}** |\n"

output += '''
## 3. Failed Cases

'''

for row in data:
    if row['result'] == 'FAIL':
        actual = row['actual'].replace('\n', ' ')
        if len(actual) > 200:
            actual = actual[:197] + '...'
        output += f"""
### {row['module']} - {row['case']}
- **Endpoint:** {row['module']} API
- **Test case:** {row['case']}
- **Request:** {row['input']}
- **Expected:** {row['expected']}
- **Actual:** {actual}
- **HTTP status:** {row['status']}
- **Error/bug:** Lỗi logic hoặc crash
"""

with open('docs/api-test-checklist.md', 'w', encoding='utf-8') as f:
    f.write(output)
