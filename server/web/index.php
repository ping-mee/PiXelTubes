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

                $sql_query = "SELECT id, mac_address, universe, dmx_address FROM tubes";
                $result = $conn->query($sql_query);

                if ($result->num_rows > 0) {
                    // output data of each row
                    while($row = $result->fetch_assoc()) {
                        echo '
                        <tr>
                            <th>'.$row["id"].'</th>
                            <th>'.$row["universe"].'</th>
                            <th>'.$row["dmx_address"].'</th>
                            <th>
                                <button type="button" class="btn btn-secondary" data-toggle="modal" data-target="#configureModal" data-id="'.$row["mac_address"].'" data-universe="'.$row["universe"].'" data-dmx-address="'.$row["dmx_address"].'">Configure</button>                          
                            </th>
                        </tr>
                        ';
                    }
                }
                else {
                    echo "0 results";
                }
            ?>
        </tbody>
    </table>
    </div>

    <!-- Configure Modal -->
    <div class="modal" id="configureModal" tabindex="-1" role="dialog" aria-labelledby="configureModalLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="configureModalLabel">Configure DMX Address and Universe</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <form id="configureForm">
                        <div class="form-group">
                            <label for="dmxAddress">DMX Address:</label>
                            <input type="text" class="form-control" id="dmxAddress" placeholder="Enter DMX Address">
                        </div>
                        <div class="form-group">
                            <label for="universe">Universe:</label>
                            <input type="text" class="form-control" id="universe" placeholder="Enter Universe">
                        </div>
                        <button type="submit" class="btn btn-primary">Save Changes</button>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <script>
        // JavaScript to handle the modal and populate values when the button is clicked
        $('#configureModal').on('show.bs.modal', function (event) {
            var button = $(event.relatedTarget);
            var macAddress = button.data('id');
            var universe = button.data('universe');
            var dmxAddress = button.data('dmx-address');

            var modal = $(this);
            modal.find('.modal-title').text('Configure DMX Address and Universe for Tube ID ' + macAddress);
            modal.find('#dmxAddress').val(dmxAddress);
            modal.find('#universe').val(universe);
        });

        // JavaScript to handle form submission
        $('#configureForm').submit(function(event) {
            // Add your logic here to handle form submission using AJAX or other methods
            // You can access values with $('#dmxAddress').val() and $('#universe').val()
            event.preventDefault();
            $('#configureModal').modal('hide');
        });
    </script>

</div>
</body>
</html>
