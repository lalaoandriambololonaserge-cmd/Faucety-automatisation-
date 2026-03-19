import requests
import os
import time

FAUCETPAY_EMAIL = os.getenv("FAUCETPAY_EMAIL")
CAPTCHA_API_KEY = os.getenv("CAPTCHA_API_KEY")

COINS = [
    "BTC","ETH","USDT","BNB","SOL","USDC","XRP","DOGE","TRX","TON",
    "BCH","ADA","LTC","POL","XMR","XLM","ZEC","DASH","DGB","FEY"
]

def solve_captcha(site_key, url):
    captcha_id = requests.post("http://2captcha.com/in.php", {
        "key": CAPTCHA_API_KEY,
        "method": "userrecaptcha",
        "googlekey": site_key,
        "pageurl": url
    }).text.split('|')[1]

    while True:
        res = requests.get(f"http://2captcha.com/res.php?key={CAPTCHA_API_KEY}&action=get&id={captcha_id}")
        if res.text == "CAPCHA_NOT_READY":
            time.sleep(5)
            continue
        return res.text.split('|')[1]

def claim_coin(coin):
    url = f"https://beefaucet.com/claim/{coin}?address={FAUCETPAY_EMAIL}"
    site_key = "SITE_KEY_DU_CAPTCHA"  # à remplacer par la clé reCAPTCHA du site
    token = solve_captcha(site_key, url)

    payload = {
        "address": FAUCETPAY_EMAIL,
        "g-recaptcha-response": token
    }

    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print(f"[OK] Claim {coin} envoyé vers FaucetPay ({FAUCETPAY_EMAIL})")
        else:
            print(f"[ERREUR] Claim {coin} : {response.status_code}")
    except Exception as e:
        print(f"[EXCEPTION] {coin} : {e}")

if __name__ == "__main__":
    for coin in COINS:
        claim_coin(coin)
