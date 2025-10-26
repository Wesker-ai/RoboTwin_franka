from openai import OpenAI

kimi_api = "sk-3QqNXuGPaFRPWVF9tuIdUap26xGoEuS1OjXnSDXGvWw6iF0u"
openai_api = "Your key"
deep_seek_api = "sk-38d78003746447d4ba94daa2274fde2a"

# Configure the API and key (using DeepSeek as an example)
def generate(message, gpt="deepseek", temperature=0):

    if gpt == "deepseek":
        MODEL = "deepseek-chat"
        OPENAI_API_BASE = "https://api.deepseek.com"
        # Set your API key here
        OPENAI_API_KEY = deep_seek_api
        client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)

    elif gpt == "Kimi":
        MODEL = "moonshot-v1-128k"
        OPENAI_API_BASE = "https://api.moonshot.cn/v1"
        OPENAI_API_KEY = kimi_api
        client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)

    elif gpt == "openai":
        MODEL = "gpt-4o"
        OPENAI_API_BASE = "https://api.gptapi.us/v1"
        OPENAI_API_KEY = openai_api
        client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)

    else:
        raise ValueError(f"Unsupported API provider: {gpt}")

    print('start generating')
    response = client.chat.completions.create(
        model=MODEL,
        messages=message,
        stream=False,
        temperature=temperature,
    )
    print('end generating')

    return response.choices[0].message.content


