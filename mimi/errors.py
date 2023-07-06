from flask.app import HTTPException


class InvaildNodeId(HTTPException):
    code = 400
    description = 'Invalid node id'

class NoKeyFile(HTTPException):
    code = 400
    description = 'No key file'

class PublicKeyNotFound(HTTPException):
    code = 404
    description = 'Public key not found'

class SecretNotFound(HTTPException):
    code = 404
    description = 'Secret not found'

class SecretAlreadyUsed(HTTPException):
    code = 400
    description = 'Secret already used'
