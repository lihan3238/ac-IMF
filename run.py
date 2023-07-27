from views import *
import ssl

def run(app):
    from config import host, port, debug
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')
    app.run(host=host, port=port, debug=debug, ssl_context=ssl_context)



def main():
    from database import create_app
    app = create_app(__name__)

    from config import csrf_key
    app.secret_key = csrf_key
    #print("csrf_key=="+str(csrf_key))
    # ----------- 注册蓝图 ------------ #
    app.register_blueprint(root, url_prefix='/')
    app.register_blueprint(register, url_prefix='/register')
    app.register_blueprint(login, url_prefix='/login')
    app.register_blueprint(logout, url_prefix='/logout')
    app.register_blueprint(file, url_prefix='/file')
    app.register_blueprint(shared_file, url_prefix='/shared_file')

    run(app)


if __name__ == '__main__':
    main()
