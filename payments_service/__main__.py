from loafer.managers import LoaferManager

from payments_service.routes import routes

manager = LoaferManager(routes=routes)
manager.run()
