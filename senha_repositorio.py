import json
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

class SenhaRepositorio:
    def __init__(self, arquivo, senha_mestra, salt):
        self.arquivo = arquivo
        self.chave = self._gerar_chave(senha_mestra, salt)
        self.fernet = Fernet(self.chave)

    def _gerar_chave(self, senha, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(senha.encode()))

    def salvar(self, dados):
        dados_json = json.dumps(dados).encode()
        criptografado = self.fernet.encrypt(dados_json)
        with open(self.arquivo, "wb") as f:
            f.write(criptografado)

    def carregar(self):
        if not os.path.exists(self.arquivo):
            return []
        try:
            with open(self.arquivo, "rb") as f:
                dados_criptografados = f.read()
            dados_json = self.fernet.decrypt(dados_criptografados).decode()
            return json.loads(dados_json)
        except:
            return []
