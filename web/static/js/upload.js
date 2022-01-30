function create_address() {
    let street_name = d3.select("#address").property("value").split(" ")
    let street_number = street_name[0]
    let apt_number = d3.select("#apt-number").property("value")

    let city = d3.select("#city").property("value")
    let state = d3.select("#state").property("value")
    let zip = d3.select("#zip").property("value")

    let address = {
        street_number: street_number,
        street_name: street_name.splice(1).join(" "),
        apt_number: apt_number,
        city: city,
        state: state,
        zip: zip
    }
    return address
}

function format(address) {
    if (address.apt_number) {
        console.log(address)
        return address.street_number + " " + address.street_name + " Apt " + address.apt_number + " " + address.city + " " + address.state + " " + address.zip
    }

    return address.street_number + " " + address.street_name + " " + address.city + " " + address.state + " " + address.zip
}

function handle_click() {
    if (!this.addresses)
        this.addresses = []

    let address = create_address()
    if (address && address.street_name) {
        this.addresses.push(address)
    } else {
        return
    }

    let list = d3.select("#addresses")
        .attr("class", "list-group")

    let addressCp = []
    this.addresses.forEach(item => addressCp.push(item))
    let item = list.selectAll("li")
        .data(addressCp.reverse())

    item.html((d) => format(d))

    item.enter()
        .append("li")
        .attr("class", "list-group-item")
        .html((d) => format(d))

    item.exit()
        .remove()

    d3.select("#address-form")
        .selectAll("input[type=text]")
        .property("value", "")

    d3.select("#json")
        .property("value", JSON.stringify(this.addresses))

    d3.select("#json-submit")
        .property("hidden", false)

    console.log(d3.select("#json")
        .property("value"))
}


d3.select("#add-btn")
    .on("click", handle_click)

