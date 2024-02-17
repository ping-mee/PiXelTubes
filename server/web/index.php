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
                
                $conn = new mysqli($server, $username, $password)

                if ($conn->connect_error) {
                    die("Connection failed: " . $conn->connect_error);
                  }
                  echo "Connected successfully";

                
            ?>
            ?>
        </tbody>
    </table>
    </div>

</div>
</body>
</html>
