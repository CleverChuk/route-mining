import os
import web

# Configuration for deploying to google app engine
prod_config = {
    "UPLOAD_FOLDER":f"{os.getenv('GCLOUD_BUCKET')}/files",
    "EXPORT_FILE":f"{os.getenv('GCLOUD_BUCKET')}/files/export.xlsx"
}
app = web.create_app(config=prod_config)
