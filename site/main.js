const sexes = ["male", "female", "combined"];
const years = ["Average", "08-12", "09-13", "10-14", "11-15"];
const alltypes = "All Sites / Types"

function get_ci(data, year, category, sex) {
    /* Get confidence intervals, returning "Not Applicable"
    if the year range is the "Average" of all the ranges,
    or if the ci range data isn't present.
    */
    if (year == "Average") { return "NA"; }
    if (data[year][category][sex]["ci_low"] == null) { return "NA"; }
    var ci_low = data[year][category][sex]["ci_low"].toFixed(2);
    var ci_high = data[year][category][sex]["ci_high"].toFixed(2);
    return ci_low + " - " + ci_high;
}

function loadCityData(city, data) {
    $("#cityname").html(city);
    // Load average data first.
    for (s in sexes) {
        var sex = sexes[s];
        var tableBody = "";
        for (y in years) {
            var year = years[y];
            var row = "<tr>";
            var sir = "NA";
            if (
                (data[year][alltypes][sex]["sir"] != null) &&
                (
                    (data[year][alltypes][sex]["significant"] == true) ||
                    (year == "Average")
                )
            ) {
                sir = data[year][alltypes][sex]["sir"].toFixed(2);
            }
            var rank = "NA";
            if (
                (data[year][alltypes][sex]["significant"] == true) ||
                ((sir != "NA") && (year == "Average"))
            ) {
                rank = data["Rank"][year][alltypes][sex];
            }
            row += "<td>" + year + "</td>";
            row += "<td>" + rank + "</td>";
            row += "<td>" + sir + "</td>";
            row += "<td>" + get_ci(data, year, alltypes, sex) + "</td>";
            row += "</tr>";
            tableBody += row;
        }
        $("#"+sex).html(tableBody);
    }
    // Load in the rest of the stats, separate by year range.
    for (y in years) {
        var year = years[y];
        var tableBody = "";
        var categories = Object.keys(data[year]);
        categories.sort();
        for (c in categories) {
            var category = categories[c];
            for (g in sexes) {
                var sex = sexes[g];
                var rowData = data[year][category][sex];
                var sir = "NA";
                if ((rowData["significant"] == true) &&
                    (rowData["sir"] != null)) {
                    sir = data[year][alltypes][sex]["sir"].toFixed(2);
                }
                var row = "<tr>";
                row += "<td>" + year + "</td>";
                row += "<td>" + category + "</td>";
                row += "<td>" + sex + "</td>";
                row += "<td>" + rowData["observed"].toFixed(2) + "</td>";
                row += "<td>" + rowData["expected"].toFixed(2) + "</td>";
                row += "<td>" + sir + "</td>";
                row += "<td>" + get_ci(data, year, category, sex) + "</td>";
                row += "</tr>";
                tableBody += row;
            }
        }
        $("#details_" + year).html(tableBody);
    }

}

$( document ).ready(function() {
    var options = "<option></option>";
    for (city in cities) {
        options += "<option>" + cities[city] + "</option>";
    }
    $("#cityselect").html(options);

    $("#cityselect").change(function() {
      var name = $(cityselect).val();
      if (name.length == 0) {
          $("#city").hide();
          $("#cityname").html("");
          $("#downloadjson").hide();
      } else {
          $("#city").show();
          $("#downloadjson").show();          
          $("#downloadjson").attr("href", "data/" + name + ".json");
          $.getJSON("./data/" + name + ".json", function(data) {
              loadCityData(name, data);
          });
      }
    });
});