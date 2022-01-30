d3.json("/data")
    .then(function (data) {
        function tabulate_addr_cr(data, columns) {
            let table = d3.select("#addr-cr")
                , columnNames = ["Street Number", "Street Name", "Apt #", "City", "State", "Zip", "Carrier Route"]
                , thead = table.append("thead")
                , tbody = table.append("tbody");

            // append the header row
            thead.append("tr")
                .selectAll("th")
                .data(columnNames)
                .enter()
                .append("th")
                .text(function (columnName) { return columnName; });

            // create a row for each object in the data
            let rows = tbody.selectAll("tr")
                .data(data)
                .enter()
                .append("tr");

            // create a cell in each row for each column
            rows.selectAll("td")
                .data(function (row) {
                    return columns.map(function (column) {
                        return { column: column, value: row[column] };
                    });
                })
                .enter()
                .append("td")
                .html(function (d) {
                    return d.value;
                });

            return table;
        };

        function tabulate_addr_count(data) {
            let table = d3.select("#addr-count")
                , columnNames = ["Carrier Route", "Address Count"]
                , thead = table.append("thead")
                , tbody = table.append("tbody");

            var computed = {}
            data.forEach(element => {
                if (computed[element["carrier_route"]]) {
                    let cr = computed[element["carrier_route"]]
                    cr["count"] += 1;
                } else {
                    computed[element["carrier_route"]] = { carrier_route: element["carrier_route"], count: 1 }
                }
            });
            // append the header row
            thead.append("tr")
                .selectAll("th")
                .data(columnNames)
                .enter()
                .append("th")
                .text(function (columnName) { return columnName; });

            // create a row for each object in the data
            let rows = tbody.selectAll("tr")
                .data(Object.values(computed))
                .enter()
                .append("tr");

            // create a cell in each row for each column
            let columns = ['carrier_route', 'count']
            rows.selectAll("td")
                .data(function (row) {
                    return columns.map(function (column) {
                        return { column: column, value: row[column] };
                    });
                })
                .enter()
                .append("td")
                .html(function (d) {
                    return d.value;
                });

            return table;
        };
        tabulate_addr_cr(data, ['street_number', 'street_name', 'apt_number', 'city', 'state', 'zip', 'carrier_route']);
        tabulate_addr_count(data);
    });
