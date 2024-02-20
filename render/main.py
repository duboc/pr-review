import functions_framework
from google.cloud import storage
import markdown
import os
import argparse, sys, markdown

@functions_framework.http
def markdown_render(request):
    storage_client = storage.Client()
    bucket = storage_client.bucket(os.environ["BUCKET_NAME"])
    latest_build_id = bucket.get_blob("latest_build_id.txt").download_as_string().decode("utf-8")
    markdown_text = bucket.get_blob(f"{latest_build_id}.md").download_as_string().decode("utf-8")
    
    extensions = ['extra', 'smarty']
    html = markdown.markdown(markdown_text, extensions=extensions, output_format='html5')
    return TEMPLATE.replace('{{content}}', html)


# Inspired by https://gist.github.com/Fedik/674f4148439698a6681032b3bec370b3

TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            margin-top: 7em;
            font-family: Helvetica,Arial,sans-serif;
        }
        code, pre {
            font-family: monospace;
        }
    </style>
</head>
<body>
<div class="container container-table">
    <div class="row vertical-center-row">
        <div class="text-justify col-md-8 col-md-offset-2">
            {{content}}
        </div>
    </div>
</div>
</body>
</html>
"""