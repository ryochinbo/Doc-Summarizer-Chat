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

def get_gemini_model_config() -> dict:
    """
    .streamlit/config.yamlからGeminiモデルの設定を読み込む。
    ファイルが存在しない場合や設定が見つからない場合はエラーを発生させる。
    """
    config_path = os.path.join(".streamlit", "config.yaml")
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at {config_path}. Please create it.")

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    if "gemini_models" not in config:
        raise KeyError(f"'gemini_models' section not found in {config_path}.")

    return config["gemini_models"]