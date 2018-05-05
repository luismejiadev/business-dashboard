def get_summary_table():
    expected = 100
    real = 90
    percent = (real-expected)*100.0/expected if expected else 0

    expected2 = 100
    real2 = 100
    percent2 = (real2-expected2)/expected2 if expected2 and real2 != expected2 else 0
    return [
        {
            'id': 'NI',
            'operator': 'Nicaragua',
            'expected': expected,
            'real': real,
            'diff': real-expected,
            'percent': "{0:.0f}%".format(percent)
        },
        {
            'id': 'OHIO',
            'operator': 'Cleveland',
            'expected': expected2,
            'real': real2,
            'diff': real2-expected2,
            'percent': "{0:.0f}%".format(percent2)
        }
    ]
