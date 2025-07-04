import logging
from logging.config import dictConfig

from storeapi.config import DevConfig, config
# filter = asgi_correlation_id.CorrelationIdFilter(uuid_lenght=8, default_value=3)

# with this we used the logtail management,add the source_token to our .env
def obfuscated(email:str, obfuscated_lenght) -> str:
    characters= email[:obfuscated_lenght]
    first,last = email.split("@")
    return characters + ('*' * len(first) - obfuscated_lenght) + '@' + last



class EmailObfuscationFilter(logging.Filter):
    def __init__(self, name: str = "",obfuscated_lenght:int = 2) -> None:
        super().__init__(name)
        self.obfuscated_lenght = obfuscated_lenght

    def filter(self, record:logging.LogRecord) -> bool:
        # record.my_variable = '123'
        if "email"  in record.__dict__:
            record.email = obfuscated(record.email,self.obfuscated_lenght)
        return True
    
handlers = ["default","rotating_file"]
if isinstance(config,DevConfig):
    handlers = ["default","rotating_file","logtail"]


def configure_logging() -> None:
    dictConfig(
        {
            "version":1,
            "disable_existing_loggers":False,
            "filters":{
                "correlation_id":{
                    "()":"asgi_correlation_id.CorrelationIdFilter",
                    "uuid_length": 8 if isinstance(config,DevConfig) else 32,
                    "default_value":"-",
                },
                'email_obfuscation':{
                    '()':EmailObfuscationFilter,
                    'obfuscated_length': 2 if isinstance(config,DevConfig) else 0,
                }
            },
            
            "formatters":{
                "console":{
                    "class":"logging.Formatter",
                    "datefmt":"%Y-%m-%dT%H:%M:%S",
                    "format":"(%(correlation_id)s) %(name)s: %(lineno)d - %(message)s"
                },
                "file":{
                    # "class":"logging.Formatter",
                    "class":"pythonjsonlogger.jsonlogger.JsonFormatter",
                    "datefmt":"%Y-%m-%dT%H:%M:%S",
                    "format":"%(asctime)s %(msecs)03dZ  %(levelname)-8s  [(%(correlation_id)s)] %(name)s %(lineno)d  %(message)s"
                }
            },
            "handlers":{
                "default":{
                    # "class":"logging.StreamHandler",
                    "class":"rich.logging.RichHandler",
                    "level":"DEBUG",
                    "formatter":"console",
                    "filters":["correlation_id","email_obfuscation"]
                },
                "rotating_file":{
                    "class":"logging.handlers.RotatingFileHandler",
                    "level":"DEBUG",
                    "formatter":"file",
                    "filename":"storeapi.log",
                    "maxBytes":1024 * 1024 * 5,
                    "backupCount":2,
                    "encoding":"utf8",
                    "filters":["correlation_id","email_obfuscation"],
                },
                "logtail":{
                    "class":"logtail.LogtailHandler",
                    "level":"DEBUG",
                    "formatter":"console",
                    "filters":["correlation_id","email_obfuscation"],
                    "source_token":config.LOGTAIL_API_KEY
                }
            },
            "loggers":{
                "uvicorn":{"handlers":["default","rotating_file"],"level":"INFO"},
                "storeapi":{
                    "handlers":handlers,
                    "level":"DEBUG" if isinstance(config,DevConfig) else "INFO",
                    "propagate":False,
                },
                "databases":{"handlers":["default"],"level":"WARNING"},
                "aiosqlite":{"handlers":["default"],"level":"WARNING"},
            }
        }
    )