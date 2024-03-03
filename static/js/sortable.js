function sortTable(columnIndex, thElement) {
    var table, rows, switching, i, x, y, shouldSwitch, dir = "asc", switchcount = 0;
    table = document.getElementById("recordsTable");
    switching = true;
    // Make all columns neutral by removing any sort classes
    var allTh = table.getElementsByTagName("th");
    for (i = 0; i < allTh.length; i++) {
        allTh[i].classList.remove("sort-asc", "sort-desc");
    }
    while (switching) {
        switching = false;
        rows = table.rows;
        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            x = rows[i].getElementsByTagName("TD")[columnIndex];
            y = rows[i + 1].getElementsByTagName("TD")[columnIndex];
            if (dir == "asc") {
                if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                    shouldSwitch = true;
                    break;
                }
            } else if (dir == "desc") {
                if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                    shouldSwitch= true;
                    break;
                }
            }
        }
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            switchcount++;      
        } else {
            if (switchcount == 0 && dir == "asc") {
                dir = "desc";
                switching = true;
            }
        }
    }
    // Apply the sort class to the column that was just sorted
    if (dir == "asc") {
        thElement.classList.add("sort-asc");
    } else {
        thElement.classList.add("sort-desc");
    }
}



function searchTable() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("searchBox");
    filter = input.value.toUpperCase();
    table = document.getElementById("recordsTable");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td");
        for (let j = 0; j < td.length; j++) {
            if (td[j]) {
                txtValue = td[j].textContent || td[j].innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    tr[i].style.display = "";
                    break; // Stop loop if one cell matches
                } else {
                    tr[i].style.display = "none";
                }
            }       
        }
    }
}