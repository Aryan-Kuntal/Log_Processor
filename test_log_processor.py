from logs_processor import process_logs

def test_process_logs():
    test_case1 = """[2024-01-07 10:15:30] ERROR: Database connection failed
    [2024-01-07 10:15:35] INFO: Retry attempt 1 
    [2024-01-07 10:15:40] ERROR: Authentication failed"""

    assert process_logs(logs=test_case1) == {"total_errors":2,"unique_error_messages":["Authentication failed","Database connection failed"]}

    test_case2 = """[2024-01-07 10:15:30] ERROR: Memory overflow
    [2024-01-07 10:15:35] ERROR: Memory overflow"""

    assert process_logs(logs=test_case2) == {"total_errors":2,"unique_error_messages":["Memory overflow"]}

    test_case3 = ""

    assert process_logs(logs=test_case3) == {"total_errors":0,"unique_error_messages":[]}