<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PiXelTube Settings</title>
    <link rel="stylesheet" href="bootstrap/css/bootstrap.min.css">
    <script src="bootstrap/js/bootstrap.min.js"></script>
</head>
<body class="d-flex align-items-center justify-content-center" style="min-height: 100vh;">

    <div class="container">
        <h1 class="mb-4 text-center">PiXelTube Settings</h1>
        <?php
        // Check if the Mac address is provided in the URL
        if (isset($_GET['mac'])) {
            $macAddress = $_GET['mac'];
            ?>
            <form action="update_settings.php" method="post">
                <div class="form-group">
                    <label for="universe">Universe:</label>
                    <input type="text" class="form-control" id="universe" name="universe" placeholder="Enter Universe" required>
                </div>
                <br>
                <div class="form-group">
                    <label for="dmxAddress">DMX Address:</label>
                    <input type="text" class="form-control" id="dmxAddress" name="dmxAddress" placeholder="Enter DMX Address" required>
                </div>
                <input type="hidden" name="macAddress" value="<?php echo $macAddress; ?>">
                <button type="submit" class="btn btn-primary">Save Changes</button>
            </form>
            <?php
        } else {
            echo '<p class="text-danger">Mac address not provided in the URL.</p>';
        }
        ?>
    </div>
</body>
</html>