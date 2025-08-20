import yaml
import os

def get_api_key(key_name: str) -> str:
    """
    .streamlit/secrets.yamlからAPIキーを読み込む。
    ファイルが存在しない場合やキーが見つからない場合はエラーを発生させる。
    """
    secrets_path = os.path.join(".streamlit", "secrets.yaml")
    if not os.path.exists(secrets_path):
        raise FileNotFoundError(f"Secrets file not found at {secrets_path}. Please create it.")

    with open(secrets_path, 'r') as f:
        secrets = yaml.safe_load(f)

    if key_name not in secrets:
        raise KeyError(f"API key '{key_name}' not found in {secrets_path}.")

    return secrets[key_name]
