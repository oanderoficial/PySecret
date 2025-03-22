# PySecret

## Criptografia utilizada 

<p> O projeto utiliza criptografia simétrica com o algoritmo AES (Advanced Encryption Standard) no modo CBC com HMAC (implementado via Fernet) fornecido pela biblioteca cryptography. </p>

* <strong> Biblioteca:<strong> cryptography

* <strong> Classe utilizada:<strong> Fernet

* <strong> Algoritmo Base:<strong> AES (AES-128 no modo CBC)

* <strong> Validação (HMAC):<strong> SHA-256 (para autenticação e integridade)

* <strong> Tamanho da chave:<strong> 128 bits (gerada a partir de uma senha mestra com PBKDF2HMAC)

* <strong> Derivação de chave:<strong> PBKDF2HMAC com SHA256, sal fixo definido (SALT), e 100000 iterações.

