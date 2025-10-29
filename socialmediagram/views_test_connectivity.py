"""
Vistas para pruebas de seguridad del ConnectionServer.
Estos endpoints están diseñados para probar diferentes escenarios
de seguridad y comportamiento de conexiones.
"""
import time
import json
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt


@require_http_methods(["GET"])
def test_status(request, code):
    """Retorna un código de estado específico para probar manejo de errores."""
    return HttpResponse(
        json.dumps({"status": code, "message": f"Test status code {code}"}),
        status=int(code),
        content_type="application/json"
    )


@require_http_methods(["GET"])
def test_slow(request):
    """Simula una respuesta lenta para probar timeouts."""
    delay = float(request.GET.get("delay", "5"))
    time.sleep(delay)
    return JsonResponse({"ok": True, "delay": delay, "timestamp": time.time()})


@require_http_methods(["GET"])
def test_fast(request):
    """Retorna una respuesta instantánea."""
    return JsonResponse({"ok": True, "timestamp": time.time()})


@require_http_methods(["GET"])
def test_large(request):
    """Genera una respuesta grande para probar límites de tamaño."""
    size = int(request.GET.get("size", "2000000"))
    chunk = "x" * 1024
    
    def generate():
        sent = 0
        while sent < size:
            yield chunk.encode('utf-8')
            sent += len(chunk)
    
    response = StreamingHttpResponse(generate(), content_type="text/plain")
    response['Content-Length'] = size
    return response


@require_http_methods(["GET"])
def test_content_type(request):
    """Retorna un content-type específico para probar validación."""
    ct = request.GET.get("ct", "application/octet-stream")
    return HttpResponse(b"\x00\x01\x02", content_type=ct)


@require_http_methods(["GET"])
def test_chunked(request):
    """Retorna una respuesta en chunks para probar streaming."""
    chunks = int(request.GET.get("chunks", "5"))
    interval = float(request.GET.get("interval", "1"))
    
    def stream():
        for i in range(chunks):
            yield f"chunk-{i}\n".encode('utf-8')
            time.sleep(interval)
    
    return StreamingHttpResponse(stream(), content_type="text/plain")


@require_http_methods(["GET"])
@csrf_exempt
def test_basic_auth(request):
    """Simula autenticación básica."""
    auth = request.META.get('HTTP_AUTHORIZATION', '')
    
    if not auth.startswith('Basic '):
        response = JsonResponse({"error": "Unauthorized"}, status=401)
        response['WWW-Authenticate'] = 'Basic realm="Test"'
        return response
    
    try:
        import base64
        credentials = base64.b64decode(auth[6:]).decode('utf-8')
        username, password = credentials.split(':', 1)
        
        if username == "user" and password == "pass":
            return JsonResponse({"user": username, "authenticated": True})
        else:
            response = JsonResponse({"error": "Invalid credentials"}, status=401)
            response['WWW-Authenticate'] = 'Basic realm="Test"'
            return response
    except Exception:
        response = JsonResponse({"error": "Invalid authorization header"}, status=400)
        return response


@require_http_methods(["GET"])
def test_redirect(request):
    """Redirige a una URL específica."""
    from django.shortcuts import redirect
    to = request.GET.get("to", "https://example.com")
    return redirect(to, permanent=False)


@require_http_methods(["GET", "POST"])
@csrf_exempt
def test_echo(request):
    """Devuelve información sobre la petición recibida."""
    data = {
        "method": request.method,
        "path": request.path,
        "GET": dict(request.GET),
        "headers": {k: v for k, v in request.META.items() if k.startswith('HTTP_')},
    }
    
    if request.method == "POST":
        try:
            data["json"] = json.loads(request.body.decode('utf-8'))
        except Exception:
            data["body"] = request.body.decode('utf-8', errors='ignore')
    
    return JsonResponse(data)


@require_http_methods(["GET"])
def test_json(request):
    """Retorna un JSON válido para pruebas."""
    return JsonResponse({
        "status": "ok",
        "message": "Test endpoint",
        "timestamp": time.time(),
        "data": {
            "items": [1, 2, 3, 4, 5],
            "nested": {"key": "value"}
        }
    })


@require_http_methods(["GET"])
def test_timeout(request):
    """Simula un timeout no respondiendo durante mucho tiempo."""
    delay = float(request.GET.get("delay", "60"))
    time.sleep(delay)
    return JsonResponse({"ok": True, "delayed": delay})
