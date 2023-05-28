#include <pgmspace.h>
 
#define SECRET
#define THINGNAME "ESP32_MAIN"                         //change this
 
const char WIFI_SSID[] = "RealmeX2";               //change this
const char WIFI_PASSWORD[] = "PRAD2003";           //change this
const char AWS_IOT_ENDPOINT[] = "a8kn6lm00vt11-ats.iot.us-east-1.amazonaws.com";       //change this
 
// Amazon Root CA 1
static const char AWS_CERT_CA[] PROGMEM = R"EOF(
-----BEGIN CERTIFICATE-----
MIIDQTCCAimgAwIBAgITBmyfz5m/jAo54vB4ikPmljZbyjANBgkqhkiG9w0BAQsF
ADA5MQswCQYDVQQGEwJVUzEPMA0GA1UEChMGQW1hem9uMRkwFwYDVQQDExBBbWF6
b24gUm9vdCBDQSAxMB4XDTE1MDUyNjAwMDAwMFoXDTM4MDExNzAwMDAwMFowOTEL
MAkGA1UEBhMCVVMxDzANBgNVBAoTBkFtYXpvbjEZMBcGA1UEAxMQQW1hem9uIFJv
b3QgQ0EgMTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALJ4gHHKeNXj
ca9HgFB0fW7Y14h29Jlo91ghYPl0hAEvrAIthtOgQ3pOsqTQNroBvo3bSMgHFzZM
9O6II8c+6zf1tRn4SWiw3te5djgdYZ6k/oI2peVKVuRF4fn9tBb6dNqcmzU5L/qw
IFAGbHrQgLKm+a/sRxmPUDgH3KKHOVj4utWp+UhnMJbulHheb4mjUcAwhmahRWa6
VOujw5H5SNz/0egwLX0tdHA114gk957EWW67c4cX8jJGKLhD+rcdqsq08p8kDi1L
93FcXmn/6pUCyziKrlA4b9v7LWIbxcceVOF34GfID5yHI9Y/QCB/IIDEgEw+OyQm
jgSubJrIqg0CAwEAAaNCMEAwDwYDVR0TAQH/BAUwAwEB/zAOBgNVHQ8BAf8EBAMC
AYYwHQYDVR0OBBYEFIQYzIU07LwMlJQuCFmcx7IQTgoIMA0GCSqGSIb3DQEBCwUA
A4IBAQCY8jdaQZChGsV2USggNiMOruYou6r4lK5IpDB/G/wkjUu0yKGX9rbxenDI
U5PMCCjjmCXPI6T53iHTfIUJrU6adTrCC2qJeHZERxhlbI1Bjjt/msv0tadQ1wUs
N+gDS63pYaACbvXy8MWy7Vu33PqUXHeeE6V/Uq2V8viTO96LXFvKWlJbYK8U90vv
o/ufQJVtMVT8QtPHRh8jrdkPSHCa2XV4cdFyQzR1bldZwgJcJmApzyMZFo6IQ6XU
5MsI+yMRQ+hDKXJioaldXgjUkK642M4UwtBV8ob2xJNDd2ZhwLnoQdeXeGADbkpy
rqXRfboQnoZsG4q5WTP468SQvvG5
-----END CERTIFICATE-----
)EOF";
 
// Device Certificate                                               //change this
static const char AWS_CERT_CRT[] PROGMEM = R"KEY(
-----BEGIN CERTIFICATE-----
MIIDWTCCAkGgAwIBAgIUGpwpq8N21Rzxggtta83SsFA6Nj0wDQYJKoZIhvcNAQEL
BQAwTTFLMEkGA1UECwxCQW1hem9uIFdlYiBTZXJ2aWNlcyBPPUFtYXpvbi5jb20g
SW5jLiBMPVNlYXR0bGUgU1Q9V2FzaGluZ3RvbiBDPVVTMB4XDTIzMDUyNDE5Mjkz
MloXDTQ5MTIzMTIzNTk1OVowHjEcMBoGA1UEAwwTQVdTIElvVCBDZXJ0aWZpY2F0
ZTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAMBLcyCHWOU+ah211/L5
ovePc1GMztc+dInydjy6+2JCL7ajstYAO+Z4BNCU+yVloacrjdErWBfIrlxfPFHH
qrzrXxrxjaOBRev0UBI9tb5GUm5jrXbK738lSLcoPYqCytXigVW3U+7RXofCt0rz
K44n7Tm2DP93uN/jEJLZ6FM39vmKVM364sQpGLtCNgswdDqfhnsjK21ggVr0kuRS
fSeVFOLKe4QbVglMTz/u2zJMJGlYpV1b/T37R6uWik23b6+FcK3S10g0jO/Px4rC
dH2KNwFMxRvrfbbE+Z14euOin9nRGR9iJ8VMbTAoxUdtFOImAA1fyTMhRzN/rNjD
lhcCAwEAAaNgMF4wHwYDVR0jBBgwFoAU5gfwnMcjkiHGfxbV9LWQKdvbAXwwHQYD
VR0OBBYEFFxhVtShemOQx5Xjtsm+4AQmFf3iMAwGA1UdEwEB/wQCMAAwDgYDVR0P
AQH/BAQDAgeAMA0GCSqGSIb3DQEBCwUAA4IBAQCaldFoJSCoQGTz2kkc+wRVCA5e
uur9oen4AOtXiMAYVUFpPJCJBzq9XIVuFwmoiimsoUWmdkq+Y417Pffq0VUSOXb5
uVMdwWjcFAo04OvaA3aFtZsQCFiI+P6I9E6w23zRjtkeB1s7F3DPKRUPb6LQwQO4
BFk9vJlT0/jWuQWyVAf81pYRMLVK23SzIPLBPpCuReqkOKdSRet9qLeg2EdBDYxF
/J6nqQs6ZACdei7NBrFJLyYXR7gT+VZfeO4ZNNv/IKJLXh6A3fCqwO0Kr5AywK81
TzgLudkgWHtGtIYUeS0YVGsWXu6DLyT8/u+3CBYbk9YzSSIWWFNZFJ4qmbmO
-----END CERTIFICATE-----

 
 
)KEY";
 
// Device Private Key                                               //change this
static const char AWS_CERT_PRIVATE[] PROGMEM = R"KEY(
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAwEtzIIdY5T5qHbXX8vmi949zUYzO1z50ifJ2PLr7YkIvtqOy
1gA75ngE0JT7JWWhpyuN0StYF8iuXF88UceqvOtfGvGNo4FF6/RQEj21vkZSbmOt
dsrvfyVItyg9ioLK1eKBVbdT7tFeh8K3SvMrjiftObYM/3e43+MQktnoUzf2+YpU
zfrixCkYu0I2CzB0Op+GeyMrbWCBWvSS5FJ9J5UU4sp7hBtWCUxPP+7bMkwkaVil
XVv9PftHq5aKTbdvr4VwrdLXSDSM78/HisJ0fYo3AUzFG+t9tsT5nXh646Kf2dEZ
H2InxUxtMCjFR20U4iYADV/JMyFHM3+s2MOWFwIDAQABAoIBAHYho89W9qiWaFBq
NwkAjToyeTCfJS6cIrHgLvzuDaL2cCNue132dNYH40VUUNlPjziIjC30x8CMu3jp
1L+UvvIiUqHVxSKuNwtWYp5iJLWIs/k26QiycOEWQY6rfOsLoJo29Sd4YWq0WrNi
ToIP0zEYnCa5DVEf9oYsEzF0BsKf7VD5xkU9g5MwKvm+cNR6ODPY1b2qewuqI3Jn
teWNYqDfIIKPVrdzEzg8Rlk0ZI2FCE6fNVP39hAXY8LXtYeEt2YPOwJpYiVVEAqY
ImHwA1IiRazogCbxjCFKl0+RSMqskkb8oBS0d7tNipg8Bm2VbCHX+QLDVdKsnUM2
hmce6DECgYEA3kGecEP3YlmCQEwFo3u16/Gb4EapZ+FH6G/FHx9tyF8vhPiNMSzg
FnFpZ78LphI6P7jyzaO9YXTV/BGH989unZqyVNRer2YM2UDez3X3xm8Jv5hz9xA1
4AYilhbx4AFl3bhaEQ/iaqbg73eCc0KfUrrqlH4+cnj4cB7H4F9zs18CgYEA3X1S
ItIVGMf4i39B5bRyW3uTr1HlIrBQICED+Ibbo0a0KERT5+ZOPK3bs+hPczKWqP2+
7p1VxygjkrbBmaBIJ0yuHvLDtB2mfPu4HIV5h+x5QdGiT+I6egHNcDwyh873/2kW
fWK8GOloQVlBX/PnXa5EYvbNtToxFMj2yeAgkEkCgYEAqZsxqUJ0mlzsBNz+wI87
eN5bsX668Eb+dOY2a1W0lV/uB28VcB1qtDW/1if4X7cxNEeTIlJ9xs0+LqnCNN3a
7/KJfCrERt19mJzkazT+7DL4IXnZpQR92INWCWthESx/6/8u3C5e/jxzEssEhail
pKB3OvJL/VdLX2Rd619sD8kCgYBdaZVSijfLk8sHSkyIjGoOmzfWITv6PVINut7p
2jaXziH9OZQJoeAtR0X5wmh/tT5FV39HM6QRsqQOJHXSTP8hU/27n7daJ4cn/yHP
JZvz74/Uao2CE2+GNWxngXvuOyPs3G1XxGSAPTBzHymrRjq2D+FXu69WV4yLr5Yl
3hjdwQKBgD7ENoXh00SQkWnmsqU11sQEwj/tV/vzh4zyNun40DapRTXvVOuU/wXK
rKnSQTo+mTdL04gADQNLGIKWX1DkgNUEAohqwC6IwTcbkK2Nc+iU9mU3mcbGvdNW
4P7MShAT0seFpbKdQLz3+hKCtH7RLy1xAAJjptO6CzTHeEzcK8O1
-----END RSA PRIVATE KEY-----

 
 
)KEY";