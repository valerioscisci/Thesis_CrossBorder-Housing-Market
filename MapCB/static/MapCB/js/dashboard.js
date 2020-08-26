// Funzioni necessarie al calcolo delle dashboard

// Funzione che mi carica l'html per ogni prezzo che verrà visualizzato sottoforma di tabella
function caricaHtmlDatiRaw() {
  return new Promise((resolve) => {
    var dataFilteredAF = dataSelected.filter(
      (dato) =>
        dato.affitto_vendita === affitto_vendita
    );
    console.log(dataFilteredAF);
    setTimeout(() => {
      resolve(
        "<div class='col-12 text-center'><h3 class='display-4 my-5' id='lista-dati-title'>Lista Dati Singoli</h3>" +
          "<div class='table-responsive'><table class='table table-dark table-bordered table-striped table-hover' id='dati-raw-table'><thead>" +
          "<tr><th scope='col'>#</th>" +
          "<th scope='col'>Stato</th>" +
          "<th scope='col'>Regione</th>" +
          "<th scope='col'>Provincia</th>" +
          "<th scope='col'>Comune</th>" +
          "<th scope='col'>Codice Postale</th>" +
          "<th scope='col'>Nome Annuncio</th>" +
          "<th scope='col'>Metri Quadri</th>" +
          "<th scope='col'>Prezzo</th>" +
          "<th scope='col'>Latitudine e Longitudiine</th>" +
          "<th scope='col'>Data Inserimento</th></tr>" +
          "</thead><tbody>" +
          (dataFilteredAF.length != 0
            ? dataFilteredAF
                .map((dato, id) => {
                  return (
                    "<tr><th scope='row'>" +
                    id +
                    "</th><td class='text-capitalize'>" +
                    dato.stato +
                    "</td><td>" +
                    dato.regione +
                    "</td><td>" +
                    dato.provincia +
                    "</td><td>" +
                    dato.comune +
                    "</td><td>" +
                    (dato.zip_code != 0
                      ? dato.zip_code
                      : "Non presente") +
                    "</td><td>" +
                    dato.nome_annuncio +
                    "</td><td>" +
                    (dato.metri_quadri > -1
                      ? dato.metri_quadri
                      : "Non presente") +
                    "</td><td>" +
                    (dato.prezzo > 100
                      ? dato.prezzo +
                        " <span class='oi oi-euro'></span>"
                      : "Non presente") +
                    "</td><td>[" +
                    dato.latitudine +
                    ", " +
                    dato.longitudine +
                    "]</td><td>" +
                    dato.data_inserimento +
                    "</td></tr>"
                  );
                })
                .join("")
            : "<tr><td>Nessun dato presente</td></tr>") +
          "</tbody></table></div></div>"
      );
    }, 2000);
  });
}

// Funzione che mi visualizza i prezzi singoli per la zona
async function visualizzaDatiSingoli(
  datiRawContainer
) {
  datiRawContainer.innerHTML =
    "<div class='text-center col-12'><h2>...Caricamento Lista Dati...</h2>" +
    "<div class='spinner-grow color-primary' role='status'>" +
    "<span class='sr-only'>Loading...</span></div></div>";
  const result = await caricaHtmlDatiRaw();
  datiRawContainer.innerHTML = result;
}

function caricaDatiRaw(status, dataResponse) {
  if (status === null) {
    dataSelected = dataResponse;
    var datiRawContainer = document.getElementById(
      "dati-raw"
    );

    var observer = new IntersectionObserver(
      function (entries) {
        if (entries[0].isIntersecting === true) {
          observer.unobserve(datiRawContainer);
          visualizzaDatiSingoli(datiRawContainer);
        }
      },
      { threshold: [0.25] }
    );

    observer.observe(datiRawContainer);
  } else {
    console.log("error");
    return {};
  }
}

// Funzione che mi carica i dati e costruisce l'html delle dashboard
function caricaHtmlDashboard(e) {
  return new Promise((resolve) => {
    const featureName = e.feature.properties.Name;
    const featureState =
      e.feature.properties.Stato;

    jsonRequest(
      "http://localhost:8000/api/prezzi/" +
        featureName,
      caricaDatiRaw,
      livelloSelezionato
    );

    var numAnnunci = 0;

    var PrezzoMedio = (
      e.feature.properties.datiFiltrati.reduce(
        (prev, cur) => {
          numAnnunci += cur.num_annunci;
          return (prev += cur.PrezzoPercentuale);
        },
        0
      ) / numAnnunci
    ).toFixed(2);

    e.feature.properties.PrezzoMedio = PrezzoMedio;

    setTimeout(() => {
      // idee: dashboard torta prezzi, dashboard prezzi vicini, dashboard prezzi nel tempo
      resolve(
        "<h3 class='display-4 text-center mt-5 mt-lg-0'>" +
          featureName +
          " - <span class='text-capitalize'>" +
          featureState +
          "</span></h3>" +
          "<div class='container'><div class='row'><div class='col-12'>" +
          "<ul class='nav nav-tabs' id='dashTab' role='tablist'>" +
          "<li class='nav-item'>" +
          "<a class='nav-link active' id='tab-medie' data-toggle='tab' href='#medie' role='tab' aria-controls='medie' aria-selected='true'>Dati Medi</a>" +
          "</li>" +
          "<li class='nav-item'>" +
          "<a class='nav-link' id='tab-dettaglio' data-toggle='tab' href='#dettaglio' role='tab' aria-controls='dettaglio' aria-selected='false'>Dettaglio Dati</a>" +
          "</li>" +
          "<li class='nav-item'>" +
          "<a class='nav-link' id='tab-vicine' data-toggle='tab' href='#vicine' role='tab' aria-controls='vicine' aria-selected='false'>Zone Vicine</a>" +
          "</li>" +
          "<li class='nav-item'>" +
          "<a class='nav-link' id='tab-trend' data-toggle='tab' href='#trend' role='tab' aria-controls='trend' aria-selected='false'>Trend</a>" +
          "</li>" +
          "</ul>" +
          "<div class='tab-content mt-3' id='dashTabContent'>" +
          "<div class='tab-pane fade show active' id='medie' role='tabpanel' aria-labelledby='tab-medie'>" +
          "<p class='lead text-justify'>In questa dashboard è possibile visualizzare in che fascia ricadono mediamente i prezzi degli immobili, nonchè l'ammontare medio degli stessi.<p>" +
          "<div class='text-center'><div class='bg-light rounded border border-secondary p-3 m-3 box-prezzi'>" +
          "<h3>Prezzo medio <strong>" +
          (affitto_vendita === "A"
            ? "Affitto"
            : "Vendita") +
          "</strong>: <span class='color-primary'>" +
          e.feature.properties.PrezzoMedio +
          " <span class='oi oi-euro'></span></span></h3></div><hr class='hr-mappa'>" +
          (e.feature.properties.PrezzoMedio !=
          "NaN"
            ? "<span class='oi oi-pie-chart color-secondary h2'></span><br><h4><em>Diagramma <u>numero annunci per fascia di prezzo</u></em></h4>" +
              "<div id='medieDash'></div></div></div>"
            : "<h3 class='alert alert-danger' role='alert'>Dashboard non disponibile</h3></div></div>") +
          "<div class='tab-pane fade' id='dettaglio' role='tabpanel' aria-labelledby='tab-dettaglio'>trewtre</div>" +
          "<div class='tab-pane fade' id='vicine' role='tabpanel' aria-labelledby='tab-vicine'>ertret</div>" +
          "<div class='tab-pane fade' id='trend' role='tabpanel' aria-labelledby='tab-trend'>ertre</div>" +
          "</div>" +
          "</div></div></div>"
      );
    }, 1000);
  });
}

// Funzione che mi calcola le dashboard
async function calcolaDashboard(
  e,
  dashContainer
) {
  dashContainer.innerHTML =
    "<div class='text-center'><h2>...Caricamento Dashboard...</h2>" +
    "<div class='spinner-border color-primary' role='status'>" +
    "<span class='sr-only'>Loading...</span></div></div>";
  const result = await caricaHtmlDashboard(e);
  dashContainer.innerHTML = result;

  // Costruzione DIAGRAMMA A TORTA

  if (e.feature.properties.PrezzoMedio != "NaN") {
    // Setta le dimensioni in base alla grandezza del container dove verrà inserito
    var width =
      document.getElementById("medie")
        .offsetWidth / 1.7;
    height = width;
    margin = 45;

    // Viene settato il raggio
    var radius =
      Math.min(width, height) / 2 - margin;

    // Viene aggiunto l'elemento svg al container
    var svg = d3
      .select("#medieDash")
      .attr("class", "text-center")
      .append("svg")
      .attr("width", width)
      .attr("height", height)
      .append("g")
      .attr(
        "transform",
        "translate(" +
          width / 2 +
          "," +
          height / 2 +
          ")"
      );

    // Calcolo annunci per fascia di prezzo
    var totaliAnnunci = [0, 0, 0];
    e.feature.properties.datiFiltrati.map(
      (dato) => {
        if (dato.fascia_prezzo === "A") {
          totaliAnnunci[0] += dato.num_annunci;
        }
        if (dato.fascia_prezzo === "M") {
          totaliAnnunci[1] += dato.num_annunci;
        }
        if (dato.fascia_prezzo === "B") {
          totaliAnnunci[2] += dato.num_annunci;
        }
      }
    );

    // Assegna i dati alle 3 variabili
    var data = {
      Alto: totaliAnnunci[0],
      Medio: totaliAnnunci[1],
      Basso: totaliAnnunci[2],
    };

    // Setta i colori
    var color = d3
      .scaleOrdinal()
      .domain(["Alto", "Medio", "Basso"])
      .range(["#e10f47", "#C05847", "#7eeb47"]);

    // Calcola la posizione di ogni elemento della torta
    var pie = d3
      .pie()
      .sort(null) // Non ordina gli elementi per grandezza
      .value(function (d) {
        return d.value;
      });
    var data_ready = pie(d3.entries(data));

    var arc = d3
      .arc()
      .innerRadius(radius * 0.5) // This is the size of the donut hole
      .outerRadius(radius * 0.8);

    var outerArc = d3
      .arc()
      .innerRadius(radius * 0.9)
      .outerRadius(radius * 0.9);

    svg
      .selectAll("allSlices")
      .data(data_ready)
      .enter()
      .append("path")
      .attr("d", arc)
      .attr("fill", function (d) {
        return color(d.data.key);
      })
      .attr("stroke", "white")
      .style("stroke-width", "2px")
      .style("opacity", 0.7);

    svg
      .selectAll("allPolylines")
      .data(data_ready)
      .enter()
      .append("polyline")
      .attr("stroke", "black")
      .style("fill", "none")
      .attr("stroke-width", 1)
      .attr("points", function (d) {
        var posA = arc.centroid(d); // line insertion in the slice
        var posB = outerArc.centroid(d); // line break: we use the other arc generator that has been built only for that
        var posC = outerArc.centroid(d); // Label position = almost the same as posB
        var midangle =
          d.startAngle +
          (d.endAngle - d.startAngle) / 2; // we need the angle to see if the X position will be at the extreme right or extreme left
        posC[0] =
          radius *
          0.95 *
          (midangle < Math.PI ? 1 : -1); // multiply by 1 or -1 to put it on the right or on the left
        return [posA, posB, posC];
      });

    svg
      .selectAll("allLabels")
      .data(data_ready)
      .enter()
      .append("text")
      .text(function (d) {
        return d.data.key;
      })
      .attr("transform", function (d) {
        var pos = outerArc.centroid(d);
        var midangle =
          d.startAngle +
          (d.endAngle - d.startAngle) / 2;
        pos[0] =
          radius *
          0.99 *
          (midangle < Math.PI ? 1 : -1);
        return "translate(" + pos + ")";
      })
      .style("text-anchor", function (d) {
        var midangle =
          d.startAngle +
          (d.endAngle - d.startAngle) / 2;
        return midangle < Math.PI
          ? "start"
          : "end";
      });

    svg
      .append("text")
      .attr("text-anchor", "middle")
      .attr("y", -30)
      .attr("font-size", "1.3em")
      .text("Alto: " + totaliAnnunci[0]);
    svg
      .append("text")
      .attr("text-anchor", "middle")
      .attr("y", 0)
      .attr("font-size", "1.3em")
      .text("Medio: " + totaliAnnunci[1]);
    svg
      .append("text")
      .attr("text-anchor", "middle")
      .attr("y", 30)
      .attr("font-size", "1.3em")
      .text("Basso: " + totaliAnnunci[2]);
  }
}
