# Acquisizione e riconciliazione dati strutturati per sistema investigativo
Il progetto è predisposto per funzionare con Visual Studio Code (da non confondere con Visual Studio), gratuito e funziona su Windows, MAC e linux.

OS supportati:
* ~~`Windows`~~ la libreria utilizzata da gremlinpython (connettore per JanusGraph) si appoggia a tornado, che a sua volta usa asyncio.  
  Sembra che l'implementazione per Windows di asyncio non sia [completa](https://github.com/tornadoweb/tornado/issues/2751).  
  C'è una [issue](https://github.com/tornadoweb/tornado/issues/2608#issuecomment-550180288) aperta con una possibile soluzione al problema. Occorre verificare.  
  Nel caso si voglia comunque sviluppare con Windows è possibile, ma in questo caso docker e Visual Studio Code sono necessari. L'IDE è in grado di funzionare in modalità client server. La componente server viene installata (automaticamente) all'interno del container Linux (virtualizzato), mentre la parte client è gestita lato Windows.
  Fare riferimento alla [documentazione](https://docs.microsoft.com/en-us/windows/wsl/install-win10) per l'installazione di Docker su Windows (richiede Windows 10, una cpu che supporta le estensioni per la virtualizzazione e una discreta quantità di RAM, il minimo consigliato per tenere tutti i servizi accesi è 8GB).
* `MAC` (non testato, ma è ragionevole pensare che l'implementazione di python sia pressochè identica a quella di linux)
* `Linux` in particolare sviluppato con `Manjaro` e `Ubuntu`.
## Pre-Requisiti
* Docker
* docker-compose
* python 3.7+ (nel caso non si utilizzi VSCode) è consigliata la creazione di un [virtualenv](https://virtualenv.pypa.io/en/latest/). Consigliato l'utilizzo di [pyenv](https://github.com/pyenv/pyenv) con il plugin [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv).

Nel caso lo si utilizzi all'apertura della cartella compare la notifica `Folder contains a Dev Container configuration file. Reopen folder to develop in a container `. Premendo il pulsante `Reopen in Container` avvia automaticamente i servizi riavviando l'editor (molto lento la prima volta).
## Avvio Servizi
> !! Note per l'utilizzo di Docker !!
> Per poter utilizzare docker è necessario avere privilegi di `root` (`sudo`).
> Si può digitare `sudo` davanti a ogni comando o aggiungere l'utente corrente al gruppo docker con il comando `sudo gpasswd -a username docker`. Serve ripetere il login perchè la modifica sia effettiva. In alternativa è possibile usare il comando `newgrp docker` per avviare una nuova shell con il nuovo gruppo (modifica temporanea).

Viene fornito il file `.devcontainer/docker-compose.yaml` che viene utilizzato da VSCode per configurare l'ambiente di sviluppo e i servizi necessari.  
Nel caso non si usi VSCode il file `docker-compose` può comunque essere usato per avviare in maniera rapida i servizi (`JanusGraph`, `ElasticSearch`, ~~`Cassandra`~~ `Scylla`) necessari allo sviluppo. In questo caso conviene commentare la sezione `app` sotto `services` (`services.app`), dato che serve solo per VSCode.  
Perchè il `docker-compose` funzioni correttamente è necessario eseguirlo dalla cartella `.devcontainer`, il primo avvio richiede un attimo di tempo dato che alcuni container devono essere costruiti prima di essere avviati (il container più lungo da assemblare è `app`). 
Dato che i servizi si avviano contemporaneamente può essere necessario avviare manualmente `JanusGraph` nel caso ~~`Cassandra`~~ `Scylla` non abbia terminato l'inizializzazione prima che `JanusGraph` faccia un tentativo di connessione e di conseguenza termini con un errore.  
In caso si abbiano problemi di avvio uno dei servizi può essere utile eliminare i volumi relativi ai servizi (`docker volume rm <nome>`, `docker volume ls` per avere la lista dei volumi).
> !! Note per chi usa windows !!  
> Il container `app` contiene a tutti gli effetti una installazione degli strumenti di sviluppo e quindi anche una versione di linux funzionante

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
* `path`: si applica solo ai file di tipo `xml` e `json`. Permette di specificare il percorse dei dati di interesse all'interno del file.


## Visualizzazione
Sono forniti:
* `start_gremlin_console.sh`: apre una console gremlin nel terminale (richiede docker)
* `graphexp`: servizio avviato da `docker-compose`. Contattabile all'indirizzo http://localhost:8080 (può essere necessario correggere le impostazioni di graphexp dall'interfaccia per puntare a localhost)

## Setup su server
* Clonare il repository.
* Posizionarsi nella cartella `ida/.devcontainer`.
* commentare la sezione `services.app` in `docker-compose.yaml`
* Lanciare il comando `docker-compose up -d`
* Verificare che Janus si avvii correttamente (`docker logs -f jce-janusgraph`).
  Se avviato correttamente nel log l'ultima riga conterrà:
  ```
  13385 [gremlin-server-boss-1] INFO  org.apache.tinkerpop.gremlin.server.GremlinServer  - Channel started at port 8182.
  ```
* Posizionarsi nella root del progetto.
* Avviare console gremlin `./start_gremlin_console.sh`.
  Versioni diverse di docker-compose usano regole diverse per dare il nome alla rete virtuale. Nel caso dia errore correggere il parametro network (per vedere le reti virtuali `docker network ls`).

### Setup pyenv
```
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
cd ~/.pyenv && src/configure && make -C src
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile

# build dependencies python
sudo add-apt-repository universe
sudo apt-get update
sudo apt-get install --no-install-recommends make build-essential libssl-dev \
  zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
  libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev \
  liblzma-dev

# riloggarsi per caricare pyenv

git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bash_profile

# riloggarsi per caricare pyenv-virtualenv

pyenv install 3.8.6
pyenv virtualenv 3.8.6 ida386
pyenv activate ida386
python --version
# l'output deve essere $> Python 3.8.6
cd ida
sudo apt-get install libarchive-dev
pip install -r requirements.txt
```

### Creazione grafo e creazione indici
Per creare il grafo inserire:
```
map = new HashMap<String, Object>()
map.put("storage.backend", "cql")
map.put("storage.hostname", "jce-cassandra")
map.put("index.search.backend", "elasticsearch")
map.put("index.search.hostname", "jce-elastic")
map.put("index.search.elasticsearch.transport-scheme", "http")
map.put("graph.graphname", "tabulati")
ConfiguredGraphFactory.createConfiguration(new MapConfiguration(map))

```
Verificare che il grafo esista con `ConfiguredGraphFactory.getGraphNames()` e aprire il grafo con:
```
graph = ConfiguredGraphFactory.open("tabulati")
g = graph.traversal()
```

La creazione degli indici è la parte più critica. Non vengono creati automaticamente dal programma di mappatura dato che non è possibile verificarne lo stato (esiste la chiamata ma va in timeout anche se gli indici sono stati creati).
Qualsiasi errore durante questo procedimento porta nella maggior parte delle volte alla corruzione dell'intero db (non solo il grafo corrente). Se dopo il procedimento si verificano errori strani conviene cancellare tutti i servizi (`docker-compose down -v`).  
Il procedimento è lungo ma non ho trovato un modo migliore per risolvere il problema della corruzione.  
Può essere utile aumentare il timeout della console gremlin (:remote config timeout 999999999, in millisecondi, non mettere numeri troppo grandi che dà errore).
Nel caso si verificano timeout durante l'esecuzione di un comando non c'è modo di verificarne il completamento. La maggior parte delle volte i comandi (che scrivono) in timeout corrompono il db.

Esempio di creazione indice:
```

g.addV('Persona').property('lbl', 'Persona').property('numero', '123') // serve almeno un nodo con le proprietà da indicizzare
g.tx().commit()

// controllo che il nodo sia stato inserito
g.V().elementMap()
g.tx().rollback() // sto leggendo ma janus può aver avviato una transazione implicita quindi la annullo, in caso è una nop

mgmt = graph.openManagement() // notare che è graph inizializzato con la open

numero = mgmt.getPropertyKey('numero') // indici interni, più performanti per corrispondenze esatte
lbl = mgmt.getPropertyKey('lbl')

mgmt.buildIndex('byLblAndNumber', Vertex.class).addKey(numero).addKey(lbl).buildCompositeIndex()

mgmt.commit()

mgmt = graph.openManagement() // ne apro uno nuovo altrimenti non funziona

// assettare qualche secondo 
mgmt.updateIndex(mgmt.getGraphIndex('byLblAndNumber'), SchemaAction.REINDEX).get() // alcune volte dà errore riprovare qualche secondo dopo, se dà ancora errore creare un'atro graph

mgmt.commit()


// se updateIndex non funziona controllare anche le istanze aperte del management e chiuderle
mgmt = graph.openManagement()
mgmt.getOpenInstances()
==>0934f2eb69223-xxxxxxxxxxxxxx
==>0729845962091-yyyyyyyyyyyyyy(current)
mgmt.forceCloseInstance('0934f2eb69223-xxxxxxxxxxxxxx') 
mgmt.commit()

// ora posso cancellare il nodo superfluo
g.V().drop().iterate()
g.tx().commit() // importante! Se non lo faccio rimane la transazione aperta e se faccio un'importazione sarà rallentata di molto
// committando questa transazione dopo parecchi inserimenti impiega molto, di conseguenza timeout e corruzione



```
Note:
* Committare sempre prima di creare indici `g.tx().commit()` / `g.tx().rollback()`  
  Notare che Janus crea le transazioni implicitamente (anche in lettura). Spesso occorre committare le transazioni, per vedere i nuovi dati dalla console.
  Se rimangono delle transazioni aperte e si aggiungono indici il db si corrompe.
* Non è possibile creare indici sulla `label`. Il software usa la proprietà surrogata `lbl` per poter indicizzare il tipo di nodo
* Aspettare sempre qualche secondo prima di lanciare buildIndex  
* `buildIndex` e `updateIndex` sembra siano sincroni anche se leggendo su internet sembra non lo sia, in ogni caso se i dati sono tanti ci impiega molto prima di terminare. Se va in timeout al 99.99% il db è corrotto
* Aspettare qualche secondo (o più, dipende dalla macchina che si usa) prima di committare, e prima di eseguire `buildIndex` 
* `commit` ha lo stesso difetto di `buildIndex`, aspettare qualche secondo.
* Se ci si dimentica di committare `mgmt` e se apre un'altro il db si corrompe.
* Per creare un indice bisogna creare un nodo con quelle proprietà (committare dopo l'inserimento). L'indice resta anche dopo che il nodo viene eleminato.
* Ci sono due tipi di indici, quelli interni e quelli esterni (Elastic). Quelli interni sono più performanti per ricerche esatte (==), mentre quelli esterni sono più performanti per ricerche full text.

La prova che gli indici vengono usati correttamente la si ha dal log di janus. Il messaggio si commenta da solo.
```
Query requires iterating over all vertices [(lbl = Persona AND numero = 1234567890)]. For better performance, use indexes
```

### importazione dati
Consiglio di usare l'utente andrea per evitare problemi di permessi, anche se in teoria il programma non dovrebbe scrivere nulla (`sudo -iu andrea`).

```
echo extracted_data/f8xx_bt_italia.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_bt_italia.csv
echo extracted_data/f8xx_iliad.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_iliad.csv
echo extracted_data/f8xx_wind_00.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_wind_00.csv
echo extracted_data/f8xx_wind_01.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_wind_01.csv
echo extracted_data/f8xx_wind_02.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_wind_02.csv
echo extracted_data/f8xx_wind_03.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_wind_03.csv
echo extracted_data/f8xx_wind_04.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_wind_04.csv
echo extracted_data/f8xx_wind_05.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_wind_05.csv
echo extracted_data/f8xx_wind_06.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_wind_06.csv
echo extracted_data/f8xx_wind_07.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_wind_07.csv
echo extracted_data/f8xx_wind_08.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_wind_08.csv
echo extracted_data/f8xx_wind_09.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_wind_09.csv
echo extracted_data/f8xx_wind_10.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_wind_10.csv
echo extracted_data/f8xx_wind_11.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_wind_11.csv
echo extracted_data/f8xx_wind_12.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_wind_12.csv
echo extracted_data/f8xx_wind_13.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_wind_13.csv
echo extracted_data/f8xx_wind_14.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_wind_14.csv
echo extracted_data/f8xx_wind_15.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_wind_15.csv
echo extracted_data/f8xx_wind_16.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_wind_16.csv
echo extracted_data/f8xx_wind_17.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_wind_17.csv
echo extracted_data/f8xx_wind_18.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_wind_18.csv
echo extracted_data/f8xx_wind_19.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_wind_19.csv
echo extracted_data/f8xx_wind_20.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_wind_20.csv
echo extracted_data/f8xx_wind_21.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_wind_21.csv
echo extracted_data/f8xx_wind_22.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_wind_22.csv
echo extracted_data/f8xx_wind_23.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_wind_23.csv
echo extracted_data/f8xx_wind_24.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_wind_24.csv
echo extracted_data/f8xx_wind_25.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_wind_25.csv
echo extracted_data/f8xx_wind_26.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_wind_26.csv
echo extracted_data/f8xx_wind_27.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_wind_27.csv
echo extracted_data/f8xx_wind_28.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_wind_28.csv
echo extracted_data/f8xx_wind_29.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_wind_29.csv
echo extracted_data/f8xx_wind_30.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_wind_30.csv
echo extracted_data/f8xx_wind_31.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_wind_31.csv
echo extracted_data/f8xx_wind_32.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_wind_32.csv
echo extracted_data/f8xx_wind_33.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_wind_33.csv
echo extracted_data/f8xx_wind_34.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_wind_34.csv
echo extracted_data/f8xx_wind_35.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_wind_35.csv
echo extracted_data/f8xx_wind_36.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_wind_36.csv
echo extracted_data/f8xx_wind_37.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_wind_37.csv
echo extracted_data/f8xx_wind_38.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_wind_38.csv
echo extracted_data/f8xx_wind_39.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/f8xx_wind_39.csv
echo extracted_data/xxtab_sparkle.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/xxtab_sparkle.csv
echo extracted_data/xxtab_tim.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/xxtab_tim.csv
echo extracted_data/xxtab_voda_00.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/xxtab_voda_00.csv
echo extracted_data/xxtab_voda_01.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/xxtab_voda_01.csv
echo extracted_data/xxtab_voda_02.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/xxtab_voda_02.csv
echo extracted_data/xxtab_voda_03.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/xxtab_voda_03.csv
echo extracted_data/xxtab_voda_04.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/xxtab_voda_04.csv
echo extracted_data/xxtab_voda_05.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/xxtab_voda_05.csv
echo extracted_data/xxtab_voda_06.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/xxtab_voda_06.csv
echo extracted_data/xxtab_voda_07.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/xxtab_voda_07.csv
echo extracted_data/xxtab_voda_08.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/xxtab_voda_08.csv
echo extracted_data/xxtab_voda_09.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/xxtab_voda_09.csv
echo extracted_data/xxtab_voda_10.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/xxtab_voda_10.csv
echo extracted_data/xxtab_voda_11.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/xxtab_voda_11.csv
echo extracted_data/xxtab_voda_12.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/xxtab_voda_12.csv
echo extracted_data/xxtab_voda_13.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/xxtab_voda_13.csv
echo extracted_data/xxtab_voda_14.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/xxtab_voda_14.csv
echo extracted_data/xxtab_voda_15.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/xxtab_voda_15.csv
echo extracted_data/xxtab_voda_16.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/xxtab_voda_16.csv
echo extracted_data/xxtab_voda_17.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/xxtab_voda_17.csv
echo extracted_data/xxtab_voda_18.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/xxtab_voda_18.csv
echo extracted_data/xxtab_voda_19.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/xxtab_voda_19.csv
echo extracted_data/xxtab_voda_20.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/xxtab_voda_20.csv
echo extracted_data/xxtab_voda_21.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/xxtab_voda_21.csv
echo extracted_data/xxtab_voda_22.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/xxtab_voda_22.csv
echo extracted_data/xxtab_voda_23.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/xxtab_voda_23.csv
echo extracted_data/xxtab_voda_24.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/xxtab_voda_24.csv
echo extracted_data/xxtab_voda_25.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/xxtab_voda_25.csv
echo extracted_data/xxtab_voda_26.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/xxtab_voda_26.csv
echo extracted_data/xxtab_voda_27.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/xxtab_voda_27.csv
echo extracted_data/xxtab_voda_28.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/xxtab_voda_28.csv
echo extracted_data/xxtab_voda_29.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/xxtab_voda_29.csv
echo extracted_data/xxtab_voda_30.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/xxtab_voda_30.csv
echo extracted_data/xxtab_voda_31.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/xxtab_voda_31.csv
echo extracted_data/xxtab_wind.csv
python cli.py --gremlin_url='ws://127.0.0.1:8182/gremlin' mapping apply --graph tabulati --mapping mappings/xxtab.yaml --input extracted_data/xxtab_wind.csv
```
Per ogni comando vengono mostrate due barre di progresso. La prima indica il progresso dell'inserimento dei nodi, la seconda gli archi.

### Per cancellare
* Posizionarsi nella cartella `ida/.devcontainer`
* Lanciare il comando `docker-compose down` (`-v` per eliminare anche i volumi)

### Backup e importazione
L'importazione e l'esportazione avvengono da filesistem. Nel caso JanusGraph sia avviato via container sarà necessario copiare i file con il comando docker.

L'esortazione si fa dalla console gremlin:
```
graph.io(IoCore.graphml()).writeGraph("/tmp/tabulati.graphml")
```
La copia in locale del file si fa con il comando:
```
docker cp jce-janusgraph:/tmp/tabulati.graphml . # jce-janusgraph è il nome assegnato al container di JanusGraph
```
La sintassi è simile a quella di scp (copia file con ssh).
> !! Timeout !!  
> Dato che è un'operazione che richiede molto tempo può essere utile aumentare il tempo di timeout  modificando la voce `scriptEvaluationTimeout` nel file `.devcontainer/janus/gremlin-server.yaml`. Il valore utilizzato per i tabulati è `300000`

L'importazione si fa con il comando:
```
graph.io(IoCore.graphml()).readGraph('/tmp/tabulati.graphml')
```
La copia in locale del file nel container si fa con il comando:
```
docker cp tabulati.graphml jce-janusgraph:/tmp/tabulati.graphml
```

In entrambi i casi `graph` fa riferimento all'istanza ottenuta da `ConfiguredGraphFactory.open`