// Creo la mia mappa posizionandola sul nord italia
var map = L.map("map").setView([45.8, 9.9], 6);

// Controll fullscreen
map.addControl(new L.Control.Fullscreen());

// Variabili che conterranno i layer della mappa con i confini e le aree cliccabili
var geojsonLayer, borderLayer;

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
    document.getElementById(
      "dati-raw"
    ).innerHTML = " ";
    document.getElementById(
      "dashboards"
    ).innerHTML = " ";
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

    document
      .getElementById("map")
      .classList.remove("col-lg-6");
    document
      .getElementById("dashboards")
      .classList.remove("col-lg-6");
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
}

// Zoomma quando l'utente clicca
function zoomToFeature(e) {
  document
    .getElementById("map")
    .classList.add("col-lg-6");
  var dashContainer = document.getElementById(
    "dashboards"
  );

  dashContainer.classList.add("col-lg-6");

  document.getElementById("dati-raw").innerHTML =
    "<div></div>";

  setTimeout(function () {
    map.invalidateSize();
    map.fitBounds(e.target.getBounds());
  }, timeout);

  timeout = 0;

  // Lancia la funzione che mi effettua il calcolo delle dashboard per l'area selezionata
  calcolaDashboard(e.target, dashContainer);
}

function onEachFeature(feature, layer) {
  layer.on({
    mouseover: highlightFeature,
    mouseout: resetHighlight,
    click: zoomToFeature,
  });
  layer._leaflet_id = feature.properties.Name;
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

    /*setTimeout(function () {
      geojsonLayer.eachLayer(function (layer) {
        layer._path.id =
          layer.feature.properties.Name;
      });
    }, 1000);*/

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

// Sezione che mi aggiunge il form di ricerca in basso a sinistra sulla mappa
let ricerca = L.control({
  position: "bottomleft",
});

ricerca.onAdd = function () {
  this._div = L.DomUtil.create(
    "div",
    "ricerca container"
  ); // create a div with a class "info"
  this.update();
  return this._div;
};

// Variabile che contiene i possibili valori da inserire nel campo ricerca
var nomiProvince = [
  "Alpes-de-Haute-Provence",
  "Alpes-Maritimes",
  "Aosta",
  "Belluno",
  "Bolzano",
  "Como",
  "Cuneo",
  "Gorenjska",
  "Gorizia",
  "Grigioni",
  "Haute-Savoie",
  "Hautes-Alpes",
  "Imperia",
  "Innsbruck",
  "Karnten",
  "Kitzbuhel",
  "Lienz",
  "Primorska",
  "Savoie",
  "Severna-Primorska",
  "Solden",
  "Sondrio",
  "Spittal-An-Der-Drau",
  "Ticino",
  "Torino",
  "Trieste",
  "Udine",
  "Vallese",
  "Varese",
  "Verbania",
  "Vercelli",
  "Zell-am-See",
];

ricerca.update = function () {
  this._div.innerHTML =
    "<div class='row'><div class='col-12'><h4>Ricerca " +
    livelloSelezionato +
    "</h4></div></div>" +
    "<div class='row'><div class='col-12'><form autocomplete='off' >" +
    "<div class='form-group autocomplete'><label for='localita'>Località: </label>" +
    "<input type='text' id='localita' name='localita' class='form-control' placeholder='Inserisci località'></input>" +
    "<small id='localitaErr' class='text-danger'></small>" +
    "</div></div></div>" +
    "<div class='row'><div class='col-12'><button id='cerca' class='btn btn-primary' type='submit'>Cerca</button>" +
    "</div></div>" +
    "</form></div></div>";
};

ricerca.addTo(map);

function autocomplete(inp, arr) {
  /*the autocomplete function takes two arguments,
  the text field element and an array of possible autocompleted values:*/
  var currentFocus;
  /*execute a function when someone writes in the text field:*/
  inp.addEventListener("input", function (e) {
    var a,
      b,
      i,
      val = this.value;
    /*close any already open lists of autocompleted values*/
    closeAllLists();
    if (!val) {
      return false;
    }
    currentFocus = -1;
    /*create a DIV element that will contain the items (values):*/
    a = document.createElement("DIV");
    a.setAttribute(
      "id",
      this.id + "autocomplete-list"
    );
    a.setAttribute("class", "autocomplete-items");
    /*append the DIV element as a child of the autocomplete container:*/
    this.parentNode.appendChild(a);
    /*for each item in the array...*/
    for (i = 0; i < arr.length; i++) {
      /*check if the item starts with the same letters as the text field value:*/
      if (
        arr[i]
          .substr(0, val.length)
          .toUpperCase() == val.toUpperCase()
      ) {
        /*create a DIV element for each matching element:*/
        b = document.createElement("DIV");
        /*make the matching letters bold:*/
        b.innerHTML =
          "<strong>" +
          arr[i].substr(0, val.length) +
          "</strong>";
        b.innerHTML += arr[i].substr(val.length);
        /*insert a input field that will hold the current array item's value:*/
        b.innerHTML +=
          "<input type='hidden' value='" +
          arr[i] +
          "'>";
        /*execute a function when someone clicks on the item value (DIV element):*/
        b.addEventListener("click", function (e) {
          /*insert the value for the autocomplete text field:*/
          inp.value = this.getElementsByTagName(
            "input"
          )[0].value;
          /*close the list of autocompleted values,
              (or any other open lists of autocompleted values:*/
          closeAllLists();
        });
        a.appendChild(b);
      }
    }
  });
  /*execute a function presses a key on the keyboard:*/
  inp.addEventListener("keydown", function (e) {
    var x = document.getElementById(
      this.id + "autocomplete-list"
    );
    if (x) x = x.getElementsByTagName("div");
    if (e.keyCode == 40) {
      /*If the arrow DOWN key is pressed,
        increase the currentFocus variable:*/
      currentFocus++;
      /*and and make the current item more visible:*/
      addActive(x);
    } else if (e.keyCode == 38) {
      //up
      /*If the arrow UP key is pressed,
        decrease the currentFocus variable:*/
      currentFocus--;
      /*and and make the current item more visible:*/
      addActive(x);
    } else if (e.keyCode == 13) {
      /*If the ENTER key is pressed, prevent the form from being submitted,*/
      e.preventDefault();
      if (currentFocus > -1) {
        /*and simulate a click on the "active" item:*/
        if (x) x[currentFocus].click();
      }
    }
  });
  function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length)
      currentFocus = 0;
    if (currentFocus < 0)
      currentFocus = x.length - 1;
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add(
      "autocomplete-active"
    );
  }
  function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (var i = 0; i < x.length; i++) {
      x[i].classList.remove(
        "autocomplete-active"
      );
    }
  }
  function closeAllLists(elmnt) {
    /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
    var x = document.getElementsByClassName(
      "autocomplete-items"
    );
    for (var i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
        x[i].parentNode.removeChild(x[i]);
      }
    }
  }
  /*execute a function when someone clicks in the document:*/
  document.addEventListener("click", function (
    e
  ) {
    closeAllLists(e.target);
  });
}

autocomplete(
  document.getElementById("localita"),
  nomiProvince
);

document
  .getElementById("cerca")
  .addEventListener("click", function (event) {
    event.preventDefault();
    const inputVal = document.getElementById(
      "localita"
    ).value;
    const contains = (arr, criteria) =>
      arr.some((v) => criteria(v));
    const localitaErr = document.getElementById(
      "localitaErr"
    );
    if (
      contains(
        nomiProvince,
        (v) => v === inputVal
      )
    ) {
      localitaErr.innerHTML = "";

      var layer = geojsonLayer.getLayer(inputVal);
      //fire event 'click' on target layer
      layer.fireEvent("click");
    } else {
      localitaErr.innerHTML =
        "La località cercata non è presente nel database.";
    }
  });
