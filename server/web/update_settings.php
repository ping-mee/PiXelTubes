<?php
    $server = "localhost";
    $username = "pxm";
    $password = "pixel";
    $db_name = "pixeltube_db";

    $conn = new mysqli($server, $username, $password, $db_name);

    $conn = new mysqli($server, $username, $password, $db_name);

    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

// Check if the form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Get the form data
    $macAddress = $_POST['macAddress'];
    $dmxAddress = $_POST['dmxAddress'];
    $universe = $_POST['universe'];
    
    $update_query = "UPDATE tubes SET dmx_address = '$dmxAddress', universe = '$universe' WHERE mac_address = '$macAddress'";
    
    $conn->close();
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="bootstrap/css/bootstrap.min.css">
    <script src="bootstrap/js/bootstrap.bundle.min.js"></script>
    <script src="jquery/jquery.min.js"></script>
</head>
    <body class="d-flex align-items-center justify-content-center" style="min-height: 100vh;">
        <div class="container">
            <h1 class="mb-4 text-center">Update Settings</h1>
            <?php
                if ($conn->query($update_query) === TRUE) {
                    header("Location: ".$_SERVER['SERVER_NAME']."/");
                    exit();
                } else {
                    echo '<p class="text-danger">Error updating settings: ' . $conn->error . '</p>';
                }
            ?>
        </div>
    </body>
</html>
