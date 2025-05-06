# Regex → DFA Converter
## Descrierea proiectului  
Acest proiect primește expresii regulate (regex), le transformă în automate finite deterministe (DFA) și apoi le simulează pe un set de string-uri de test, afișând pentru fiecare dacă este acceptat sau nu de DFA-ul generat. Conversia se face în două etape:
1. **Thompson’s construction**  
   - Se construiește un NFA din regexul postfixat.  
2. **Subset construction**  
   - Se transformă NFA-ul într-un echivalent DFA (ε‐închidere + move).

---

## Structura fișierelor
### 1. **main.py**  
   - Punctul de intrare: încarcă un fișier JSON cu cazuri de test, pentru fiecare regex construiește un DFA şi rulează testele, apoi afișează rezultate sub forma  
     ```  
     ✔ input='…' expected=True got=True  
     ✘ input='…' expected=False got=True  
     ```
### 2. parser.py  
Pregătește expresia regulată pentru conversia în postfix:

- `concatenation(regex)`:  
  - Parcurge caracter cu caracter și inserează explicit operatorul `.` acolo unde două componente (literal sau ) se succed în mod implicit.
  - Exemplu: `ab|c*` → `a.b|c*`
- `parse(regex)`:  
  1. Apel `concatenation` → șir cu puncte.  
  2. Apel `shunting_yard` → returnează șirul postfixat, gata de trimis la etapa Thompson.

### 3. shunting_yard.py  
Algoritmul Shunting-Yard pentru regex-uri, echivalent cu cel al expresiilor aritmetice infix→postfix:

- Definirea precedențelor:  
  - `|` (0) < `.` (1) < `*`, `+`, `?` (2)
- Stive:  
  - `st` pentru operatori,  
  - `final` pentru output (lista postfixată).
- Regulile de bază:  
  1. Dacă caracterul e literă/cifră → pune direct în `final`.  
  2. Dacă e `(` → împinge în `st`.  
  3. Dacă e `)` → pop până la `(`.  
  4. Dacă e operator → pop din `st` toți operatorii cu precedență >= precedenței curente, apoi pune operatorul curent.  
  5. La sfârșit, golește stiva în `final`.  

### 4. nfa_construct.py  
Implementarea construcției lui Thompson pentru a genera un NFA din regex-ul postfixat:

- Clase:
  - `State`: menține un dicționar `transitions` (cheie simbol, valoare lista de destinații) și o listă `lambda` de tranziții λ.
  - `NFA`: simplu container cu doi poli—`start` și `accept`.
- Funcția `thompson_construction(postfix)`:
  - Folosește o stivă de obiecte `NFA`.  
  - Pentru fiecare caracter din postfix:
    - **literă/cifră**: creează NFA cu o singură tranziție etichetată.  
    - **`.`** (concatenare): lipește NFA-urile din topul stivei în serie (λ-legătură între accept-ul primului și start-ul celui de-al doilea).  
    - **`|`** (uniune): creează un nou start și un nou accept, cu λ-tranziții către cele două sub-NFA-uri și de la ambele accept-uri către noul accept.  
    - **`*`, `+`, `?`**: respectă schema clasică—în veloare în Bucla Kleene (`*`), plus-one (`+`) sau opțional (`?`) cu noduri adiționale și ε.  
  - La final există exact un NFA pe stivă, returnat ca rezultat.

### 5. nfa_to_dfa.py  
Transformarea unui NFA cu λ-tranziții într-un DFA (algorithmul subset-construction):

- `lambda_closure(states)`:  
  - Pornind de la un set de stări NFA, adaugă recursiv toate stările accesibile prin tranziții λ.  
- `move(states, symbol)`:  
  - Pentru un set de stări și un simbol, colectează toate stările vizate de tranziții etichetate cu acel simbol.  
- `nfa_to_dfa(nfa)`:  
  1. Calculează λ-închiderea inițială a stării `start` → setul inițial de stări DFA.  
  2. Menține o coadă („unmarked”) de seturi de stări NFA („stări DFA neprocesate”).  
  3. La fiecare pas extrage un set, pentru fiecare simbol din alfabetul NFA:
     - Aplică `move` apoi `lambda_closure` → obține un nou subset.  
     - Dacă subset-ul e nou, îi dă un nou ID și îl pune în coadă.  
     - Înregistrează tranziția DFA `(ID curent, simbol) → ID nou`.  
  4. După ce nu mai sunt stări neprocesate, marchează ca stări finale toate ID-urile care conțin starea `accept` a NFA-ului.  
  5. Returnează structura `{ start: 0, transitions: {...}, accepting: {...} }`.


### 6. dfa.py  
Utilitar pentru simularea (și, parțial, citirea/validarea) unui DFA:

- `simulate_dfa(dfa, input_string)`:  
  - Pornește în `dfa["start"]` și traversează `dfa["transitions"]` caracter cu caracter.  
  - Dacă nu există o tranziție pentru `(stare curentă, simbol)`, întoarce `False`.  
  - La sfârșit, verifică dacă starea curentă este în setul `dfa["accepting"]`.  
- (Optional) există și funcții de citire dintr-un fișier text și validare, dar în pipeline-ul principal e folosită numai `simulate_dfa`.


7. **LFA-Assignment2_Regex_DFA_v2.json**  
   - Fișierul de configurare / test: o listă de obiecte fiecare având  
     ```json
     {
       "name": "nume_test",
       "regex": "expresie_regulata",
       "test_strings": [
         { "input": "…", "expected": true },
         …
       ]
     }
     ```

---
## Cum se folosește  
1. Clonează acest repository.  
2. Pune testele tale în `LFA-Assignment2_Regex_DFA_v2.json` (sau alt fișier) respectând structura JSON.  
3. Rulează:

   ```bash
   python main.py
   ```

4. Vei vedea, pentru fiecare caz de test, marcajul ✔ sau ✘, input-ul testat, valoarea așteptată și cea obținută.
