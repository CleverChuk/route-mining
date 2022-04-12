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

            draw_pie_chart(Object.values(computed))
            return table;
        };

        function draw_pie_chart(data) {

            var width = 450
            height = 450
            margin = 40

            var radius = Math.min(width, height) / 2 - margin

            var svg = d3.select("svg")
                .attr("width", width)
                .attr("height", height)
                .append("g")
                .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");


            var color = d3.scaleOrdinal()
                .domain(data)
                .range(d3.schemeSet2);

            var pie = d3.pie()
                .value(function (d) { return d.count; })

            var data_ready = pie(data)

            var arcGenerator = d3.arc()
                .innerRadius(0)
                .outerRadius(radius)

            svg
                .selectAll('slices')
                .data(data_ready)
                .enter()
                .append('path')
                .attr('d', arcGenerator)
                .attr('fill', function (d) { return (color(d.data['carrier_route'])) })
                .attr("stroke", "black")
                .style("stroke-width", "2px")
                .style("opacity", 0.7)


            svg
                .selectAll('slices')
                .data(data_ready)
                .enter()
                .append('text')
                .text(function (d) { return d.data['carrier_route'] })
                .attr("transform", function (d) { return "translate(" + arcGenerator.centroid(d) + ")"; })
                .style("text-anchor", "middle")
                .style("font-size", 17)
        }
        tabulate_addr_cr(data, ['street_number', 'street_name', 'apt_number', 'city', 'state', 'zip', 'carrier_route']);
        tabulate_addr_count(data);
    });
