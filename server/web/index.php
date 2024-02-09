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
        </tbody>
    </table>

    <div class="modal fade" id="tubeSettingsModal" tabindex="-1" role="dialog" aria-labelledby="tubeSettingsModalLabel"
         aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="tubeSettingsModalLabel">Tube Settings</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <form id="tubeSettingsForm">
                        <div class="form-group">
                            <label for="universeInput">Universe:</label>
                            <input type="number" class="form-control" id="universeInput" required>
                        </div>
                        <div class="form-group">
                            <label for="dmxAddressInput">DMX Address:</label>
                            <input type="number" class="form-control" id="dmxAddressInput" required>
                        </div>
                        <button type="submit" class="btn btn-primary">Save Changes</button>
                    </form>
                </div>
            </div>
        </div>
    </div>

</div>
</body>
</html>
