# Secret Sharing

Questo progetto simula il  secret sharing con schema (t, n)-threshold, in 
cui un segreto (ad esempio una password) viene condiviso tra `n` entità in modo 
che solo la collaborazione di almeno `t` entità consenta di ricostruire il 
segreto originale.

Il progetto è stato sviluppato nell'ambito dell'esame pratico del corso 
Sicurezza dell'Informazione M del corso di laurea magistrale in Ingegneria 
Informatica dell'Università di Bologna.

## Architettura

Il sistema è composto da due componenti principali:

- **Server (`server.py`)**
  Si occupa di generare a partire dalla password i segreti e di distribuirli 
  ai client.
  Successivamente, cancella dalla propria memoria la password e tenta, 
  ricevendo dai client i segreti, la ricostruzione del segreto originario.

- **Client (`client.py`)**  
  Ogni client riceve un segreto dal server. Può decidere se partecipare alla 
  fase di ricostruzione del segreto inviando (oppure no) la propria porzione 
  al server. La scelta avviene in modo casuale.

## Funzionamento

La simulazione si svolge in due fasi:

1. Il server viene lanciato specificando
    - `n` (numero totale di client)
    - `t` (numero minimo di segreti necessario per ricostruire il segreto)
    - una `password` da condividere

   Tali informazioni vengono usate per distribuire tra i client `n` segreti 
   che potranno essere usati in un secondo momento per ricostruire la password.
   Dopo la distribuzione, la password viene cancellata dalla memoria del 
   server.

2. Ogni client decide se collaborare o meno alla ricostruzione della password.
   - Se collabora, invia il proprio segreto al server.  
   - Se non collabora, invia un messaggio ad-hoc in cui dice di non voler
     collaborare. 
   
   Il server attende di ricevere le porzioni dai client. Se riceve almeno `t` 
   segreti, ricostruisce la password. In caso contrario, la ricostruzine 
   fallisce.

## Eseguire la simulazione
Per eseguire la simulazione è disponibile un apposito script `run.sh`. 
I parametri della simulazione possono essere cambiati all'inizio di tale file.
Da terminale:
```bash
chmod +x run.sh
./run.sh
```
