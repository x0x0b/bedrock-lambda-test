import json
import logging
from typing import Dict, Any

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

default_region = "ap-northeast-1"


def chat_with_bedrock(prompt, region_name=default_region):
  try:
    bedrock = boto3.client(
        service_name='bedrock-runtime',
        region_name=region_name
    )

    logger.info("Chat with Bedrock: %s", prompt)
    body = json.dumps({
      "inputText": f"User: {prompt}\\nBot: "
    })

    response = bedrock.invoke_model(
        modelId="amazon.titan-text-express-v1",
        body=body,
        contentType="application/json",
        accept="application/json",
    )

    # レスポンスの解析
    response_body = json.loads(response.get('body').read())
    return response_body.get('results')[0].get('outputText')

  except Exception as e:
    raise e


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
  try:
    logger.info("Received event: %s", json.dumps(event))

    http_method = (event.get('httpMethod')
                   or event.get('requestContext', {}).get('http', {}).get('method'))

    query_params = event.get('queryStringParameters', {}) or {}

    path_params = event.get('pathParameters', {}) or {}

    response_body = {
      'message': 'Success',
      'method': http_method,
      'queryParams': query_params,
      'pathParams': path_params,
      'response': chat_with_bedrock(query_params.get('prompt', '自己紹介をしてください。'))
    }

    return {
      'statusCode': 200,
      'headers': {
        'Content-Type': 'application/json'
      },
      'body': json.dumps(response_body, ensure_ascii=False)
    }

  except Exception as e:
    logger.error("Error processing request: %s", str(e))
    return {
      'statusCode': 500,
      'headers': {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      'body': json.dumps({
        'message': 'Internal server error',
      }, ensure_ascii=False)
    }
