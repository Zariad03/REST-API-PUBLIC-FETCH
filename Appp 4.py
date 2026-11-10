from flask import Flask, render_template_string

app = Flask(__name__)

PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Active Safety System Data</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 25px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }

        th, td {
            border: 1px solid #ccc;
            padding: 10px;
            text-align: left;
        }

        th {
            background-color: #eeeeee;
        }

        #status {
            margin-top: 15px;
        }

        .error {
            color: red;
        }
    </style>
</head>

<body>

    <h1>Active Safety System</h1>

    <p>Car part information from the NHTSA public API.</p>

    <p id="status">Loading data...</p>

    <table id="dataTable" hidden>
        <thead>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Data Type</th>
                <th>Group Name</th>
            </tr>
        </thead>

        <tbody id="dataBody"></tbody>
    </table>

    <script>
        async function loadData() {
            const status = document.getElementById("status");
            const table = document.getElementById("dataTable");
            const tableBody = document.getElementById("dataBody");

            status.textContent = "Loading data...";
            table.hidden = true;
            tableBody.innerHTML = "";

            const apiURL =
                "https://vpic.nhtsa.dot.gov/api/vehicles/GetVehicleVariableList?format=json";

            try {
                const response = await fetch(apiURL);

                if (!response.ok) {
                    throw new Error("Unable to connect to the API.");
                }

                const data = await response.json();

                if (!Array.isArray(data.Results)) {
                    throw new Error("The API data format is incorrect.");
                }

                // Only display the exact Active Safety System group.
                const filter = {
                    GroupName: "Active Safety System"
                };

                const filteredResults = data.Results.filter(item =>
                    item.GroupName === filter.GroupName
                );

                filteredResults.forEach(item => {
                    const row = document.createElement("tr");

                    [item.ID, item.Name, item.DataType, item.GroupName]
                        .forEach(value => {
                            const cell = document.createElement("td");
                            cell.textContent = value ?? "";
                            row.appendChild(cell);
                        });

                    tableBody.appendChild(row);
                });

                if (filteredResults.length > 0) {
                    status.textContent =
                        "Data loaded successfully. Records found: "
                        + filteredResults.length;

                    table.hidden = false;
                } else {
                    status.textContent =
                        "No Active Safety System records were found.";
                }

            } catch (error) {
                status.textContent =
                    "Error loading data: " + error.message;

                status.className = "error";
            }
        }

        loadData();
    </script>

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(PAGE)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
