<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PiXelTube Web Interface</title>
    <link rel="stylesheet" href="bootstrap/css/bootstrap.min.css">
    <script src="bootstrap/js/bootstrap.bundle.min.js"></script>
</head>
<body>

<div class="container mt-5">
    <h1 class="mb-4">PiXelTube Web Interface</h1>
    <table class="table">
        <thead>
        <tr>
            <th scope="col">Tube ID</th>
            <th scope="col">Universe</th>
            <th scope="col">DMX Address</th>
            <th scope="col">Actions</th>
        </tr>
        </thead>
        <tbody id="tubeList">
            <?php
                $server = "localhost";
                $username = "pxm";
                $password = "pixel";
                $db_name = "pixeltube_db";
                
                $conn = new mysqli($server, $username, $password, $db_name);

                if ($conn->connect_error) {
                    die("Connection failed: " . $conn->connect_error);
                  }
                  echo "Connected successfully";

                $sql_query = "SELECT id, mac_address, universe, dmx_address FROM tubes";
                $result = $conn->query($sql_query);

                if ($result->num_rows > 0) {
                    // output data of each row
                    while($row = $result->fetch_assoc()) {
                        echo '''
                        <tr>
                            <th>'.$row["id"].'</th>
                            <th>'.$row["universe"].'</th>
                            <th>'.$row["dmx_address"].'</th>
                            <th>
                                <form action="./settings.php?id='.$row["mac_address"]'">
                                    <button type="submit" class="btn btn-secondary">Configure</button>
                                </form>                            
                            </th>
                        </tr>
                        ''';
                    }
                }
                else {
                    echo "0 results";
                }
            ?>
        </tbody>
    </table>
    </div>

</div>
</body>
</html>
