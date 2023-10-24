# !CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 pip install --upgrade --force-reinstall llama-cpp-python --no-cache-dir
from llama_cpp import Llama

SYSTEM_PROMPT = """Ты менеджер технической поддержки в чате
"""
SYSTEM_TOKEN = 1788
USER_TOKEN = 1404
BOT_TOKEN = 9225
LINEBREAK_TOKEN = 13

ROLE_TOKENS = {
    "user": USER_TOKEN,
    "bot": BOT_TOKEN,
    "system": SYSTEM_TOKEN
}

model = Llama(
    model_path='/work/projects/uii/saiga_assistant_api/models/model-q2_K.gguf',
    n_ctx=4096,
    n_parts=1,
    # n_gpu_layers=70,
    n_batch=512,
    # n_gqa=8,
)

def get_message_tokens(model, role, content):
    message_tokens = model.tokenize(content.encode("utf-8"))
    message_tokens.insert(1, ROLE_TOKENS[role])
    message_tokens.insert(2, LINEBREAK_TOKEN)
    message_tokens.append(model.token_eos())
    return message_tokens


def get_system_tokens(model):
    system_message = {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
    return get_message_tokens(model, **system_message)


def interact(
    model,
    query,
    tokens,
    top_k=30,
    top_p=0.9,
    temperature=0.2,
    repeat_penalty=1.1
):

    answer = []

    while True:
        user_message = f"User: {query}"
        message_tokens = get_message_tokens(model=model, role="user", content=user_message)
        role_tokens = [model.token_bos(), BOT_TOKEN, LINEBREAK_TOKEN]
        tokens += message_tokens + role_tokens
        generator = model.generate(
            tokens,
            top_k=top_k,
            top_p=top_p,
            temp=temperature,
            repeat_penalty=repeat_penalty
        )
        for token in generator:
            token_str = model.detokenize([token]).decode("utf-8", errors="ignore")
            tokens.append(token)
            answer.append(token_str)
            if token == model.token_eos():
                return ''.join(answer)
                break

            print(token_str, end="", flush=True)
        print()


def main(query):
    # query - "То что должно передать API от пользователя"
    system_tokens = get_system_tokens(model)
    tokens = system_tokens
    model.eval(tokens)
    result = interact(model, query=query, tokens=tokens)

    return result #API должно отдать

if __name__ == '__main__':
    main("Привет")
