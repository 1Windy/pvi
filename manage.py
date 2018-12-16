from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from pvi import create_app
import settings
import models

app = create_app()

migrate = Migrate(app, settings.db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
