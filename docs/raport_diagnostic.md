# Raport Diagnostic: Rezolvare eroare `400 Bad Request` în Chatty Chronos v1

Am analizat eroarea `400 Bad Request` raportată la utilizarea modelului local Qwen cu `llama.cpp` și am identificat două cauze principale, ambele fiind corectate cu succes:

---

## 1. Depășirea limitei de context (`4096` tokeni) în `llama-server`

### Cauză
În fișierul `config.json`, parametrul `"local_server_ctx"` era configurat la limita mică de `4096`. 
Când agentul este rulat:
- **System Prompt**: ~100 tokeni.
- **Tool Schema** (lista celor 8 instrumente filesystem/shell serializate ca JSON): ~2500+ tokeni.
- **RAG Context**: ~1000–1500 tokeni.
- **Istoric conversație** (mesaje anterioare): ~500+ tokeni.

La a doua replică, promptul combinat trimis către model a totalizat **4137 tokeni**, depășind limita fizică de `4096` configurată pentru slotul de rulare. Serverul `llama.cpp` a răspuns cu eroarea specifică:
> `error: request (4137 tokens) exceeds the available context size (4096 tokens), try increasing it`

### Soluție
Am mărit limita implicită și activă de context la **16384 tokeni**. Având în vedere placa grafică Radeon 890M (iGPU) și cei 32 GB RAM, un context de 16k este extrem de sigur, performant și oferă spațiu generos pentru cod de dimensiuni mari.
- Modificat în: [config.py](file:///E:/AI_Sandbox/Chatty-Chronos-v1/core/config.py#L21)
- Modificat în fișierul de configurare al utilizatorului: [config.json](file:///C:/Users/georg/.chatty-chronos/config.json#L16)

---

## 2. Păstrarea permanentă a contextului RAG în istoric

### Cauză
În `main.py`, contextul extras prin RAG (Retrieval-Augmented Generation) era inserat direct în lista globală de mesaje:
```python
messages.insert(-1, {"role": "system", "content": rag_context})
```
Această metodă altera permanent istoricul conversației. Cu fiecare nouă replică, vechile căutări RAG se acumulau în memorie, provocând umflarea rapidă a numărului de tokeni din context și ducând inevitabil la erori de tip `Bad Request`.

### Soluție
Am reimplementat RAG ca fiind **tranzitoriu** (valabil doar pentru tura curentă). Acesta este eliminat automat la finalul fiecărei execuții, fie că aceasta s-a finalizat cu succes sau a eșuat.
- Modificat în: [main.py](file:///E:/AI_Sandbox/Chatty-Chronos-v1/main.py#L559-L642)

---

## 3. Filtrarea eronată a apelurilor de tool-uri din istoric

### Cauză
În implementările `llamacpp_provider.py` și `openai_provider.py`, payload-ul de mesaje era filtrat printr-o listă comprehensivă:
```python
"messages": [{"role": m["role"], "content": m["content"]} for m in messages if m.get("content")]
```
Dacă un mesaj de tip `assistant` (care execută un apel de funcție) avea `"content": ""` sau `None`, acesta era **exclus** complet din payload-ul trimis către LLM, însă mesajul asociat de tip `tool` (cu rezultatul execuției) era păstrat. Serverele compatibile cu OpenAI (inclusiv `llama.cpp`) refuză astfel de structuri invalide (mesaje de tip `tool` fără un apel de tip `assistant` corespunzător în amonte) și răspund cu `400 Bad Request`.

### Soluție
Am rescris serializarea mesajelor pentru ambele endpoint-uri astfel încât să păstreze corect structurile cu `tool_calls` și `tool_call_id`, fără a filtra mesajele doar pe baza cheii `content`.
- Modificat în: [llamacpp_provider.py](file:///E:/AI_Sandbox/Chatty-Chronos-v1/llm/llamacpp_provider.py#L53-L129)
- Modificat în: [openai_provider.py](file:///E:/AI_Sandbox/Chatty-Chronos-v1/llm/openai_provider.py#L29-L37)

---

## 4. Evitarea blocării serverului vechi pe același port (Model Mismatch)

### Cauză
Când utilizatorul închidea fereastra de terminal (folosind butonul `X` al ferestrei CMD/Terminal) fără a folosi `/exit`, procesul de fundal `llama-server.exe` nu era oprit.
La o pornire ulterioară prin starterul bat (de ex. `Start_Chronos.bat`), chiar dacă utilizatorul alegea un model diferit (de exemplu `Qwen 3.5`), scriptul `server_manager.py` verifica doar dacă portul `8069` răspunde. Deoarece serverul vechi (cu modelul `Qwen2.5.1-Coder-7B-Instruct`) era încă activ, scriptul nu mai pornea noul server, rezultând într-o neconcordanță tăcută: agentul folosea un alt model decât cel selectat.

### Soluție
Am implementat o rutină de detecție automată a neconcordanței în [server_manager.py](file:///E:/AI_Sandbox/Chatty-Chronos-v1/llm/server_manager.py#L32-L68):
1. Interoghează endpointul `/v1/models` al serverului care rulează deja pe portul configurat.
2. Compară modelul detectat cu cel configurat.
3. În caz de diferențe, **oprește automat procesul vechi** (`taskkill` pe Windows sau `pkill` pe Unix) și lansează `llama-server` cu noul model selectat în starter.
