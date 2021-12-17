class Error:

    def call(message, code):
        error_dict = {
            "code"      :   code,
            "message"   :   message
        }
        return error_dict, code

    def connection_error():
        message = "connection error."
        return Error.call(message, 500)

    def bad_request(req):
        message = f"{req} is either empty, or bad value."
        return Error.call(message, 400)
