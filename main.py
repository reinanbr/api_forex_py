
from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from forex_python.converter import CurrencyRates,CurrencyCodes
from datetime import datetime,timedelta
import uvicorn
import os

c = CurrencyRates()
cc = CurrencyCodes()

app = FastAPI(debug=True,docs_url="/help")
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
currency_to_country = {
    "EUR": {"country": "União Europeia", "currency_name": "Euro", "iso_code": "EU"},
    "JPY": {"country": "Japão", "currency_name": "Iene", "iso_code": "JP"},
    "BGN": {"country": "Bulgária", "currency_name": "Lev", "iso_code": "BG"},
    "CZK": {"country": "República Tcheca", "currency_name": "Coroa Tcheca", "iso_code": "CZ"},
    "DKK": {"country": "Dinamarca", "currency_name": "Coroa Dinamarquesa", "iso_code": "DK"},
    "GBP": {"country": "Reino Unido", "currency_name": "Libra Esterlina", "iso_code": "GB"},
    "HUF": {"country": "Hungria", "currency_name": "Forint", "iso_code": "HU"},
    "PLN": {"country": "Polônia", "currency_name": "Zloty", "iso_code": "PL"},
    "RON": {"country": "Romênia", "currency_name": "Leu", "iso_code": "RO"},
    "SEK": {"country": "Suécia", "currency_name": "Coroa Sueca", "iso_code": "SE"},
    "CHF": {"country": "Suíça", "currency_name": "Franco Suíço", "iso_code": "CH"},
    "ISK": {"country": "Islândia", "currency_name": "Coroa Islandesa", "iso_code": "IS"},
    "NOK": {"country": "Noruega", "currency_name": "Coroa Norueguesa", "iso_code": "NO"},
    "TRY": {"country": "Turquia", "currency_name": "Lira Turca", "iso_code": "TR"},
    "AUD": {"country": "Austrália", "currency_name": "Dólar Australiano", "iso_code": "AU"},
    "BRL": {"country": "Brasil", "currency_name": "Real", "iso_code": "BR"},
    "CAD": {"country": "Canadá", "currency_name": "Dólar Canadense", "iso_code": "CA"},
    "CNY": {"country": "China", "currency_name": "Yuan Chinês", "iso_code": "CN"},
    "HKD": {"country": "Hong Kong", "currency_name": "Dólar de Hong Kong", "iso_code": "HK"},
    "IDR": {"country": "Indonésia", "currency_name": "Rupia Indonésia", "iso_code": "ID"},
    "INR": {"country": "Índia", "currency_name": "Rupia Indiana", "iso_code": "IN"},
    "KRW": {"country": "Coreia do Sul", "currency_name": "Won Sul-Coreano", "iso_code": "KR"},
    "MXN": {"country": "México", "currency_name": "Peso Mexicano", "iso_code": "MX"},
    "MYR": {"country": "Malásia", "currency_name": "Ringgit Malaio", "iso_code": "MY"},
    "NZD": {"country": "Nova Zelândia", "currency_name": "Dólar Neozelandês", "iso_code": "NZ"},
    "PHP": {"country": "Filipinas", "currency_name": "Peso Filipino", "iso_code": "PH"},
    "SGD": {"country": "Cingapura", "currency_name": "Dólar de Cingapura", "iso_code": "SG"},
    "THB": {"country": "Tailândia", "currency_name": "Baht Tailandês", "iso_code": "TH"},
    "ZAR": {"country": "África do Sul", "currency_name": "Rand Sul-Africano", "iso_code": "ZA"},
}


@app.get('/usd')
def usd_page(minutes:int):
    now = datetime.now()
    last_time = now - timedelta(minutes=minutes)
    usd_last = c.get_rates('USD',last_time)
    usd_now = c.get_rates('USD',now)
    
    hours = minutes//60
    days = hours//24
    timedelt = {'seconds':minutes*60,'minutes': minutes,'hours':hours,'days':days}

    usd_now_ = usd_now
    for key in usd_now_:
        
        percent = (usd_now[key] - usd_last[key])/usd_last[key]
        
        status = 'neutral'
        if percent > 0:
            status = 'up'
        elif percent < 0:
            status = 'down'
        
        usd_now[key] = {'currency':usd_now[key]}
        usd_now[key]['symbol'] = f'{cc.get_symbol(key)}'
        usd_now[key]['variation'] = percent
        usd_now[key]['status'] = status
        

        usd_now[key]['timedelta'] = timedelt

        usd_now[key]['info'] = currency_to_country[key]

    return {'dolar':{'now_time':usd_now}}







if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run('main:app', host="0.0.0.0", port=port, reload=True)