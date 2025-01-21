import json
import boto3
import uvicorn
from pydantic import BaseModel
from logs_processor import process_logs
from fastapi import FastAPI,HTTPException


app = FastAPI()

class LogRequest(BaseModel):
    candidate_id: str
    log_content: str

#API endpoint for local call to gunicorn server
@app.post("/processLogs/local")
async def log_processor(request: LogRequest):
    
    log_content:str = request.log_content
    candidate_key:str = request.candidate_id
    processed_result:dict = process_logs(logs=log_content)

    
    return_json = {
        "body":{
            "candidate_id":candidate_key,
            "result":processed_result
        }
    }
    
    return_json["statusCode"] = 200
    
    return return_json

#API endpoint to trigger the lambda function
@app.post("/processLogs/lambda")
async def log_processor(request: LogRequest):
    
    log_content:str = request.log_content
    candidate_key:str = request.candidate_id

    lambda_client = boto3.client("lambda",
                                aws_access_key_id="AWS_SERVER_PUBLIC_KEY",
                                aws_secret_access_key="AWS_SERVER_SECRET_KEY",
                                region_name="REGION_NAME")

    try:
        response = lambda_client.invoke(
            FunctionName='process_logs',
            Qualifier='1',
            Payload=json.dumps({"candidate_id":candidate_key,
                                "log_data":log_content})
        )

        response_payload = json.loads(response['Payload'].read())
    except:
        return HTTPException(status_code=500,detail="Error calling Lambda function")
    
    return_json = {
        "body":{
            "candidate_id":candidate_key,
            "result":response_payload or []
        }
    }
    
    return_json["statusCode"] = 200
    
    return return_json

if __name__ == "__main__":
    uvicorn.run("api_endpoint:app",host="0.0.0.0", port=8000,workers=1)