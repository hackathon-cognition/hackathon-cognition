# Golden Path — Cirurgia de ombro vs. fisioterapia

Roteiro determinístico para a demo do MediCheck.

**Cenário:** paciente recebeu indicação de cirurgia no ombro por lesão do supraespinhal. Quer uma segunda opinião antes de operar. Os especialistas (4 mocks roteirizados + 1 médico humano via dashboard) recomendam tratamento conservador com fisioterapia antes da cirurgia.

---

## Pré-requisitos (1 min)

1. **Rede que não bloqueia o Telegram** (testado em Cisco Umbrella → bloqueia; tether de celular funciona).
2. `.env` configurado com `PATIENT_BOT_TOKEN`.
3. Subir o app:
   ```bash
   .venv/bin/python -m app.main
   ```
   No log você verá:
   - 25 médicos seedados
   - Lista de magic-links (1 por médico)
   - Bloco "🎯 GOLDEN PATH" com o link do primeiro ortopedista (Dr. Gustavo Silva)

---

## Setup do demo (30s antes de começar)

1. **Abre o link do ortopedista no navegador** (qualquer um dos 5 da lista). Esse será o "médico humano" do demo.
   - Acessar o link marca o médico como humano (deixa de receber resposta automática).
   - A página mostra "Casos pendentes (0)" e auto-atualiza a cada 15s.
2. **Abre o bot do paciente no Telegram:** `t.me/medicheck_pacientebot`

---

## Roteiro (3–5 min)

### 1. Cadastro do paciente
No bot do paciente:
```
/start
```
Bot pergunta o nome. Responde com qualquer nome:
```
Guilherme
```

### 2. Descrição do caso
```
/caso meu medico recomendou cirurgia no ombro direito por causa de uma lesao no supraespinhal. tenho dor ha 3 meses e limitacao de movimento, mas queria uma segunda opiniao antes de operar.
```
Bot confirma o rascunho e pergunta se quer anexar exames.

### 3. Anexar exame (PDF)
```
/exame
```
Anexa um ou mais arquivos (PDFs, fotos de raio-X, etc). Bot confirma cada um:
> ✅ Arquivo recebido (1 no total). Mande mais ou /enviar.

### 4. Envio
```
/enviar
```
Bot responde:
> 🚀 Caso enviado para 5 especialistas em **ortopedia**. Aguarde — você será notificado conforme as opiniões chegarem (até 3 horas).

### 5. Médico humano responde (via dashboard)
Em até 15s, o caso aparece no dashboard como "Caso #1". Clica no caso:
- Vê o diagnóstico, sintomas e link do PDF anexado (abre inline).
- Marca **❌ Discordo**.
- Observação:
  > Discordo da indicação cirúrgica imediata. Recomendo iniciar fisioterapia especializada antes de considerar cirurgia.
- Tipo: **Presencial**
- Data: `Próxima quinta às 10h`
- Notas: `Reavaliação após 6 semanas de fisioterapia. Trazer RM e laudos.`
- Clica **Enviar opinião**.

No Telegram o paciente recebe:
> 💬 **Nova opinião de Dr. Gustavo Silva** (ortopedia)
> ❌ **Discorda** do diagnóstico.
> 📝 **Observações:** Discordo da indicação cirúrgica imediata...
> Para responder à proposta de consulta, use /agendar

### 6. Mocks roteirizados respondem
Em 10–30s, os outros **4 ortopedistas mocks** respondem automaticamente, todos defendendo tratamento conservador. Cada resposta gera uma notificação no Telegram. Exemplos do roteiro:

- **Dra. Renata Castro** — *"Discordo da indicação cirúrgica. Tendinopatia do supraespinhal. Recomendo fisioterapia 3x/semana, 12 sessões..."* + propõe consulta presencial.
- **Dr. Bruno Magalhães** — *"Estudos recentes (Beard et al., Lancet 2018) demonstram que 70-80% dos casos respondem ao tratamento conservador..."* + propõe teleconsulta.
- **Dra. Fátima Rocha** — *"Em meus 15 anos de prática, casos semelhantes resolveram com fisioterapia bem orientada..."* + propõe consulta presencial.
- **Dr. Marcelo Duarte** — *"Recomendo fortemente fisioterapia antes de qualquer procedimento cirúrgico..."* (sem proposta de consulta).

### 7. Agendamento
No bot:
```
/agendar
```
Bot lista as propostas pendentes (4 médicos que propuseram consulta) com botões inline:
> 📅 **Propostas de consulta pendentes:**
> • Dr. Gustavo Silva (ortopedia) — presencial — Próxima quinta às 10h
> • Dra. Renata Castro (ortopedia) — presencial — Próxima terça às 15h
> • Dr. Bruno Magalhães (ortopedia) — remoto — Quinta às 9h30
> • Dra. Fátima Rocha (ortopedia) — presencial — Sexta às 14h
>
> [✅ Aceitar com Dr. Gustavo Silva]
> [✅ Aceitar com Dra. Renata Castro]
> [✅ Aceitar com Dr. Bruno Magalhães]
> [✅ Aceitar com Dra. Fátima Rocha]

Clica **✅ Aceitar com Dr. Gustavo Silva**:
> ✅ Agendamento confirmado com Dr. Gustavo Silva!
> Tipo: presencial
> Quando: Próxima quinta às 10h
> Você receberá um lembrete antes do horário.

**Fim do golden path.** ✅

---

## Mensagem central da demo

> "4 de 5 especialistas independentes recomendaram fisioterapia ao invés de cirurgia. O paciente economiza uma cirurgia desnecessária, riscos cirúrgicos, semanas de recuperação e milhares de reais."

---

## Troubleshooting

| Sintoma | Causa provável | Solução |
|---|---|---|
| Bot não responde | Token errado ou rede bloqueia Telegram | Verifica `.env`, testa `curl https://api.telegram.org/bot$TOKEN/getMe` |
| `SSL handshake failure` | Filtro corporativo (Cisco Umbrella, etc) | Tether de celular ou VPN (Cloudflare WARP) |
| Caso não aparece no dashboard | DB foi resetado, token velho | Pega o novo token no log do `app.main` |
| Mocks respondem **na vaga do médico humano** | Médico não acessou o magic-link antes do `/enviar` | Abre o link **antes** do paciente enviar o caso |
| Auto-resposta não usa o roteiro de fisio | Diagnose não tem as palavras "cirurgia" + "ombro" | Use o texto exato do passo 2 |

---

## Reset rápido

Para repetir a demo do zero:
```bash
pkill -f app.main
rm -f data/app.db
rm -rf data/files
.venv/bin/python -m app.main
```
*(Tokens vão mudar — pega os novos do log.)*
