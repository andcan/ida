# Setup
Il progetto è predisposto per funzionare con Visual Studio Code (gratuito funziona su Windows, MAC e Linux), ma può funzionare anche senza.
## Pre-Requisiti
* Docker
* docker-compose
* python 3.7+ (nel caso non si utilizzi VSCode) è consigliata la creazione di un virtualenv
## Avvio Servizi
Viene fornito il file `.devcontainer/docker-compose.yaml` che viene utilizzato da VSCode per configurare l'ambiente di sviluppo e i servizi necessari.  
Nel caso non si usi VSCode il file `docker-compose` può comunque essere usato per avviare in maniera rapida i servizi (`JanusGraph`, `ElasticSearch`, `Cassandra`) necessari allo sviluppo. In questo caso conviene commentare la sezione `app` sotto `services` (`services.app`), dato che serve solo per VSCode.  
Perchè il `docker-compose` funzioni correttamente è necessario eseguirlo all'interno della cartella `.devcontainer`, il primo avvio richiede un attimo di tempo dato che alcuni container devono essere costruiti prima di essere avviati. 
Dato che i servizi si avviano contemporaneamente può essere necessario avviare manualmente `JanusGraph` nel caso `Cassandra` non abbia terminato l'inizializzazione prima che `JanusGraph` faccia un tentativo di connessione e termini dato che non è ancora disponibile.
In caso si abbiano problemi di avvio di qualsiasi servizio può essere utile eliminare i volumi relativi ai servizi (`docker volume rm <nome>`, `docker volume ls` per avere la lista dei volumi).
# Utilizzo
Le funzionalità sono fonite tramite CLI (`cli.py`).  
I parametri con il carattere `*` davanti sono obbligatori.
## Generazione mappatura
```
python cli.py mapping generate
```
Genera un file di mappatura utilizzando i dati contenuti all'iterno del grafo specificato (`--graph`) con i campi contenuti all'interno del file di input (`--input`).
La ricerca di campi corrispondenti viene fatta filtrando tutti i caratteri non alpha numerici (`[a-zA-Z0-9]`) e applicando la Levenshtein distance.  
Parametri:
* *`graph`: nome del grafo all'interno del quale cercare eventuali corrispondenze 
* *`label`: etichetta da associare al nodo
* `map_all(default=false)`: genera una mapatura per tutti i campi all'interno del file di input, ache se non vi è alcuna corrispondenza all'interno del grafo
* *`input`: file contentente i dati da caricare
* `tolerance(default=0.5)`: massima Levenshtein distance permessa per considerare un match con una proprietà all'interno del grafo. `0.5` significa che il match è considerato tale se la Levenshtein distance è al più il `50%` della lunghezza del nome della proprietà. `1` fà in modo che ogni proprietà faccia match con qualsiasi campo. `0` indica una corrispondeza perfetta.
* `query`: query da con la quale filtrare i dati in input. Per maggiori informazioni sul formato delle query visitare [pandas.Dataframe.Query](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.query.html). Es: `Tipo == 1 or Tipo == 2 or Tipo == 6`
* `path`: si applica solo ai file di tipo `xml` e `json`. Permette di specificare il percorse dei dati di interesse all'interno del file. La sintassi del percorso è in formato [JSON Path](https://support.smartbear.com/alertsite/docs/monitors/api/endpoint/jsonpath.html). Internamente l'xml viene convertito in JSON utilizzando [questa](https://github.com/martinblech/xmltodict) specifica. Es: `Risposta.dati.blocchi-impresa.doc-consultabili`

## Applicazione mappatura
* *`input`: file contentente i dati da caricare
* *`mapping`: percorso del file contentente la mappatura
* *`graph`: nome del grafo all'interno del quale applicare la mappatura
* `create(default=false)`: crea il grafo se non esistente
* `query`: query da con la quale filtrare i dati in input.
* si applica solo ai file di tipo `xml` e `json`. Permette di specificare il percorse dei dati di interesse all'interno del file.


## Visualizzazione
Sono forniti:
* `start_gremlin_console.sh`: apre una console gremlin nel terminale (richiede docker)
* `graphexp`: servizio avviato da `docker-compose`. Contattabile all'indirizzo http://localhost:8080