# from src.app import app


# def codingsphere(request):  
#   if __name__ == "__main__":
#     if app.config['APP_ENVIRONMENT'] == "dev":
#       # from awslambdaric.lambda_handler import handler
#       # handler(app)
#       app.run(host='127.0.0.1', port=8080, debug=True)
#     else:
#       # from awslambdaric.lambda_handler import handler
#       # handler(app)  # pragma: no cover
#       app.run(host='0.0.0.0', port=8080)


from src.app import app  # Import your Flask app from src/app.py
from flask import Request

# Cloud Run requires a function as an entry point
# def codingsphere(request: Request):
#     """
#     Function for Cloud Run to handle requests.
#     It simply forwards requests to the Flask app.
#     """
#     return app(request.environ, start_response_handler)



# Cloud Run requires a function as an entry point
def codingsphere(request: Request):
    """
    Function for Cloud Run to handle requests.
    Routes requests to the Flask app and returns a JSON response.
    """
    with app.test_request_context(
        path=request.path,
        base_url=request.base_url,
        query_string=request.query_string.decode('utf-8') if request.query_string else "",
        method=request.method,
        headers={key: value for key, value in request.headers.items()},  # Copy headers safely
        data=request.get_data()  # Pass request data
    ):
        # Dispatch the request through Flask's request handling
        response = app.full_dispatch_request()

        # Return Flask response directly
        return response.get_data(), response.status_code, dict(response.headers)

def start_response_handler(status, headers, exc_info=None):
    """
    Helper function to handle HTTP responses for WSGI.
    """
    return lambda data: (data, status, headers)

# Run Flask app locally for development
if __name__ == "__main__":
    import os

    # Default to production
    environment = os.getenv("APP_ENVIRONMENT", "prod")

    if environment == "dev":
        app.run(host="127.0.0.1", port=8080, debug=True)
    else:
        app.run(host="0.0.0.0", port=8080)











# from src.app import app  # Import your Flask app from src/app.py
# from flask import Request, jsonify

# # Cloud Run requires a function as an entry point
# def codingsphere(request: Request):
#     """
#     Function for Cloud Run to handle requests.
#     Routes requests to the Flask app and ensures JSON responses.
#     """
#     with app.test_request_context(
#         path=request.path,
#         base_url=request.base_url,
#         query_string=request.query_string,
#         method=request.method,
#         headers=request.headers,
#         data=request.data,
#     ):
#         # Dispatch the request through Flask's request handling
#         response = app.full_dispatch_request()

#         # Ensure JSON response
#         if response.is_json:
#             return response
#         else:
#             return jsonify({"error": "Invalid response format"}), 500

# # Run Flask app locally for development
# if __name__ == "__main__":
#     import os

#     # Default to production
#     environment = os.getenv("APP_ENVIRONMENT", "prod")

#     if environment == "dev":
#         app.run(host="127.0.0.1", port=8080, debug=True)
#     else:
#         app.run(host="0.0.0.0", port=8080)





















# from src.app import app
# import awsgi

# def lambda_handler(event, context):
#     """AWS Lambda handler function."""
#     return awsgi.response(app, event, context)

# if __name__ == "__main__":
#     if app.config.get('APP_ENVIRONMENT') == "dev":
#         app.run(host='127.0.0.1', port=4000, debug=True)
#     else:
#         app.run(host='0.0.0.0', port=4000)




# from src.app import app
# import awsgi

# def lambda_handler(event, context):
#     """AWS Lambda handler function."""
#     print("Spi just got triggerd")
#     return awsgi.response(app, event, context)



# from src.app import app
# from mangum import Mangum

# # Create a handler
# handler = Mangum(app)

# def lambda_handler(event, context):
#     """AWS Lambda handler function."""
#     print("Spi just got triggered")
#     return handler(event, context)


# import serverless_wsgi
# from src.app import app


# def handler(event, context):
#     return serverless_wsgi.handle_request(app, event, context)