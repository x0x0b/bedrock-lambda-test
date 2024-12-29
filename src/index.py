import json
import logging
from typing import Dict, Any

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
  try:
    logger.info("Received event: %s", json.dumps(event))

    http_method = (event.get('httpMethod')
                   or event.get('requestContext', {}).get('http', {}).get('method'))

    query_params = event.get('queryStringParameters', {}) or {}

    body = {}
    if event.get('body'):
      body = json.loads(event['body']) if event['body'] else {}

    path_params = event.get('pathParameters', {}) or {}

    response_body = {
      'message': 'Success',
      'method': http_method,
      'queryParams': query_params,
      'pathParams': path_params,
      'body': body
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
        'error': str(e)
      }, ensure_ascii=False)
    }
