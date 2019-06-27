from flask_script import Manager
from App import create_app
from flask_migrate import MigrateCommand


app = create_app()
manager = Manager(app)
# 添加自定义的命令
manager.add_command('db', MigrateCommand)


# 对9取余
@app.template_filter('quyu')
def quyu(n):
    if n%8==0:
        return 1
    else:
        return n%8

if __name__ == '__main__':
    manager.run()
