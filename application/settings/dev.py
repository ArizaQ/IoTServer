from . import Config

class DevelopmentConfig(Config):
    '开发模式下的配置'
    # 查询时会显示原始SQL语句
    # SQLALCHEMY_ECHO = True

    SECRET_KEY='secret!'
    # MQTT 相关设置
    MQTT_BROKER_URL= '127.0.0.1'
    MQTT_BROKER_PORT=1883
    MQTT_USERNAME= 'IoT'
    MQTT_PASSWORD='liuhaitao'
    MQTT_KEEPALIVE=5
    MQTT_TLS_ENABLED=False
    # MySql相关设置
    DB_HOST="127.0.0.1"
    DB_PORT=3306
    DB_UN="root"
    DB_PW="123456"
    DB_NAME="iotdb"