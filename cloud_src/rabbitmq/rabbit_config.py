# RabbitMQ connection details
HOST = "localhost"

# Exchange details
PICTURAS_EXCHANGE= "picturas.tools"
EXCHANGE_DURABLE = True

# Queues and Routing keys
QUEUES = [
    {"name": "border-requests"              , "routing_key": "requests.border"               , "durable": True},
    {"name": "crop-requests"                , "routing_key": "requests.crop"                 , "durable": True},
    {"name": "rotation-requests"            , "routing_key": "requests.rotation"             , "durable": True},
    {"name": "brightness-requests"          , "routing_key": "requests.brightness"           , "durable": True},
    {"name": "binarization-requests"        , "routing_key": "requests.binarization"         , "durable": True},
    {"name": "resize-requests"              , "routing_key": "requests.resize"               , "durable": True},
    {"name": "count-people-requests"        , "routing_key": "requests.count-people"         , "durable": True},
    {"name": "object-detection-requests"    , "routing_key": "requests.object-detection"     , "durable": True},
    {"name": "background-removal-requests"  , "routing_key": "requests.background-removal"   , "durable": True},
    {"name": "watermark-requests"           , "routing_key": "requests.watermark"            , "durable": True},
    {"name": "results"                      , "routing_key": "results"                       , "durable": True},
]