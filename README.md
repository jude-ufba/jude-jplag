# jude-jplag

Serviço HTTP de detecção de plágio com [JPlag](https://github.com/jplag/JPlag), usado pelo [Jude](https://jude.dcc.ufba.br/) (UFBA Online Judge) para comparar submissões de código.

Wrapper Flask mínimo: recebe as submissões, roda o JPlag e devolve os resultados em JSON.

## API

`POST /` (porta 5000)

```json
{
  "extension": "cpp",
  "submissions": [
    { "id": "123", "code": "<código em base64>" },
    { "id": "456", "code": "<código em base64>" }
  ]
}
```

Resposta: `{ "results": [...], "command_output": "...", "errors": [] }` — pares de submissões com os percentuais de similaridade calculados pelo JPlag.

Os arquivos `code1.cpp`/`code2.cpp` são fixtures de teste (duas implementações de fatorial).

## Executando

```bash
docker build -t judeufba/jude-jplag .
docker run --rm -p 5000:5000 judeufba/jude-jplag
```

Imagem publicada: [`judeufba/jude-jplag`](https://hub.docker.com/r/judeufba/jude-jplag) (CI publica `latest` + short-hash a cada push em `main`).

## Licença

O wrapper deste repositório é do projeto Jude. O JPlag (jar baixado durante o build da imagem) é licenciado sob [GPL-3.0](https://github.com/jplag/JPlag/blob/main/LICENSE) — fonte disponível no repositório upstream.

> ⚠️ O serviço não tem autenticação — deve rodar apenas em rede interna (no Jude, a rede do Docker Compose), nunca exposto publicamente.
