import sys
import warnings
import app.modules.headers as headers

warnings.filterwarnings("ignore")

if len(sys.argv) <= 1:
    print("ERROR: Seleccione la URL destino")
else: 
    url = sys.argv[1]
    result = headers.analyze_headers(url)
    print(result)