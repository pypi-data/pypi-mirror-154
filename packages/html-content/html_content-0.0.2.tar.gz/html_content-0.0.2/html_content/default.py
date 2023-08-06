
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <title>TITLE</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
  <style>
    table.table-fit {
        width: auto !important;
        table-layout: auto !important;
    }
    table.table-fit thead th, table.table-fit tfoot th {
        width: auto !important;
    }
    table.table-fit tbody td, table.table-fit tfoot td {
        width: auto !important;
        padding-left: 10px;
        padding-right: 10px;
    }
    div {
        margin-top: 15px;
        margin-bottom: 10px;
    }
    table tr:hover td {
        border-bottom: 1px solid #aaa;
        border-top: 1px solid #aaa;
    }
  </style>
</head>
<body>

<div class="container">
  CONTENT
</div>

</body>
</html>

"""
