import datetime
from borica import Response, Verifier


CERTIFICATE = """-----BEGIN CERTIFICATE-----
MIID0DCCAzmgAwIBAgIFAIETPncwDQYJKoZIhvcNAQELBQAwgY0xCzAJBgNVBAYT
AkJHMQ4wDAYDVQQIEwVTb2ZpYTEOMAwGA1UEBxMFU29maWExHjAcBgNVBAoTFUJP
UklDQS1CQU5LU0VSVklDRSBBRDEdMBsGA1UECxMUSW5mb3JtYXRpb24gU2VjdXJp
dHkxHzAdBgNVBAMTFjNEIFNlY3VyZSBDQSBURVNUIDIwMTYwHhcNMTYwNTExMDAw
MDAwWhcNMTgwNTEwMjM1OTU5WjCBjzEeMBwGA1UEChMVQk9SSUNBLUJBTktTRVJW
SUNFIEFEMR0wGwYDVQQLExRJbmZvcm1hdGlvbiBTZWN1cml0eTEOMAwGA1UEBxMF
U29maWExDjAMBgNVBAgTBVNvZmlhMQswCQYDVQQGEwJCRzEhMB8GA1UEAxMYM0RT
IFBheW1lbnQgR2F0ZXdheSBURVNUMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKB
gQDWNB8yH8j2Uy1KvOkpemM3wcrNNPMsZCTnUr+keNzkTQxzT6hdUDiNFT6byYab
W5/lAbQoJ25Xnx4AAdkI4+ZzqtOUF53Fzrs3zsV63fLvvqOyiyq80cc7to8WmnPn
duruEVcB2VEl66KjN5D0k79YrITyYJNhmarpFJU7Ji/VmQIDAQABo4IBNjCCATIw
DAYDVR0TAQH/BAIwADAdBgNVHQ4EFgQU3QowJy8yIKf9f3KhSJ+pSomBPOUwgZgG
A1UdIwSBkDCBjYAUX57guTHQsm0J7+Hy+WX1B4n+imahbqRsMGoxCzAJBgNVBAYT
AkJHMQ4wDAYDVQQHEwVTb2ZpYTEUMBIGA1UEChMLQk9SSUNBIEx0ZC4xHDAaBgNV
BAsTE1NlY3VyaXR5IERlcGFydG1lbnQxFzAVBgNVBAMTDkJPUklDQSBSb290IENB
ggUAgRM+dTALBgNVHQ8EBAMCA/gwOwYDVR0lBDQwMgYIKwYBBQUHAwEGCCsGAQUF
BwMCBggrBgEFBQcDAwYIKwYBBQUHAwQGCCsGAQUFBwMIMB4GCWCGSAGG+EIBDQQR
Fg94Y2EgY2VydGlmaWNhdGUwDQYJKoZIhvcNAQELBQADgYEAHRjQG/lRQ9I5cnqm
BmZyAwUge/HSE0Ar9JSVX6Wdzw2fBzXv6sIiL9m59OzKKrRyCrdWjR1fJBHuwSJI
HJek6DV8CB27RwqGlkGoN8CSHy8IyajkOaTHHSCRCfRWEG/IdHA3YpLFgtSnzbQz
j5iEh6dkpRC1GhMKO02dbEr6xtU=
-----END CERTIFICATE-----"""


def test_response():
    RESPONSE = "MTAyMDE3MDYzMDEyMzU0MDAwMDAwMDAwMDAwOTYyMTYxMDcyMTIzNDUxMjM0NTEyMzQxOTQxLjG/Iuty7qXxa2DyhTXi0Rq8J/odRU6QOqI1p7GHrcJPCNNgEqWop7hbwPIg8ebBgX0BhpE+                 myBoxMDWWJS7ecY4K+FumdXGkpwOCRfe2GGwX/qLvZ3LZWGwFLffe0A62JBWmc6Lvacq5deAkkZ8Kx3QMdTk8tzgjdOpfFmSswGjNA=="  # noqa
    verifier = Verifier(CERTIFICATE)
    response = Response(RESPONSE)
    assert response.verify(verifier) is True
    assert response.transaction_code == 10
    assert response.transaction_time == datetime.datetime(
        year=2017, month=6, day=30, hour=12, minute=35, second=40)
    assert response.amount == 0.09
    assert response.terminal_id == 62161072
    assert response.order_id == "123451234512341"
    assert response.status_code == 94
    assert response.protocol_version == "1.1"


def test_bad_signature_response():
    RESPONSE = "MTAyMDE3MDYzMDEyMzU0MDAwMDAwMDAwMDAwOTYyMTYxMDcyMTIzNDUxMjM0NTEyMzQxOTQxLjG/Iuty7qXxa2DyhTXi0Rq8J/odRU6QOqI1p7GHrcJPCNNgEqWop7hbwPIg8ebBgX0BhpE+                 myBoxMDWWJS7ecY4K+FumdXGkpwOCRfe2GGwX/qLvZ3LZWGwFLffe0A62JBWmc6Lvacq5deAkkZ8Kx3QMdT=="  # noqa
    verifier = Verifier(CERTIFICATE)
    response = Response(RESPONSE)
    assert response.verify(verifier) is False


def test_bad_base64_response():
    RESPONSE = "MTAyMDE3MDYzMDEyMzU0MDAwMDAwMDA"  # noqa
    verifier = Verifier(CERTIFICATE)
    response = Response(RESPONSE)
    assert response.verify(verifier) is False
