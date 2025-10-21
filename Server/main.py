from fastapi import FastAPI, HTTPException, Query
from scanner.port_scanner import scan_ports

app = FastAPI(title="Jarvis MK9 - Starter API")

@app.get("/health")
async def health():
    return {"status": "ok", "service": "jarvis-mk9-starter"}

@app.get("/scan")
async def scan(host: str = Query(..., description="Target host, e.g. 127.0.0.1")):
    """Safe scanner: only scans a short list of common ports on a host you own."""
    try:
        result = await scan_ports(host)
        return {"host": host, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
      
