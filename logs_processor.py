import re

def process_logs(logs: str) -> dict:

    error_pattern: re.Pattern = re.compile(r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] ERROR\s*:\s*(.+)")

    error_logs = [sanitize.strip() for sanitize in error_pattern.findall(logs)]

    unique_errors = set(error_logs)
    
    return {
        "total_errors":len(error_logs),
        "unique_error_messages":list(sorted(unique_errors))
    }

def lambda_handler(event:dict, context) -> dict:

    log_data:str = event.get("log_data", "")
    candidate_id:str = event.get("candidate_id", "")

    processed_logs:dict = process_logs(logs=log_data)

    return_json = {
        "body":{
            "candidate_id":candidate_id,
            "result":processed_logs
        }
    }

    return return_json

