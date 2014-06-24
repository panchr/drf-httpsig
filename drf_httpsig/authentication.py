from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from httpsig import HeaderSigner
import re

try:
    # Python 3
    from urllib.request import parse_http_list
except ImportError:
    # Python 2
    from urllib2 import parse_http_list


class SignatureAuthentication(authentication.BaseAuthentication):
    algorithm = "hmac-sha256"
    
    request = None
    authorization_header = None
    authorization_fields = {}
    
    def authenticate(self, request):
        # Check if request has a "Signature" request header.
        self.authorization_header = self.request_header(request, 'Authorization')
        if not self.authorization_header:
            return None
            
        if not self.authorization_header.startswith("Signature "):
            return None
        
        self.authorization_header = self.authorization_header[len("Signature "):]
        self.authorization_fields = self.parse_authorization_header(self.authorization_header)
        
        # Fetch the secret associated with the keyid
        user, secret = self.fetch_user_data(self.authorization_fields["keyId"])
        if not (user and secret):
            raise exceptions.AuthenticationFailed('Invalid signature.')
        
        # Sign the message ourselves to compare.
        computed_header = self.build_signature(
            self.authorization_fields['keyId'],
            secret,
            request)
        computed_fields = self.parse_authorization_header(computed_header)
        computed_signature = computed_fields['signature']

        if computed_signature != self.authorization_fields['signature']:
            raise exceptions.AuthenticationFailed('Invalid signature.')
        
        return (user, None)

    def parse_authorization_header(self, auth_header):
        result = {}
        auth_field_list = parse_http_list(auth_header)
        for item in auth_field_list:
            key, value = item.split('=', 1)
            if value[0] == '"' or value[0] == '\'':
                value = value[1:-1]
            result[key] = value
        return result
        
    def fetch_user_data(self, keyId):
        """Retuns a tuple (User, secret) or (None, None)."""
        return (None, None)

    
    def canonical_header(self, header_name):
        """Translate HTTP headers to Django header names."""
        
        header_name = header_name.upper()
        if header_name == 'CONTENT-TYPE' or header_name == 'CONTENT-LENGTH':
            return header_name
        
        # Translate as stated in the docs:
        # https://docs.djangoproject.com/en/1.6/ref/request-response/#django.http.HttpRequest.META
        return "HTTP_" + header_name.replace('-', '_')


    def request_header(self, request, header_name):
        return request.META.get(self.canonical_header(header_name), None)


    def get_headers_from_signature(self, signature):
        """Returns a list of headers fields to sign."""
        headers = []
        authorization = self.parse_authorization_header(signature)
        headers_string = authorization.get('headers')
        
        if headers_string:
            headers.extend(headers_string.split())
        
        return headers


    def build_dict_to_sign(self, request, signature_headers):
        """
        Build a dict with headers and values used in the signature.
        
        "signature_headers" is a list of header names.
        """
        d = {}
        for header in signature_headers:
            header = header.lower()
            if header == '(request-line)':
                continue #Handled by the signer.
            d[header] = self.request_header(request, header)
        return d


    def build_signature(self, keyId, secret, request):
        """Return the signature for the request."""
        
        host = self.request_header(request, "Host")
        method = request.method
        path = request.get_full_path()
        
        headers_field = self.get_headers_from_signature(self.authorization_header)
        
        headers_list = self.build_dict_to_sign(request, headers_field)
        
        signer = HeaderSigner(
            key_id=keyId,
            secret=secret,
            algorithm=self.algorithm,
            headers=headers_field,
            )
        
        print("2")
        signed = signer.sign(headers_list, host=host, method=method, path=path)
        
        print("3")
        return signed['Authorization']
