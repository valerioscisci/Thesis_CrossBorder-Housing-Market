// Creo la mia mappa posizionandola sul nord italia
var map = L.map("map").setView([45.8, 9.9], 6);

// Controll fullscreen
map.addControl(new L.Control.Fullscreen());

// Variabili che conterranno i layer della mappa con i confini e le aree cliccabili
var geojsonLayer, borderLayer, flussiLayer;

// Variavile che conterrà i dati delle province che piloteranno poi il colore delle regioni e i dati visualizzati
var dataProvince;

// Varibaile che contiene i dati della zona selezionata dall'utente
var dataSelected;

// Inizialmente si parte a livello affitto ma poi l'utente potrà cambiare questa cosa
var affitto_vendita = "A";

// Inizialmente si parte a livello provincia ma poi l'utente potrà cambiare questa cosa
var livelloSelezionato = "provincia";

// Timeout che mi serve per lo zoom della mappa quando si clicca qualcosa
var timeout = 500;

// GESTIONE FORM

// Funzione che mi resetta la mappa allo stato iniziale
function formMapReload(event) {
  event.preventDefault();

  // Se il layer é già presente viene prima eliminato
  if (geojsonLayer) {
    geojsonLayer.remove();
  }

  if (
    document.getElementById("affitto_vendita")
      .checked
  ) {
    affitto_vendita = "A";
  } else {
    affitto_vendita = "V";
  }

  // Chiede e visualizza nuovamente i dati
  jsonRequest(
    "http://localhost:8000/api/prezzi_medi",
    visualizeData,
    livelloSelezionato
  );

  setTimeout(function () {
    map.invalidateSize();
    map.setView([45.8, 9.9], 6);
  }, timeout);

  // Aggiorna il box in alto a destra
  info.update();
}

// Gestione dell'aggiornamento della mappa
document
  .getElementById("form-submit")
  .addEventListener("click", function (event) {
    formMapReload(event);
  });

// Gestione del reset della mappa
document
  .getElementById("map-reset")
  .addEventListener("click", function (event) {
    timeout = 500;

    formMapReload(event);
  });

// Funzione asincrona che mi recupera i dati sottoforma di json dall'url passato e che lancia la funzione passata
// come secondo parametro al termine dell'operazione di recupero
function jsonRequest(url, callback, livello) {
  let xhr = new XMLHttpRequest();
  xhr.open(
    "GET",
    url + "?livello=" + livello,
    true
  );
  xhr.responseType = "json";
  xhr.onload = function () {
    let status = xhr.status;
    if (status === 200) {
      callback(null, xhr.response);
    } else {
      callback(status, xhr.response);
    }
  };
  xhr.send();
}

// Aggiunge alla mappa un layer che mi mostra un logo di copyright e un link a OpenMaps
L.tileLayer(
  "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
  {
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  }
).addTo(map);

// Funzione che prende una dato e cerca tra i dati json che sono stati recuperati se ci sono delle informazioni
// sui prezzi. Con queste info determina il colore in una scala da 0 a 100 dove 0 è verde(economico) e 100
// è rosso(costoso)
function getColor(d) {
  // Prende solo i dati d'interesse in base a ciò che gli viene passato come parametro e al valore della variabile affitto_vendita
  const datiProvinciaFiltrati = dataProvince.filter(
    (datiProvincia) =>
      datiProvincia.provincia.trim() ===
        d.trim() &&
      datiProvincia.affitto_vendita ===
        affitto_vendita
  );

  // Per i valori filtrati mi calcolo il totale così poi posso riportare i valori in centesimi
  let totale = datiProvinciaFiltrati.reduce(
    function (prev, cur) {
      return prev + cur.num_annunci;
    },
    0
  );

  // Variabile che mi serve per definire il peso da dare al numero di annunci in ciascuna categoria
  let priceMapping = { B: 0, M: 100, A: 100 };

  // Mi torna il valore di colore da attribuire a questa regione in base al numero di annunci in ciascuna fascia di prezzo
  let totale100 = datiProvinciaFiltrati.reduce(
    function (prev, cur) {
      const Totale100 =
        (priceMapping[cur.fascia_prezzo] *
          cur.num_annunci) /
        totale;
      cur.PrezzoPercentuale =
        cur.num_annunci * cur.prezzo_medio;
      return prev + Totale100;
    },
    0
  );

  // Mi calcola il valore della tinta da assegnare ammesso che ho de idati per quella regione
  if (totale != 0) {
    let hue = (
      (1 - totale100 / 100) *
      100
    ).toString(10);
    return [
      ["hsl(", hue, ",80%,60%)"].join(""),
      datiProvinciaFiltrati,
    ];
  } else {
    return ["#666666", datiProvinciaFiltrati];
  }
  // Ritorna il colore
}

// Funzione che per ciascuna zona ritorna lo stile da assegnargli. Lancia inotlre la funzione getColor per capire che
// colore usare per il riempimento.
function style(feature) {
  // Aggiunge il colore
  const [color, datiFiltrati] = getColor(
    feature.properties.Name
  );

  // Aggiunge lo stato
  datiFiltrati.length === 0
    ? (feature.properties.Stato =
        "Non disponibile")
    : (feature.properties.Stato =
        datiFiltrati[0].stato);

  // Aggiunge i dati delle provincie
  feature.properties.datiFiltrati = datiFiltrati;

  return {
    fillColor: color,
    weight: 3,
    opacity: 1,
    color: "white",
    dashArray: "3",
    fillOpacity: 0.7,
  };
}

// Funzione che mi evidenzia l'area su cui l'utente passa il mouse
function highlightFeature(e) {
  const regioneSelezionata = e.target;
  info.update(
    regioneSelezionata.feature.properties
  );

  let layer = e.target;

  layer.setStyle({
    weight: 5,
    color: "#666",
    dashArray: "",
    fillOpacity: 0.7,
  });

  if (
    !L.Browser.ie &&
    !L.Browser.opera &&
    !L.Browser.edge
  ) {
    layer.bringToFront();
  }
}

// Quando l'utente sposta il mouse fuori dall'area resetta lo stile e i confini
function resetHighlight(e) {
  geojsonLayer.resetStyle(e.target);
  info.update();
  borderLayer.bringToFront();
  flussiLayer.bringToFront();
}

// Zoomma quando l'utente clicca
function zoomToFeature(e) {
  map.invalidateSize();
  map.fitBounds(e.target.getBounds());
}

function onEachFeature(feature, layer) {
  layer.on({
    mouseover: highlightFeature,
    mouseout: resetHighlight,
    click: zoomToFeature,
  });
}

// Funzione che prende dei dati in formato json che gli sono stati passati, carica i dati dei confini dal file geojson
// e poi sfruttando le funzioni sopra mi costruisco lo stile del layer e lo aggiunge alla mappa
function visualizeData(status, dataResponse) {
  if (status === null) {
    dataProvince = dataResponse;
    geojsonLayer = new L.GeoJSON.AJAX(
      "/static/MapCB/geojson/province_confine.geojson",
      {
        style: style,
        onEachFeature: onEachFeature,
      }
    );
    geojsonLayer.addTo(map);

    // Crea e aggiunge i dati dei confini
    borderLayer = new L.GeoJSON.AJAX(
      "/static/MapCB/geojson/confini.geojson",
      {
        style: {
          weight: 4,
          color: "#1D90E2",
          dashArray: "",
          fillOpacity: 1,
        },
      }
    );

    borderLayer.addTo(map);
    borderLayer.bringToFront();

    // Sezione dedicata al calcolo delle frecce dei flussi di persone

    // Recupera i dati
    jsonRequest(
      "http://localhost:8000/api/flussi",
      (status, dataResponse) => {
        if (status === null) {
          // In dataResponse ci sono i vicini di ogni zona ed i dati sulle coordinate

          // Questa funzione mi permette di prendere i prezzi medi di tutte le zone e di costruire un oggetto che
          // mi mantenga queste informazioni per usarle poi per capire se una freccia avrà un verso o l'altro
          let prezziMediZone = [];
          dataResponse.map((zona) => {
            let zone = [];
            // Zone lo valorizzo con il primo elemento che è da dove parte la freccia e con i vicini
            zone.push(zona.zona);
            zona.vicini.forEach((vicino) => {
              zone.push(vicino.zona);
            });
            let datiZone = [];
            let provincia = [];

            // Per ogni zona divido i dati sui prezzi contenuti in dataProvince che sono divisi per fasce (Alto, Medio, Basso)
            // e che sono riferiti sia ad affitto che vendita, quindi prendo solo ciò che mi interessa
            zone.forEach((vicino, index) => {
              let datiProvincia = dataProvince.filter(
                (dato) =>
                  dato.affitto_vendita ===
                    affitto_vendita &&
                  dato.provincia.trim() ===
                    vicino.trim()
              );

              if (datiProvincia.length === 0) {
                provincia[index] = vicino;
              } else {
                provincia[index] =
                  datiProvincia[0].provincia;
              }
              datiZone.push(datiProvincia);
            });

            // Adesso aggrego i dati, calcolo i prezzi medi e li aggiungo all'array che conterrà la lista di oggetti {zona: X, prezzoMedio: Y}
            datiZone.forEach(
              (datiZona, index) => {
                let numAnnunci = 0;

                valoriMediZona = (
                  datiZona.reduce((prev, cur) => {
                    numAnnunci += cur.num_annunci;
                    return (prev +=
                      cur.PrezzoPercentuale);
                  }, 0) / numAnnunci
                ).toFixed(2);

                // Prendo il nome della provincia che sto analizzando
                let nomeProvincia = provincia[
                  index
                ].trim();

                // Vedo se il prezzo medio per questa provincia è stato già calcolato
                var index = prezziMediZone.findIndex(
                  (x) => x.zona == nomeProvincia
                );

                // Se non c'è lo aggiungo
                if (index === -1) {
                  prezziMediZone.push({
                    zona: nomeProvincia,
                    prezzoMedio: valoriMediZona,
                  });
                }
              }
            );
          });

          // Mi creo un paggin tra zone e nazione così da poterlo usare per i dati del mercato del lavoro transfrontaliero
          let countryMapping = {
            "Alpes-de-Haute-Provence": "FR",
            "Alpes-Maritimes": "FR",
            Aosta: "IT",
            Belluno: "IT",
            Bolzano: "IT",
            Como: "IT",
            Cuneo: "IT",
            Gorenjska: "SL",
            Gorizia: "IT",
            Grigioni: "CH",
            "Haute-Savoie": "FR",
            "Hautes-Alpes": "FR",
            Imperia: "IT",
            Innsbruck: "AU",
            Karnten: "AU",
            Kitzbuhel: "AU",
            Lienz: "AU",
            Primorska: "SL",
            Savoie: "FR",
            "Severna-Primorska": "SL",
            Solden: "AU",
            Sondrio: "IT",
            "Spittal-An-Der-Drau": "AU",
            Ticino: "CH",
            Torino: "IT",
            Trieste: "IT",
            Udine: "IT",
            Vallese: "CH",
            Varese: "IT",
            Verbania: "IT",
            Vercelli: "IT",
            "Zell-am-See": "AU",
          };

          // Questa funzione mi definisce quali frecce verranno visualizzate e quali no, sfruttanto il costo medio
          // delle zone di partenza e di arrivo dei flussi e la conoscenza sul mercato di lavoro del luogo.
          var datiFlussi = dataResponse.map(
            (zona) => {
              // Mi prendo il prezzo medio della zona
              const prezzoZona = prezziMediZone.filter(
                (zonaMedio) =>
                  zonaMedio.zona === zona.zona
              )[0].prezzoMedio;
              return zona["vicini"].map(
                (coord) => {
                  // Mi creo una variabile che mi indica la probabilità di visualizzare la freccia dalla zona al vicino
                  let arrowOdds;
                  // Mi prendo il prezzo medio del vicino che sto analizzando
                  const prezzoVicino = prezziMediZone.filter(
                    (zonaMedio) =>
                      zonaMedio.zona ===
                      coord["zona"]
                  )[0].prezzoMedio;
                  // Se non ho il dato di una zona allora la freccia ha valore casuale
                  if (
                    isNaN(
                      parseFloat(prezzoZona)
                    ) ||
                    isNaN(
                      parseFloat(prezzoVicino)
                    )
                  ) {
                    arrowOdds = Math.random();
                  } else {
                    const differenzaPrezzo =
                      prezzoZona - prezzoVicino;
                    switch (true) {
                      case differenzaPrezzo <=
                        -500: {
                        arrowOdds = 0.25;
                        break;
                      }
                      case differenzaPrezzo >
                        -500 &&
                        differenzaPrezzo <= 0: {
                        arrowOdds = 0.5;
                        break;
                      }
                      case differenzaPrezzo > 0 &&
                        differenzaPrezzo <= 500: {
                        arrowOdds = 0.75;
                        break;
                      }
                      case differenzaPrezzo >
                        500: {
                        arrowOdds = 1;
                        break;
                      }
                    }
                  }

                  // Aggiunge o sottrae probabilità in base a quali sono le info sul mercato del lavoro
                  let countryZona =
                    countryMapping[zona.zona];
                  let countryVicino =
                    countryMapping[coord["zona"]];
                  if (countryZona === "IT") {
                    if (countryVicino === "SL") {
                      arrowOdds -= 0.75;
                    }
                    if (countryVicino === "AU") {
                      if (arrowOdds <= 0.5) {
                        arrowOdds += Math.random();
                      } else {
                        arrowOdds -= Math.random();
                      }
                    }
                    if (countryVicino === "FR") {
                      arrowOdds += 0.75;
                    }
                    if (countryVicino === "CH") {
                      arrowOdds += 0.75;
                    }
                  } else if (
                    countryZona === "AU"
                  ) {
                    if (countryVicino === "SL") {
                      arrowOdds -= 0.5;
                    }
                    if (countryVicino === "CH") {
                      arrowOdds += 0.75;
                    }
                    if (countryVicino === "IT") {
                      if (arrowOdds <= 0.5) {
                        arrowOdds += Math.random();
                      } else {
                        arrowOdds -= Math.random();
                      }
                    }
                  } else if (
                    countryZona === "SL"
                  ) {
                    if (countryVicino === "IT") {
                      arrowOdds += 0.75;
                    }
                    if (countryVicino === "AU") {
                      arrowOdds += 0.5;
                    }
                  } else if (
                    countryZona === "FR"
                  ) {
                    if (countryVicino === "IT") {
                      arrowOdds += 0.25;
                    }
                    if (countryVicino === "CH") {
                      arrowOdds += 0.75;
                    }
                  } else if (
                    countryZona === "CH"
                  ) {
                    arrowOdds = 0.1;
                  }
                  if (arrowOdds > 0.5) {
                    return [
                      zona["coord"],
                      coord["coord"],
                    ];
                  }
                }
              );
            }
          );
          var datiFlussi = [].concat
            .apply([], datiFlussi)
            .filter((el) => el !== undefined);
          var plArray = [];
          for (
            var i = 0;
            i < datiFlussi.length;
            i++
          ) {
            plArray.push(
              L.polyline(datiFlussi[i])
            );
          }
          flussiLayer = L.polylineDecorator(
            datiFlussi,
            {
              patterns: [
                {
                  offset: 0,
                  repeat: 10,
                  symbol: L.Symbol.dash({
                    pixelSize: 5,
                    pathOptions: {
                      color: "#000",
                      weight: 2,
                      opacity: 0.6,
                    },
                  }),
                },
                {
                  offset: "35%",
                  repeat: "35%",
                  symbol: L.Symbol.marker({
                    rotate: true,
                    markerOptions: {
                      icon: L.icon({
                        iconUrl:
                          "/static/MapCB/img/personWalking.png",
                        iconSize: [26, 26], // size of the icon
                        shadowSize: [12, 24], // size of the shadow
                        iconAnchor: [22, 0],
                      }),
                    },
                  }),
                },
              ],
            }
          );
          flussiLayer.addTo(map);
          flussiLayer.bringToFront();
        } else {
          console.log("error");
          return {};
        }
      },
      livelloSelezionato
    );
  } else {
    console.log("error");
  }
}

// Lancio la funzione che mi recupera i dati e me li visualizza
jsonRequest(
  "http://localhost:8000/api/prezzi_medi",
  visualizeData,
  livelloSelezionato
);

// Sezione che mi aggiunge le informazioni in alto a destra
let info = L.control();

info.onAdd = function () {
  this._div = L.DomUtil.create(
    "div",
    "info container"
  ); // create a div with a class "info"
  this.update();
  return this._div;
};

// method that we will use to update the control based on feature properties passed
info.update = function (props) {
  let htmlDatiPrezzi = "";
  // Se ci sono dei dati da visualizzare vengono aggiunti
  if (
    props &&
    typeof props.datiFiltrati !== "undefined" &&
    props.datiFiltrati.length > 0
  ) {
    let totaliAnnunci = [0, 0, 0];
    const mappingFasce = ["A", "M", "B"];

    props.datiFiltrati.map((dato) => {
      if (dato.fascia_prezzo === "A") {
        totaliAnnunci[0] += dato.num_annunci;
      }
      if (dato.fascia_prezzo === "M") {
        totaliAnnunci[1] += dato.num_annunci;
      }
      if (dato.fascia_prezzo === "B") {
        totaliAnnunci[2] += dato.num_annunci;
      }
    });

    totaliAnnunci.forEach((totale, id) => {
      htmlDatiPrezzi +=
        totale != 0
          ? "<div class='row'><div class='col-6'>Fascia Prezzo: <span class='text-danger'>" +
            mappingFasce[id] +
            "</span></div><div class='col-6'>Num. Annunci: <span class='text-danger'>" +
            totale +
            "</span></div></div>"
          : "";
    });
  } else {
    // Altrimenti viene indicata l'assenza di dati
    htmlDatiPrezzi =
      "<div class='row'><div class='col-12 text-danger'>Attenzione!\
     Nessun dato disponibile per questa zona.</div></div>";
  }
  this._div.innerHTML =
    "<div class='row'><div class='col-12'><h4>Dati " +
    livelloSelezionato +
    " <span class='badge " +
    (affitto_vendita === "A"
      ? "badge-info'>" + "Affitto"
      : "badge-warning'>" + "Vendita") +
    "</span></h4></div></div>" +
    (props
      ? "<div class='row'><div class='col-12'><b>" +
        props.Name +
        "</b> - <b class='text-capitalize'>" +
        props.Stato +
        "</b></div></div>" +
        htmlDatiPrezzi
      : "Passa il mouse su una zona");
};

info.addTo(map);

// Sezione che mi aggiunge la legenda in basso a destra
let legend = L.control({
  position: "bottomright",
});

legend.onAdd = function (map) {
  let div = L.DomUtil.create(
      "div",
      "info legend"
    ),
    grades = [0, 100],
    colors = [
      "#e10f47",
      "#d71e47",
      "#D62747",
      "#CB3F47",
      "#C05847",
      "#B57047",
      "#AA8947",
      "#9FA147",
      "#94BA47",
      "#89D247",
      "#7eeb47",
    ];

  // loop through our density intervals and generate a label with a colored square for each interval
  for (let i = grades[1]; i >= 0; i -= 10) {
    let legendLabel = "";
    if (i === 0) {
      legendLabel = "Costoso";
    } else if (i === 50) {
      legendLabel = "Medio";
    } else if (i === 100) {
      legendLabel = "Economico";
    }
    div.innerHTML +=
      '<i style="background:' +
      colors[i / 10] +
      '"></i> ' +
      (i === 0 || i === 50 || i === 100
        ? legendLabel
        : "") +
      "<br>";
  }

  div.innerHTML +=
    "<br>" +
    '<i style="background:#666666"></i> ' +
    "Dati Assenti" +
    "<br>";

  return div;
};

legend.addTo(map);
