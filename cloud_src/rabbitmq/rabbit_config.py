
# RabbitMQ connection details
HOST = "localhost"

# Exchange details
PICTURAS_EXCHANGE= "picturas.tools"
EXCHANGE_DURABLE = True

# Queues and Routing keys
QUEUES = [
    {"name": "border-requests"              , "routing_key": "border"               , "durable": True},
    {"name": "crop-requests"                , "routing_key": "crop"                 , "durable": True},
    {"name": "rotation-requests"            , "routing_key": "rotation"             , "durable": True},
    {"name": "brightness-requests"          , "routing_key": "brightness"           , "durable": True},
    {"name": "binarization-requests"        , "routing_key": "binarization"         , "durable": True},
    {"name": "resize-requests"              , "routing_key": "resize"               , "durable": True},
    {"name": "count-people-requests"        , "routing_key": "count_people"         , "durable": True},
    {"name": "object-detection-requests"    , "routing_key": "object_detection"     , "durable": True},
    {"name": "background-removal-requests"  , "routing_key": "background_removal"   , "durable": True},
    {"name": "watermark-requests"           , "routing_key": "requests.watermark"   , "durable": True},
    {"name": "results"                      , "routing_key": "results"              , "durable": True},
]
