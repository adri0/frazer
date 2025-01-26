from mangum import Mangum

from frazer.api import app

handler = Mangum(app)
