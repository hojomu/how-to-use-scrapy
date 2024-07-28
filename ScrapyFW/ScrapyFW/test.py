import requests

url = "https://interbattery.or.kr/fairOnline.do"

payload = "{\"SYSTEM_IDX\":122,\"archive\":\"2024\",\"EX_FORM_ID\":\"interbattery_FAIR_01\",\"order_first_input_id\":\"mod5553_in1\",\"order_first_input_val\":\"in3\",\"order_custom_input_id\":\"mod5553_in4\",\"selPageNo\":4}"
headers = {
  'Accept': 'application/json, text/plain, */*',
  'Accept-Encoding': 'gzip, deflate, br, zstd',
  'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
  'Cache-Control': 'no-cache',
  'Connection': 'keep-alive',
  'Content-Length': '190',
  'Content-Type': 'application/json;charset=UTF-8',
  'Cookie': 'JSESSIONID=ACB7A8D1D4087DBABAE58E4DE27C59B3; _ga=GA1.1.58451493.1719274145; _ga_CRYFR3H66C=GS1.1.1719274145.1.1.1719274367.0.0.0',
  'Host': 'interbattery.or.kr',
  'Origin': 'https://interbattery.or.k',
  'Pragma': 'no-cache',
  'Referer': 'https://interbattery.or.kr/fairOnline.do?selAction=single_page&SYSTEM_IDX=122&FAIRMENU_IDX=17933&hl=KOR',
  'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
  'Sec-Ch-Ua-Mobile': '?0',
  'Sec-Ch-Ua-Platform': '"Windows"',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
